'''
Executes the Powerplant model testbench in Powerfactory.
'''
DEBUG = True
import os
#Ensure right working directory
executePath = os.path.abspath(__file__)
executeFolder = os.path.dirname(executePath)
os.chdir(executeFolder)

from configparser import ConfigParser

class readConfig:
  def __init__(self) -> None:
    self.cp = ConfigParser(allow_no_value=True)
    self.cp.read('config.ini')
    self.parsedConf = self.cp['config']
    self.sheetPath = str(self.parsedConf['Casesheet path'])
    self.pythonPath = str(self.parsedConf['Python path'])
    self.volley = int(self.parsedConf['Volley'])
    self.parallel = bool(self.parsedConf['Parallel'])
    self.exportPath = str(self.parsedConf['Export folder'])
    self.QDSLcopyGrid = str(self.parsedConf['QDSL copy grid'])

config = readConfig()
import sys
sys.path.append(config.pythonPath)

from typing import Optional, Tuple, List, Union
if getattr(sys, 'gettrace', None) is not None:
  sys.path.append('C:\\Program Files\\DIgSILENT\\PowerFactory 2024 SP2\\Python\\3.8')
import powerfactory as pf #type: ignore 

import re
import time
from datetime import datetime
import case_setup as cs
import sim_interface as si

def connectPF() -> Tuple[pf.Application, pf.DataObject, pf.DataObject]:
  '''
  Connects to the powerfactory application and returns the application, project and this script object.
  '''
  app : pf.Application = pf.GetApplicationExt()
  if not app:
    raise RuntimeError('No connection to powerfactory application')
  app.Show()
  app.ClearOutputWindow()
  app.PrintInfo(f'Powerfactory application connected externally. Executable: {sys.executable}')
  app.PrintInfo(f'Imported powerfactory module from {pf.__file__}')

  project : Optional[pf.DataObject] = app.GetActiveProject()

  if DEBUG:
    while project is None:
        time.sleep(1)
        project = app.GetActiveProject() 

  assert project is not None

  networkData = app.GetProjectFolder('netdat')
  assert networkData is not None

  thisScript : Optional[pf.DataObject] = networkData.SearchObject('MTB\\MTB\\execute.ComPython')
  assert thisScript is not None

  return app, project, thisScript

def resetProjectUnits(project : pf.DataObject) -> None:
  '''
  Resets the project units to the default units.
  '''
  #SetPrj = project.SearchObject('Settings\\Project Settings.SetPrj')
  SetPrj = project.SearchObject('Settings.SetFold')
  if SetPrj:
    SetPrj.Delete()
  #ComIncUnits = project.SearchObject('Settings\\Units')
  #if ComIncUnits:
  #  ComIncUnits.Delete()

  project.Deactivate() #type: ignore
  project.Activate() #type: ignore

