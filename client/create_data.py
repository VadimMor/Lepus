import pandas as pd
import numpy as np
import joblib
import torch
import torch.nn as nn
from sklearn.preprocessing import StandardScaler
from ai.model import AutoEncoder
from ai.train import flatten_metrics

def generate_baseline_dataset(num_samples=2000):
    data = {
        "cpu_percent": np.random.uniform(1, 50, num_samples),        # CPU загрузка 1-50% (ранее 1-30)
        "cpu_freq": np.random.uniform(1500, 3000, num_samples),      # Частота 1.5-3.0 GHz (без изменений)
        "mem_percent": np.random.uniform(20, 70, num_samples),       # Память 20-70% (без изменений)
        "mem_used": np.random.uniform(5e9, 35e9, num_samples),       # Используемая память 5-35 ГБ (ранее 5-20)
        "mem_free": np.random.uniform(5e9, 40e9, num_samples),       # Свободная память 5-40 ГБ (расширено вниз)
        "net_sent": np.random.uniform(0, 2e10, num_samples),         # bytes sent расширен до 20 млрд (ранее 1e7)
        "net_recv": np.random.uniform(0, 3e10, num_samples),         # bytes recv расширен до 30 млрд (ранее 5e7)
        "high_cpu_procs": np.random.randint(0, 6, num_samples),      # Процессов с CPU >50% от 0 до 5 (ранее 0-3)
        "disk_used_percent": np.random.uniform(5, 50, num_samples)   # Занятость диска 5-50% (без изменений)
    }
    return pd.DataFrame(data)


def train_baseline_model():
    df = generate_baseline_dataset()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df)
    joblib.dump(scaler, "client/model/scaler.pkl")

    X_tensor = torch.tensor(X_scaled, dtype=torch.float32)
    model = AutoEncoder(X_tensor.shape[1])
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.MSELoss()

    model.train()
    for epoch in range(200): 
        output = model(X_tensor)
        loss = criterion(output, X_tensor)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        if epoch % 20 == 0:
            print(f"Epoch {epoch} - Loss: {loss.item():.6f}")

    torch.save(model.state_dict(), "client/model/autoencoder.pth")
    print("Baseline autoencoder trained and saved.")

if __name__ == "__main__":
    train_baseline_model()
