import os
import pdfkit
from datetime import datetime
from flask import Flask, render_template, send_file, request
import io


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    posted_data = request.get_json() or {}
    today = datetime.today().strftime("%B %d, %Y")
    invoice_number = 666
    default_data = {
        'duedate': 'August 1, 2222',
        'from_addr': {
            'addr1': '54321 Icy Road',
            'addr2': 'Mount Everest, Nepal 12345',
            'company_name': '7-Eleven'
        },
        'invoice_number': 123,
        'items': [
            {
                'charge': 300.0,
                'title': 'Website Design'
            },
            {
                'charge': 750.0,
                'title': 'Circuit Design'
            },
            {
                'charge': 100.0,
                'title': 'PCB Manufacturing'
            }
        ],
        'to_addr': {
            'company_name': 'Hitman47',
            'person_email': 'john@doe.com',
            'person_name': 'John Doe'
        }
    }

    duedate = posted_data.get('duedate', default_data['duedate'])
    from_addr = posted_data.get('from_addr', default_data['from_addr'])
    to_addr = posted_data.get('to_addr', default_data['to_addr'])
    invoice_number = posted_data.get('invoice_number', default_data['invoice_number'])
    items = posted_data.get('items', default_data['items'])

    total = sum([i['charge'] for i in items])

    rendered = render_template('invoice.html',
                               date=today,
                               from_addr=from_addr,
                               to_addr=to_addr,
                               items=items,
                               total=total,
                               invoice_number=invoice_number,
                               duedate=duedate)

    with open('invoice.html', 'w') as html_file:
        html_file.write(rendered)
        html_file.flush()
        pdf_binary = pdfkit.from_file("invoice.html", b'')

    if os.path.exists("invoice.html"):
        os.remove("invoice.html")

    return send_file(io.BytesIO(pdf_binary), download_name='invoice.pdf')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