def setupResFiles(app : pf.Application, root : pf.DataObject):
  '''
  Setup the result files for the studycase.
  '''
  elmRes = app.GetFromStudyCase('ElmRes') #type: ignore
  assert elmRes is not None

  measurementBlock = root.SearchObject('measurements.ElmDsl') #type: ignore 
  assert measurementBlock is not None

  elmRes.AddVariable(measurementBlock, 's:Ia_pu') #type: ignore
  elmRes.AddVariable(measurementBlock, 's:Ib_pu') #type: ignore
  elmRes.AddVariable(measurementBlock, 's:Ic_pu') #type: ignore
  elmRes.AddVariable(measurementBlock, 's:Vab_pu') #type: ignore
  elmRes.AddVariable(measurementBlock, 's:Vag_pu') #type: ignore
  elmRes.AddVariable(measurementBlock, 's:Vbc_pu') #type: ignore
  elmRes.AddVariable(measurementBlock, 's:Vbg_pu') #type: ignore
  elmRes.AddVariable(measurementBlock, 's:Vca_pu') #type: ignore
  elmRes.AddVariable(measurementBlock, 's:Vcg_pu') #type: ignore
  elmRes.AddVariable(measurementBlock, 's:f_hz') #type: ignore
  elmRes.AddVariable(measurementBlock, 's:neg_Id_pu') #type: ignore
  elmRes.AddVariable(measurementBlock, 's:neg_Imag_pu') #type: ignore
  elmRes.AddVariable(measurementBlock, 's:neg_Iq_pu') #type: ignore
  elmRes.AddVariable(measurementBlock, 's:neg_Vmag_pu') #type: ignore
  elmRes.AddVariable(measurementBlock, 's:pos_Id_pu') #type: ignore
  elmRes.AddVariable(measurementBlock, 's:pos_Imag_pu') #type: ignore
  elmRes.AddVariable(measurementBlock, 's:pos_Iq_pu') #type: ignore
  elmRes.AddVariable(measurementBlock, 's:pos_Vmag_pu') #type: ignore
  elmRes.AddVariable(measurementBlock, 's:ppoc_pu') #type: ignore 
  elmRes.AddVariable(measurementBlock, 's:qpoc_pu') #type: ignore

  mtb_s_pref_pu = root.SearchObject('mtb_s_pref_pu.ElmDsl') #type: ignore
  assert mtb_s_pref_pu is not None
  elmRes.AddVariable(mtb_s_pref_pu,  's:yo') #type: ignore

  mtb_s_qref_pu = root.SearchObject('mtb_s_qref_pu.ElmDsl') #type: ignore
  assert mtb_s_qref_pu is not None
  elmRes.AddVariable(mtb_s_qref_pu,  's:yo') #type: ignore

  mtb_s_1 = root.SearchObject('mtb_s_1.ElmDsl') #type: ignore
  assert mtb_s_1 is not None
  elmRes.AddVariable(mtb_s_1,  's:yo') #type: ignore

  mtb_s_2 = root.SearchObject('mtb_s_2.ElmDsl') #type: ignore
  assert mtb_s_2 is not None
  elmRes.AddVariable(mtb_s_2,  's:yo') #type: ignore

  mtb_s_3 = root.SearchObject('mtb_s_3.ElmDsl') #type: ignore
  assert mtb_s_3 is not None
  elmRes.AddVariable(mtb_s_3,  's:yo') #type: ignore

  mtb_s_4 = root.SearchObject('mtb_s_4.ElmDsl') #type: ignore
  assert mtb_s_4 is not None
  elmRes.AddVariable(mtb_s_4,  's:yo') #type: ignore

  mtb_s_5 = root.SearchObject('mtb_s_5.ElmDsl') #type: ignore
  assert mtb_s_5 is not None
  elmRes.AddVariable(mtb_s_5,  's:yo') #type: ignore

  mtb_s_6 = root.SearchObject('mtb_s_6.ElmDsl') #type: ignore
  assert mtb_s_6 is not None
  elmRes.AddVariable(mtb_s_6,  's:yo') #type: ignore

  mtb_s_7 = root.SearchObject('mtb_s_7.ElmDsl') #type: ignore
  assert mtb_s_7 is not None
  elmRes.AddVariable(mtb_s_7,  's:yo') #type: ignore

  mtb_s_8 = root.SearchObject('mtb_s_8.ElmDsl') #type: ignore
  assert mtb_s_8 is not None
  elmRes.AddVariable(mtb_s_8,  's:yo') #type: ignore

  mtb_s_9 = root.SearchObject('mtb_s_9.ElmDsl') #type: ignore
  assert mtb_s_9 is not None
  elmRes.AddVariable(mtb_s_9,  's:yo') #type: ignore

  mtb_s_10 = root.SearchObject('mtb_s_10.ElmDsl') #type: ignore
  assert mtb_s_10 is not None
  elmRes.AddVariable(mtb_s_10,  's:yo') #type: ignore
  
def setupExport(app : pf.Application, filename : str):
    '''
    Setup the export component for the studycase.
    '''
    comRes = app.GetFromStudyCase('ComRes')
    elmRes = app.GetFromStudyCase('ElmRes')
    assert comRes is not None

    csvFileName = f'{filename}.csv'
    comRes.SetAttribute('pResult', elmRes)
    comRes.SetAttribute('iopt_exp', 6)
    comRes.SetAttribute('iopt_sep', 0)
    comRes.SetAttribute('ciopt_head', 1)
    comRes.SetAttribute('dec_Sep', ',')
    comRes.SetAttribute('col_Sep', ';')
    comRes.SetAttribute('f_name', csvFileName)
    
