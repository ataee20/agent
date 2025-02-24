import requests
from fwutech_enum import FwutechEnum


class ServerUtils():

    def __init__(self):
        pass

    def sendDataToServer(self, serverAddr, results):
        status = False
        try:

            headers = {'Content-type': 'application/json',
                       'Accept': 'text/plain'}
            r = requests.post(serverAddr, data=json.dumps(
                results), headers=headers)
            status = True
            print(FwutechEnum.RESULT_SEND_SUCCESS_MSG.value)
        except:
            print(FwutechEnum.RESULT_SEND_FAILD_MSG.value)

    def sendToServerGet(link_param):

        r1 = requests.get(link_param)
