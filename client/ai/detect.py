# detect.py
import torch
import torch.nn as nn
import pandas as pd
import joblib
from ai.model import AutoEncoder
from ai.train import flatten_metrics

# Грузим scaler и модель один раз при импорте
scaler = joblib.load("client/model/scaler.pkl")
model = AutoEncoder(input_dim=9)  # 9 признаков в flatten_metrics
model.load_state_dict(torch.load("client/model/autoencoder.pth"))
model.eval()

def detect_anomaly(metrics, threshold=1.0):
    df = pd.DataFrame([flatten_metrics(metrics)])
    X_scaled = scaler.transform(df)
    X_tensor = torch.tensor(X_scaled, dtype=torch.float32)

    with torch.no_grad():
        reconstructed = model(X_tensor)
        mse = nn.functional.mse_loss(reconstructed, X_tensor).item()

    return mse > threshold, mse
