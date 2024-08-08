from flask import Blueprint, jsonify
from ..models import Sale, Product, Invoice

bp = Blueprint('reports', __name__)

@bp.route('/sales', methods=['GET'])
def sales_report():
    sales = Sale.query.all()
    return jsonify([{"id": s.id, "product_id": s.product_id, "quantity": s.quantity, "total_price": s.total_price, "date_sold": s.date_sold} for s in sales])

@bp.route('/inventory', methods=['GET'])
def inventory_report():
    products = Product.query.all()
    return jsonify([{"id": p.id, "name": p.name, "stock": p.stock} for p in products])

@bp.route('/invoices', methods=['GET'])
def invoices_report():
    invoices = Invoice.query.all()
    return jsonify([{"id": i.id, "customer_name": i.customer_name, "total_amount": i.total_amount, "status": i.status, "date_issued": i.date_issued} for i in invoices])
