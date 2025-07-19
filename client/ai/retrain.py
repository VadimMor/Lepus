# client/ai/retrain.py
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from ai.model import AutoEncoder
import joblib
import pandas as pd

MODEL_PATH = "client/model/autoencoder.pth"
SCALER_PATH = "client/model/scaler.pkl"
FEATURE_NAMES = ['cpu_percent', 'cpu_freq', 'mem_percent', 'mem_used', 'mem_free',
                 'net_sent', 'net_recv', 'high_cpu_procs', 'disk_used_percent']

# Загружаем модель и scaler
model = AutoEncoder(input_dim=9)
model.load_state_dict(torch.load(MODEL_PATH))
model.train()

scaler = joblib.load(SCALER_PATH)

optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
loss_fn = nn.MSELoss()

def retrain_on_single_point(metrics_dict: dict, epochs=3):
    df = pd.DataFrame([metrics_dict], columns=FEATURE_NAMES)

    scaled = scaler.transform(df)
    tensor = torch.tensor(scaled, dtype=torch.float32)

    dataset = TensorDataset(tensor)
    loader = DataLoader(dataset, batch_size=1)

    for _ in range(epochs):
        for batch in loader:
            x = batch[0]
            optimizer.zero_grad()
            out = model(x)
            loss = loss_fn(out, x)
            loss.backward()
            optimizer.step()

    torch.save(model.state_dict(), MODEL_PATH)

