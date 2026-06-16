from flask import Blueprint, jsonify
from models.invoice import Invoice
from config import Config
from reportlab.pdfgen import canvas

import smtplib
from email.message import EmailMessage

email_bp = Blueprint("email_bp", __name__)


@email_bp.route("/invoices/<int:invoice_id>/email/<email>", methods=["POST"])
def send_invoice_email(invoice_id, email):

    invoice = Invoice.query.get(invoice_id)

    if not invoice:
        return jsonify({
            "message": "Invoice not found"
        }), 404

    filename = f"invoice_{invoice.id}.pdf"

    c = canvas.Canvas(filename)

    c.drawString(100, 800, "VendorBridge ERP Invoice")
    c.drawString(100, 770, f"Invoice Number: {invoice.invoice_number}")
    c.drawString(100, 740, f"PO ID: {invoice.po_id}")
    c.drawString(100, 710, f"Amount: {invoice.amount}")
    c.drawString(100, 680, f"Tax: {invoice.tax}%")
    c.drawString(100, 650, f"Total Amount: {invoice.total_amount}")

    c.save()

    msg = EmailMessage()

    msg["Subject"] = f"Invoice {invoice.invoice_number}"
    msg["From"] = Config.EMAIL_USER
    msg["To"] = email

    msg.set_content(
        f"Please find attached invoice {invoice.invoice_number}"
    )

    with open(filename, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="pdf",
            filename=filename
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(
            Config.EMAIL_USER,
            Config.EMAIL_PASSWORD
        )
        smtp.send_message(msg)

    return jsonify({
        "message": "Invoice email sent successfully"
    })