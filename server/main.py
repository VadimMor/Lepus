from fastapi import FastAPI, Request, Depends
from sqlalchemy.orm import Session
from server.db.database import SessionLocal, engine
from server.db.models import User, Alert, Base
from pydantic import BaseModel
from typing import List
import json
from dotenv import load_dotenv


app = FastAPI()
load_dotenv()


class AlertIn(BaseModel):
    metrics: dict
    mse: float
    status: str


class AlertOut(AlertIn):
    id: str
    ip: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_or_create_user(db: Session, ip: str) -> User:
    user = db.query(User).filter_by(ip=ip).first()
    if not user:
        user = User(ip=ip)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


@app.on_event("startup")
def on_startup():
    print("[INFO] Creating tables in PostgreSQL if they don't exist...")
    Base.metadata.create_all(bind=engine)
    print("[INFO] Tables are ready.")


@app.post("/alerts", response_model=AlertOut)
def receive_alert(alert: AlertIn, request: Request, db: Session = Depends(get_db)):
    ip = request.client.host
    user = get_or_create_user(db, ip)

    new_alert = Alert(
        metrics=json.dumps(alert.metrics, ensure_ascii=False),
        mse=alert.mse,
        status=alert.status,
        user_id=user.id
    )

    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)

    return new_alert.to_dict()


@app.get("/alerts", response_model=List[AlertOut])
def get_alerts(db: Session = Depends(get_db)):
    alerts = db.query(Alert).all()
    return [a.to_dict() for a in alerts]


@app.post("/alerts/{alert_id}/confirm")
def confirm_alert(alert_id: str, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if alert:
        alert.status = "confirmed"
        db.commit()
    return {"status": "confirmed"}


@app.post("/alerts/{alert_id}/reject")
def reject_alert(alert_id: str, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if alert:
        alert.status = "rejected"
        db.commit()
    return {"status": "rejected"}

@app.get("/alerts/mine", response_model=List[AlertOut])
def get_my_alerts(request: Request, db: Session = Depends(get_db)):
    ip = request.client.host
    user = db.query(User).filter_by(ip=ip).first()
    if not user:
        return []
    alerts = db.query(Alert).filter_by(user_id=user.id).order_by(Alert.timestamp.desc()).limit(20).all()
    return [a.to_dict() for a in alerts]