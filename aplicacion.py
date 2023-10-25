from fastapi import FastAPI, HTTPException
import subprocess

app = FastAPI()

@app.post("/execute_command/")
def execute_command(command: str):
    baseString=f"echo '{command}' | festival --language spanish --tts"

    try:
        # Execute the command in the shell using subprocess
        result = subprocess.check_output(baseString, shell=True, text=True)
        return {"output": result}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=400, detail=str(e))