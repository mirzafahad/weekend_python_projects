import requests

url = 'http://127.0.0.1:5000/'
data = {
    'duedate': 'September 1, 3200',
    'from_addr': {
        'addr1': 'Hamilton, Mars',
        'addr2': 'Saturn, LP 12345',
        'company_name': 'To The Moon and Back'
    },
    'invoice_number': 156,
    'items': [
        {
            'charge': 500.0,
            'title': 'Unicorn Castle'
        },
        {
            'charge': 85.0,
            'title': 'Mini Condo'
        },
        {
            'charge': 10.0,
            'title': 'Total Component Price'
        }
    ],
    'to_addr': {
        'company_name': 'hula hoop',
        'person_email': 'john@example.com',
        'person_name': 'Fahad Mirza'
    }
}

html = requests.post(url, json=data)
with open('invoice_test.pdf', 'wb') as f:
    f.write(html.content)
