import platform
import subprocess

def get_temperatures():
    system = platform.system()
    
    if system == "Linux":
        try:
            output = subprocess.check_output(['sensors'], encoding='utf-8')
            return {"sensors": output}
        except Exception as e:
            return {"error": str(e)}

    elif system == "Windows":
        return {"note": "Temperature monitoring not available on Windows in this version"}
    
    else:
        return {"note": f"No temperature support for platform {system}"}