def setupPlots(app : pf.Application, root : pf.DataObject):
  '''
  Setup the plots for the studycase.
  '''
  measurementBlock = root.SearchObject('measurements.ElmDsl') #type: ignore
  assert measurementBlock is not None

  board = app.GetFromStudyCase('SetDesktop')
  assert board is not None

  plots = board.GetContents('*.GrpPage',1)

  for p in plots:
    p.RemovePage() #type: ignore

  # Create pages
  plotPage = board.GetPage('Plot', 1,'GrpPage') #type: ignore
  pqPlot = plotPage.GetOrInsertCurvePlot('PQ') #type: ignore
  pqPlotDS = pqPlot.GetDataSeries() #type: ignore
  pqPlotDS.AddCurve(measurementBlock, 's:ppoc_pu') #type: ignore
  pqPlotDS.AddCurve(measurementBlock, 's:qpoc_pu') #type: ignore
  pqPlot.DoAutoScale() #type: ignore

  uPlot = plotPage.GetOrInsertCurvePlot('U') #type: ignore
  uPlotDS = uPlot.GetDataSeries() #type: ignore
  uPlotDS.AddCurve(measurementBlock, 's:pos_Vmag_pu') #type: ignore
  uPlotDS.AddCurve(measurementBlock, 's:neg_Vmag_pu') #type: ignore
  uPlot.DoAutoScale() #type: ignore

  iPlot = plotPage.GetOrInsertCurvePlot('I') #type: ignore
  iPlotDS = iPlot.GetDataSeries() #type: ignore
  iPlotDS.AddCurve(measurementBlock, 's:pos_Id_pu') #type: ignore
  iPlotDS.AddCurve(measurementBlock, 's:pos_Iq_pu') #type: ignore
  iPlotDS.AddCurve(measurementBlock, 's:neg_Id_pu') #type: ignore
  iPlotDS.AddCurve(measurementBlock, 's:neg_Iq_pu') #type: ignore
  iPlot.DoAutoScale() #type: ignore

  fPlot = plotPage.GetOrInsertCurvePlot('F') #type: ignore
  fPlotDS = fPlot.GetDataSeries() #type: ignore
  fPlotDS.AddCurve(measurementBlock, 's:f_hz') #type: ignore
  fPlot.DoAutoScale() #type: ignore

  app.WriteChangesToDb()

