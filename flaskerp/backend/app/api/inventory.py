from flask import Blueprint, jsonify, request
from ..models import Inventory, Product, db

bp = Blueprint('inventory', __name__)

@bp.route('/', methods=['GET'])
def get_inventory():
    inventory = Inventory.query.all()
    return jsonify([{"id": i.id, "product_id": i.product_id, "quantity": i.quantity, "type": i.type, "date": i.date} for i in inventory])

@bp.route('/', methods=['POST'])
def update_inventory():
    data = request.json
    product = Product.query.get(data['product_id'])
    if not product:
        return jsonify({"message": "Product not found"}), 404
    if data['type'] == 'remove' and product.stock < data['quantity']:
        return jsonify({"message": "Insufficient stock"}), 400
    new_inventory = Inventory(product_id=data['product_id'], quantity=data['quantity'], type=data['type'])
    if data['type'] == 'add':
        product.stock += data['quantity']
    elif data['type'] == 'remove':
        product.stock -= data['quantity']
    elif data['type'] == 'adjust':
        product.stock = data['quantity']
    db.session.add(new_inventory)
    db.session.commit()
    return jsonify({"message": "Inventory updated successfully"}), 201
