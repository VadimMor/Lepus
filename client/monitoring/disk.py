import psutil

def get_disk_usage():
    return {
        "partitions": [p._asdict() for p in psutil.disk_partitions()],
        "usage": {p.mountpoint: psutil.disk_usage(p.mountpoint)._asdict()
                  for p in psutil.disk_partitions()}
    }
