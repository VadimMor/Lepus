import psutil

def get_process_info(limit=10):
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_info']):
        try:
            info = proc.info
            info['memory_info'] = info['memory_info']._asdict()
            processes.append(info)
        except psutil.NoSuchProcess:
            continue
    # Вернем топ по CPU
    processes.sort(key=lambda p: p['cpu_percent'], reverse=True)
    return processes[:limit]
