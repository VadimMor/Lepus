import psutil

def get_cpu_usage():
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "cpu_count": psutil.cpu_count(logical=True),
        "cpu_freq": psutil.cpu_freq()._asdict()
    }
