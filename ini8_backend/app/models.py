from . import db
from datetime import datetime
import uuid

class Document(db.Model):
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = db.Column(db.String, nullable=False)
    file_path = db.Column(db.String, nullable=False)
    size = db.Column(db.Integer, nullable=False)
    patient_id = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
