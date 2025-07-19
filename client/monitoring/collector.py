from monitoring.cpu import get_cpu_usage
from monitoring.memory import get_memory_usage
from monitoring.disk import get_disk_usage
from monitoring.network import get_network_stats
from monitoring.processes import get_process_info
from monitoring.sensors import get_temperatures

def collect_all_metrics():
    return {
        "cpu": get_cpu_usage(),
        "memory": get_memory_usage(),
        "disk": get_disk_usage(),
        "network": get_network_stats(),
        "processes": get_process_info(),
        "sensors": get_temperatures()
    }
