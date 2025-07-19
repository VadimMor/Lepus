import psutil

def get_network_stats():
    net_io = psutil.net_io_counters(pernic=True)
    return {iface: stats._asdict() for iface, stats in net_io.items()}
