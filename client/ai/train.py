# lepus/client/ai/train.py
import pandas as pd
import json
import torch
import torch.nn as nn
from sklearn.preprocessing import StandardScaler
import joblib
from ai.model import AutoEncoder


def flatten_metrics(metrics):
    flat = {
        "cpu_percent": metrics["cpu"]["cpu_percent"],
        "cpu_freq": metrics["cpu"]["cpu_freq"]["current"],
        "mem_percent": metrics["memory"]["virtual_memory"]["percent"],
        "mem_used": metrics["memory"]["virtual_memory"]["used"],
        "mem_free": metrics["memory"]["virtual_memory"]["free"],
        "net_sent": metrics["network"].get("Беспроводная сеть", {}).get("bytes_sent", 0),
        "net_recv": metrics["network"].get("Беспроводная сеть", {}).get("bytes_recv", 0),
        "high_cpu_procs": sum(1 for p in metrics["processes"] if p["cpu_percent"] > 50)
    }
    disk_usage = metrics["disk"]["usage"]
    total_used = sum(d.get("used", 0) for d in disk_usage.values())
    total_size = sum(d.get("total", 1) for d in disk_usage.values())
    flat["disk_used_percent"] = (total_used / total_size) * 100 if total_size else 0
    return flat


def load_dataset(path="client/data/metrics.jsonl"):
    data = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            data.append(flatten_metrics(record))
    return pd.DataFrame(data)


def train_and_save_model():
    df = load_dataset()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df)
    joblib.dump(scaler, "client/model/scaler.pkl")

    X_tensor = torch.tensor(X_scaled, dtype=torch.float32)
    model = AutoEncoder(X_tensor.shape[1])
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.MSELoss()

    model.train()
    for epoch in range(100):
        output = model(X_tensor)
        loss = criterion(output, X_tensor)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        if epoch % 10 == 0:
            print(f"Epoch {epoch} - Loss: {loss.item():.6f}")

    torch.save(model.state_dict(), "client/model/autoencoder.pth")
    print("Autoencoder trained and saved.")