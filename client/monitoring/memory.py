import psutil

def get_memory_usage():
    vmem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    return {
        "virtual_memory": vmem._asdict(),
        "swap_memory": swap._asdict()
    }
