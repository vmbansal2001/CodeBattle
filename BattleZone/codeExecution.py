from multiprocessing import Pipe
import sys, os
from subprocess import Popen, PIPE, TimeoutExpired
from time import time

def executeUserPythonCode(code):
    process = Popen([sys.executable,"-c", code], stdin = PIPE, stdout = PIPE, stderr = PIPE)
    try:
        output, error = process.communicate(timeout=5)
        output = output.decode("utf-8")
        output = output.replace("\r", "")
        error = error.decode("utf-8")
        error = error.replace("\r", "")

        # remove extra new line
        k = output.rfind("\n")
        new_string = output[:k] + "" + output[k+1:]
        output = new_string

        k = error.rfind("\n")
        new_string = error[:k] + "" + error[k+1:]
        error = new_string
    except TimeoutExpired as e:
        process.kill()
        output = ""
        error = "TimeOut: The code execution took very long time"
    return output, error

def executeUserJavaCode(code):
    with open("BattleZone\codeBuffers\Main.java",'w') as f:
        f.write("package BattleZone.codeBuffers;\n"+code)

    processes_list = ["javac", "BattleZone\codeBuffers\Main.java"]
    process = Popen(processes_list, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    process.wait()
    processes_list = ["java", "BattleZone.codeBuffers.Main"]
    process = Popen(processes_list, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    try:
        output, error = process.communicate(timeout=5)
        output = output.decode("utf-8")
        output = output.replace("\r", "")
        error = error.decode("utf-8")
        error = error.replace("\r", "")
        
        # remove extra new line
        k = output.rfind("\n")
        new_string = output[:k] + "" + output[k+1:]
        output = new_string

        k = error.rfind("\n")
        new_string = error[:k] + "" + error[k+1:]
        error = new_string
    except TimeoutExpired:
        process.kill()
        output = ""
        error = "TimeOut: The code execution took very long time"

    return output, error

def executeUserCPPCode(code):
    with open("BattleZone\codeBuffers\Main.cpp",'w') as f:
        f.write(code)


