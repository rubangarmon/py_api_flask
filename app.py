from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid # generate GUIDs
import os # env variables

app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL', 'postgresql://dbitems_user:dbitems_password@localhost:5432/dbitems')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

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
    
# --- API Routes ---
@app.route('/')
def home():
    return "Welcome"

@app.before_request
def create_tables():
    db.create_all()

# Get all items
@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items])

# add a new item
@app.route('/items', methods=["POST"])
def add_item():
    data = request.get_json()
    if not data or not 'name' in data or not 'value' in data:
        return jsonify({
            'error': 'required fields (name, value)',
        }), 400
    
    try:
        new_item = Item(
            name=data['name'],
            value=data['value']
        )
        db.session.add(new_item)
        db.session.commit()
        return jsonify(new_item.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
# search by name endpoint
@app.route('/items/search', methods=['GET'])
def search_items():
    query_name = request.args.get('name')
    if not query_name:
        return jsonify({
            'error': 'required field (name)',
        }), 400
    
    items = Item.query.filter(Item.name.ilike(f'{query_name}')).all()
    return jsonify([item.to_dict() for item in items])

if __name__ == '__main__':
    app.run(debug=True)