def addCustomSubscribers(thisScript : pf.DataObject, channels : List[si.Channel]) -> None:
  '''
  Add custom subscribers to the channels. For example, references applied as parameter events directly to control blocks.
  '''
  def script_GetExtnalObject(name : str) -> Optional[pf.DataObject]:
    retVal : List[Union[int, pf.DataObject, None]] = thisScript.GetExternalObject(name) #type: ignore
    assert isinstance(retVal, list)
    assert len(retVal) == 2
    assert isinstance(retVal[0], int)
    assert retVal[0] == 0
    assert isinstance(retVal[1], (pf.DataObject, type(None)))
    return retVal[1]
  
  def script_GetStr(name : str) -> str:
    retVal : List[Union[int, str]] = thisScript.GetInputParameterString(name) #type: ignore
    assert isinstance(retVal, list)
    assert len(retVal) == 2
    assert isinstance(retVal[0], int)
    assert retVal[0] == 0
    if isinstance(retVal[1], str):
      return retVal[1]
    else:
      return ''
  
  def script_GetDouble(name : str) -> Optional[float]:
    retVal : List[Union[int, float]] = thisScript.GetInputParameterDouble(name)
    assert isinstance(retVal, list)
    assert len(retVal) == 2
    assert isinstance(retVal[0], int)
    assert retVal[0] == 0
    assert isinstance(retVal[1], (float, type(None)))
    return retVal[1]
  
  def getChnlByName(name : str) -> si.Channel:
    for ch in channels:
      if ch.name == name:
        return ch
    raise RuntimeError(f'Channel {name} not found.')

  custConfStr = script_GetStr('sub_conf_str')

  def convertToConfStr(param : str, signal : str) -> str:
    sub_obj = script_GetExtnalObject(f'{param}_sub')
    sub_attrib = script_GetStr(f'{param}_sub_attrib')
    if sub_obj is not None and sub_attrib != '':
      sub_scale = script_GetDouble(f'{param}_sub_scale')
      assert isinstance(sub_scale, float)
      sub_signal = getChnlByName(f'{signal}')
      assert isinstance(sub_signal, si.Signal)
      return f'\{sub_obj.GetFullName()}:{sub_attrib}={signal}:S~{sub_scale} * x' #type: ignore
    return ''

  pref_conf = convertToConfStr('Pref', 'mtb_s_pref_pu')
  qref1_conf = convertToConfStr('Qref_q', 'mtb_s_qref_q_pu')
  qref2_conf = convertToConfStr('Qref_qu', 'mtb_s_qref_qu_pu')
  qref3_conf = convertToConfStr('Qref_pf', 'mtb_s_qref_pf_pu')
  custom1_conf = convertToConfStr('Custom1', 'mtb_s_1')
  custom2_conf = convertToConfStr('Custom2', 'mtb_s_2')
  custom3_conf = convertToConfStr('Custom3', 'mtb_s_3')

  configs = custConfStr.split(';') + [pref_conf, qref1_conf, qref2_conf, qref3_conf, custom1_conf, custom2_conf, custom3_conf]

  confFilterStr = r"^([^:*?=\",~|\n\r]+):((?:\w:)?\w+(?::\d+)?)=(\w+):(S|s|S0|s0|R|r|T|t|C|c)~(.*)"
  confFilter = re.compile(confFilterStr)

  for config in configs:
    confFilterMatch = confFilter.match(config)
    if confFilterMatch is not None:
      obj = confFilterMatch.group(1)
      attrib = confFilterMatch.group(2)
      sub = confFilterMatch.group(3)
      typ = confFilterMatch.group(4)
      lamb = confFilterMatch.group(5)

      chnl = getChnlByName(sub)
      if isinstance(chnl, si.Signal):
        if typ.lower() == 's' or typ.lower() == 'c':
          chnl.addPFsub_S(obj, attrib, lambda _,x : eval(lamb))
        elif typ.lower() == 's0':
          chnl.addPFsub_S0(obj, attrib, lambda _,x : eval(lamb)) #Not exactly safe
        elif typ.lower() == 'r':
          chnl.addPFsub_R(obj, attrib, lambda _,x : eval(lamb))
        elif typ.lower() == 't':
          chnl.addPFsub_T(obj, attrib, lambda _,x : eval(lamb))
      elif isinstance(chnl, si.Constant) or isinstance(chnl, si.PfObjRefer) or isinstance(chnl, si.String):
          chnl.addPFsub(obj, attrib)

