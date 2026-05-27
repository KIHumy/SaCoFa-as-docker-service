import requests
import time
import json
import socket
import callPrivatize

algoName = "SaCoFa"
algoId = socket.gethostname()
algoIdentity = {"identification":{"name":algoName, "id":algoId}}

def serverHealthcheck():
    while True:
        try:
            healthcheck = requests.get("http://cliandanalyzer:8000/healthcheck")
            if healthcheck.status_code == 200:
                return
        except:
            time.sleep(5)

def mainEntrypoint():
    serverHealthcheck()
    stayActive = True
    while stayActive:
        instructionRequestAnswer = requests.post("http://cliandanalyzer:8000/task", json={"name":algoName, "id":algoId})
        if instructionRequestAnswer.json() != {"instruction":"no_instruction"}:
            print("Received a new instruction.", flush=True)
            print(instructionRequestAnswer.json(), flush=True)
            startInstructionHandler(instructionRequestAnswer.json())
        time.sleep(5)

def collectRequirementsForAlgo():
    P = {"name":"P", "lowerBound":"3", "upperBound":"3", "type":"int"}
    P_smart = {"name":"P_smart", "lowerBound":"2", "upperBound":"2", "type":"int"}
    N = {"name":"N", "lowerBound":"10", "upperBound":"10", "type":"int"}
    #basePath = {"name":"basePath", "value":"someString", "description":"This tring should be a file path to an event log.", "type":"string"}
    #logName = {"name":"logName", "value":"someString", "description":"This string should be the name of the event log.", "type":"string"}
    #inPath = {"name":"inPath", "value":"someString", "description":"This string represents the path to the event log file.", "type":"string"}
    epsRange = {"name":"epsRange", "lowerBound":"1.0", "upperBound":"1.0", "type":"float"} #could be list[float] instead
    tries = {"name":"tries", "lowerBound":"10", "upperBound":"10", "type":"int"} #could be literal instead
    algoVariables = [P, P_smart, N, epsRange, tries]
    return {**algoIdentity, "inputFormat":"xes", "outputStructure":"eventLog", "requirements":algoVariables}

def startInstructionHandler(instruction):
    print("Entered the instruction block.", flush=True)
    if instruction["instruction"] == "start_n_test":
        print("Accessed n_test function.", flush=True)
        requests.post("http://cliandanalyzer:8000/result/status", json={**algoIdentity, "instructionId":instruction["instructionId"], "status":"network_stable"})
    if instruction == {"instruction":"send_requirements"}:
        print("Accessed requirements function.", flush=True)
        jsonRequirements = collectRequirementsForAlgo()
        requests.post("http://cliandanalyzer:8000/myRequirements", json=jsonRequirements)
    if instruction["instruction"] == "comparison":
        print("Accessed Template function.", flush=True)
        algoDictionary = instruction.get("payload")
        P = 3
        P_smart = 2
        N = 10
        #basePath = "someString"
        logName = "someString"
        #inPath = "someString"
        epsRange = 1.0
        tries = 10
        for inputValues in algoDictionary["inputParameters"]:
            if inputValues["name"] == "P":
                P = inputValues["value"]
            if inputValues["name"] == "P_smart":
                P_smart = inputValues["value"]
            if inputValues["name"] == "N":
                N = inputValues["value"]
            #if inputValues["name"] == "basePath":
            #    basePath = inputValues["value"]
            if inputValues["name"] == "logName":
                logName = inputValues["value"]
            #if inputValues["name"] == "inPath":
            #    inPath = inputValues["value"]
            if inputValues["name"] == "epsRange":
                epsRange = inputValues["value"]
            if inputValues["name"] == "tries":
                tries = inputValues["value"]
        callPrivatize.executeSacofa(P, P_smart, N, logName, epsRange, tries, instruction["instructionId"])
        print("Sending the result of the template function to the server.", flush= True)
        requests.post("http://cliandanalyzer:8000/result/status", json={**algoIdentity, "instructionId":instruction["instructionId"], "status":"finished_privacy_enhancing_algorithm"})
    return

if __name__ == "__main__":
    mainEntrypoint()
    #executeSacofa(): from callPrivatize.py
