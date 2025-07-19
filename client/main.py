import time
import json
import requests
from monitoring.collector import collect_all_metrics
from ai.detect import detect_anomaly
from ai.train import flatten_metrics
from ai.retrain import retrain_on_single_point
from dotenv import load_dotenv
import os

load_dotenv()

DATA_PATH = "client/data/metrics.jsonl"
SERVER_URL = os.getenv("SERVER_URL")
if not SERVER_URL:
    raise RuntimeError("SERVER_URL не задан. Убедитесь, что .env файл существует и содержит SERVER_URL.")


def save_metrics(metrics, path=DATA_PATH):
    with open(path, "a", encoding="utf-8") as f:
        json.dump(metrics, f, ensure_ascii=False)
        f.write("\n")


def send_alert(metrics, mse):
    alert_data = {
        "metrics": metrics,
        "mse": mse,
        "status": "pending"
    }

    try:
        response = requests.post(SERVER_URL, json=alert_data)
        if response.status_code != 200:
            print(f"[ALERT FAILED] Status: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[ALERT ERROR] {e}")


def check_my_alerts():
    try:
        response = requests.get(SERVER_URL + "/mine")
        if response.status_code == 200:
            alerts = response.json()
            for alert in alerts:
                print(f"[ALERT STATUS] ID: {alert['id']} - Status: {alert['status']}")
                if alert["status"] == "rejected":
                    print("⚠️ Предыдущая аномалия была отклонена админом")
                    # тут можно адаптировать поведение
        else:
            print(f"[ERROR] Failed to fetch alerts: {response.status_code}")
    except Exception as e:
        print(f"[ERROR] While checking alerts: {e}")


def main():
    print("\n[Monitoring Started]\n")
    alert_check_counter = 0  # добавили счётчик

    try:
        next_tick = time.time()

        while True:
            start_time = time.time()

            metrics = collect_all_metrics()
            save_metrics(metrics)

            is_anomaly, score = detect_anomaly(metrics)

            if is_anomaly:
                send_alert(metrics, score)
            else:
                print(f"✅ Норма (MSE = {score:.5f})")
                if score < 1.5:
                    flat = flatten_metrics(metrics)
                    retrain_on_single_point(flat)

            alert_check_counter += 1
            if alert_check_counter >= 20:
                check_my_alerts()
                alert_check_counter = 0

            next_tick += 15
            sleep_duration = max(0, next_tick - time.time())
            time.sleep(sleep_duration)

    except KeyboardInterrupt:
        print("\n[Monitoring stopped by user]")



if __name__ == "__main__":
    main()