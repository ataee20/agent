
#!/usr/bin/python3

# requirment phantomjs,ntpdate,requests
import time
import sys
import os
import json
import _thread
from toolInitializer import ToolInitializer
from fwutech_enum import FwutechEnum

from tools.executor import Executor
from tools.utils import Utils
from tools.webspeed import Webspeed
from tools.checkConfig import CheckConfigAndTools


utilsObject = Utils()
conf = utilsObject.readConf()
checkConfigAndTools = CheckConfigAndTools(conf)


# excute scenario periodically
def runScenario():

    # mount /home to readonly
    # utilsObject.runCmd(FwutechEnum.MOUNT_READONLY_CMD.value);

    MID = utilsObject.getMID()
    print(MID)
    primaryTasks = conf["scenarioModelModels"][0]["taskModels"]
    tasks = utilsObject.sortTasks(utilsObject.integrateTasks(
        primaryTasks, utilsObject.integratePingTask(utilsObject.get_pingTask(primaryTasks))))
    toolInitializer = ToolInitializer()
    while True:
        try:
            checkConfigAndTools.syncScenarioFromServer()
        except:
            pass
        try:
            checkConfigAndTools.checkUpgradeTools()
        except:
            pass
#        try:
#            checkConfigAndTools.checkWebPassword()
#        except:
#            pass
        # sync Date
        try:
            date_command = FwutechEnum.DATE_CMD.value%(os.path.dirname(os.path.abspath(__file__)).replace("\'", ""))
            shortName = "None"
            date_url = FwutechEnum.DATE_URL.value % (conf["serverIp"], str(conf["serverInfoPort"]), str(
                MID), utilsObject.getMidParent(), shortName, utilsObject.getInfo()["model"], utilsObject.getInfo()["type"])
            print(date_url)
            print(utilsObject.runCmd(date_command+" "+date_url))
        except:
            print(FwutechEnum.DATE_FAILD_MSG.value)
        reuslts = []
        for task in tasks:
            try:

                buildedObject = toolInitializer.build(
                    "tools." + task["toolName"], task["toolName"].capitalize(), task)
                taskResult = buildedObject.convetColonSytx(
                    buildedObject.executeTask())
                print(taskResult)
                temp_rs = json.loads(taskResult)
                if isinstance(temp_rs, list):
                    reuslts.extend(temp_rs)
                else:
                    reuslts.append(temp_rs)
            except:
                pass
        scenario_result = {"mid": MID, "scenarioResults": [
            {"scenarioName": conf["scenarioModelModels"][0]["scenarioName"], "resultOfScenarioTaskModels":reuslts}]}
        url =FwutechEnum.SEND_RESULT_URL.value%(conf["serverIp"],str(conf["serverInfoPort"]))
        utilsObject.send(url, utilsObject.prepareResult(scenario_result))
        time.sleep(60*conf["periodicalRunSenario"])


runScenario()