def main():
  # 
  app, project, thisScript = connectPF()

  # Check if any studycase is active
  currentStudyCase = app.GetActiveStudyCase()

  if currentStudyCase is None:
    raise RuntimeError('Please activate a studycase.')

  studyTime : int = currentStudyCase.GetAttribute('iStudyTime')

  # Get and check for active grids
  networkData = app.GetProjectFolder('netdat')
  assert networkData is not None
  grids = networkData.GetContents('.ElmNet', 1)
  activeGrids = list(filter(lambda x : x.IsCalcRelevant(), grids))

  if len(activeGrids) == 0:
    raise RuntimeError('No active grids.')

  # Make project backup
  project.CreateVersion('PRE_MTB_{}'.format(datetime.now().strftime(r'%d%m%Y%H%M%S'))) #type: ignore

  resetProjectUnits(project)
  currentStudyCase.Consolidate() #type: ignore

  netFolder = app.GetProjectFolder('netmod')
  assert netFolder is not None
  varFolder = app.GetProjectFolder('scheme')

  # Create variation folder
  if varFolder is None:
    varFolder = netFolder.CreateObject('IntPrjfolder', 'Variations')
    varFolder.SetAttribute('iopt_typ', 'scheme')

  # Create studycase folder
  studyCaseFolder = app.GetProjectFolder('study')
  if studyCaseFolder is None:
    studyCaseFolder = project.CreateObject('IntPrjfolder', 'Study Cases')
    studyCaseFolder.SetAttribute('iopt_typ', 'study')

  # Create task automation
  taskAuto = studyCaseFolder.CreateObject('ComTasks')
  taskAuto.SetAttribute('iEnableParal', int(config.parallel))
  taskAuto.SetAttribute('parMethod', 0)
  (taskAuto.GetAttribute('parallelSetting')).SetAttribute('procTimeOut', 3600)

  # Find root object
  root = thisScript.GetParent()

  # Read and setup cases from sheet
  pfInterface = si.PFencapsulation(app, root)
  plantSettings, channels, cases, maxRank = cs.setup(casesheetPath = config.sheetPath, 
                                                     pscad = False,
                                                     pfEncapsulation = pfInterface)

  # Add user channel subscribers
  addCustomSubscribers(thisScript, channels)

  #Create export folder if it does not exist
  if not os.path.exists(config.exportPath):
    os.makedirs(config.exportPath)

  # Find initializer script object
  initScript = root.SearchObject('initializer_script.ComDpl')
  assert initScript is not None

  # List of created studycases for later activation
  studycases : List[pf.DataObject] = []

  currentStudyCase.Deactivate() #type: ignore

  app.EchoOff()
  for case in cases:
    if case.RMS:
      # Set-up studycase, variation and balance      
      caseName = '{}_{}'.format(str(case.rank).zfill(len(str(maxRank))), case.Name).replace('.', '')
      exportName = os.path.join(os.path.abspath(config.exportPath), f'{plantSettings.Projectname}_{case.rank}')
      newStudycase = studyCaseFolder.CreateObject('IntCase', caseName)
      studycases.append(newStudycase)
      newStudycase.Activate() #type: ignore     
      newStudycase.SetStudyTime(studyTime) #type: ignore

      # Activate the relevant networks
      for g in activeGrids:
          g.Activate() #type: ignore

      newVar = varFolder.CreateObject('IntScheme', caseName)
      newStage = newVar.CreateObject('IntSstage', caseName)
      newStage.SetAttribute('e:tAcTime', studyTime)
      newVar.Activate() #type: ignore
      newStage.Activate() #type: ignore

      si.applyToPowerfactory(channels, case.rank)

      initScript.Execute() #type: ignore

      ### WORKAROUND FOR QDSL FAILING WHEN IN MTB-GRID ###
      #TODO: REMOVE WHEN FIXED
      if config.QDSLcopyGrid != '':
        qdslInitializer = root.SearchObject('initializer_qdsl.ElmQdsl')
        assert qdslInitializer is not None
        for g in activeGrids:
          gridName = g.GetFullName() #type: ignore
          assert isinstance(gridName, str)
          if gridName.lower().endswith(f'{config.QDSLcopyGrid.lower()}.elmnet'):
            g.AddCopy(qdslInitializer) #type: ignore
          
        qdslInitializer.SetAttribute('outserv', 1) #type: ignore
      ### END WORKAROUND ###

      inc = app.GetFromStudyCase('ComInc')
      sim = app.GetFromStudyCase('ComSim')

      taskAuto.AppendStudyCase(newStudycase) #type: ignore
      taskAuto.AppendCommand(inc, -1) #type: ignore
      taskAuto.AppendCommand(sim, -1) #type: ignore
      setupResFiles(app, root)
      app.WriteChangesToDb()
      setupExport(app, exportName)
      app.WriteChangesToDb()
      newStudycase.Deactivate() #type: ignore
      app.WriteChangesToDb()

  app.EchoOn()
  
  taskAuto.Execute() #type: ignore
  
  for studycase in studycases:
    studycase.Activate() #type: ignore
    setupPlots(app, root)
    app.WriteChangesToDb()
    comRes = app.GetFromStudyCase('ComRes')
    assert comRes is not None
    comRes.Execute() #type: ignore
    app.WriteChangesToDb()
    studycase.Deactivate() #type: ignore
    app.WriteChangesToDb()

if __name__ == "__main__":
  main()