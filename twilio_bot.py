import os
from flask import Flask, request
import requests
from dateutil import parser, tz
from twilio.twiml.messaging_response import MessagingResponse
import pyjokes

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
    body = request.values.get('Body', None).lower().strip()
    resp = MessagingResponse()

    if body == 'joke':
        output = pyjokes.get_joke(language="en", category="all")

    elif body == 'joke neutral':
        output = pyjokes.get_joke(language="en", category="neutral")

    elif body == 'joke twister':
        output = pyjokes.get_joke(language="en", category="twister")

    else:
        output = ('Sorry we could not understand your response. '
                  'You can respond with "joke" to get a random joke, '
                  '"joke neutral" to get a neutral joke, "joke twister" to '
                  'get the a tongue-twister joke.\n\nHave a great day!')
    resp.message(output)
    return str(resp)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
