import sys
from subprocess import Popen, PIPE, TimeoutExpired

def executeUserCode(language,code):
    if language=="python":
        process = Popen([sys.executable,"-c", code], stdin = PIPE, stdout = PIPE, stderr = PIPE)
        try:
            output, error = process.communicate(timeout=5)
        except TimeoutExpired:
            process.kill()

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
        return output, error

    else:
        return None, None