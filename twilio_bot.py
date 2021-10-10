import os
from flask import Flask, request
import requests
from dateutil import parser, tz
from twilio.twiml.messaging_response import MessagingResponse

urls = {
    'group': 'https://worldcup.sfg.io/teams/group_results',
    'country': 'https://worldcup.sfg.io/matches/country?fifa_code=',
    'today': 'https://worldcup.sfg.io/matches/today',
    'tomorrow': 'https://worldcup.sfg.io/matches/tomorrow'
}

countries = [
    'KOR', 'PAN', 'MEX', 'ENG', 'COL', 'JPN', 'POL', 'SEN',
    'RUS', 'EGY', 'POR', 'MAR', 'URU', 'KSA', 'IRN', 'ESP',
    'DEN', 'AUS', 'FRA', 'PER', 'ARG', 'CRO', 'BRA', 'CRC',
    'NGA', 'ISL', 'SRB', 'SUI', 'BEL', 'TUN', 'GER', 'SWE'
]

app = Flask(__name__)
to_zone = tz.gettz('America/Dallas')


@app.route('/', methods=['POST'])
def receive_sms():
    body = request.values.get('Body', None)
    resp = MessagingResponse()
    resp.message(body or 'Hello World!')
    return str(resp)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
