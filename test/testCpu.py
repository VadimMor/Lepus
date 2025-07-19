import multiprocessing
import time

def cpu_stress_worker():
    x = 0
    while True:
        x = (x + 1) % 1000000

def stress_cpu(duration_seconds=10):
    num_processes = multiprocessing.cpu_count()
    print(f"Нагрузка CPU на {num_processes} ядрах в течение {duration_seconds} секунд...")

    processes = []
    for _ in range(num_processes):
        p = multiprocessing.Process(target=cpu_stress_worker)
        p.start()
        processes.append(p)

    time.sleep(duration_seconds)

    for p in processes:
        p.terminate()
        p.join()

    print("Нагрузка завершена.")

if __name__ == "__main__":
    stress_cpu()
