from flask import Blueprint, jsonify, request
from ..models import Invoice, InvoiceItem, Product, db

bp = Blueprint('invoices', __name__)

@bp.route('/', methods=['GET'])
def get_invoices():
    invoices = Invoice.query.all()
    return jsonify([{"id": i.id, "customer_name": i.customer_name, "date_issued": i.date_issued, "total_amount": i.total_amount, "status": i.status} for i in invoices])

@bp.route('/', methods=['POST'])
def create_invoice():
    data = request.json
    invoice = Invoice(customer_name=data['customer_name'], total_amount=0, status='unpaid')
    db.session.add(invoice)
    db.session.flush()
    total_amount = 0
    for item in data['items']:
        product = Product.query.get(item['product_id'])
        if not product or product.stock < item['quantity']:
            return jsonify({"message": f"Insufficient stock for product {item['product_id']}"}), 400
        invoice_item = InvoiceItem(invoice_id=invoice.id, product_id=item['product_id'], quantity=item['quantity'], unit_price=product.price, total_price=product.price * item['quantity'])
        db.session.add(invoice_item)
        total_amount += invoice_item.total_price
        product.stock -= item['quantity']
    invoice.total_amount = total_amount
    db.session.commit()
    return jsonify({"message": "Invoice created successfully", "invoice_id": invoice.id}), 201
