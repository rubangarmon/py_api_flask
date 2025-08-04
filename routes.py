from flask import Blueprint, request, jsonify
from models import db, Item

bp = Blueprint('api', __name__)

@bp.route('/')
def home():
    return "Welcome"

# Get all items
@bp.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items])

# add a new item
@bp.route('/items', methods=["POST"])
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
@bp.route('/items/search', methods=['GET'])
def search_items():
    query_name = request.args.get('name')
    if not query_name:
        return jsonify({
            'error': 'required field (name)',
        }), 400
    
    items = Item.query.filter(Item.name.ilike(f'{query_name}')).all()
    return jsonify([item.to_dict() for item in items])