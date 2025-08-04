from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid # generate GUIDs

db = SQLAlchemy()

# --- Models ---
class Item(db.Model):
    __tablename__ = 'items'
    guid = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<Item {self.name}>'
    
    def to_dict(self):
        return {
            'guid': self.guid,
            'name': self.name,
            'value': self.value,
            'created_date': self.created_date.isoformat()
        }