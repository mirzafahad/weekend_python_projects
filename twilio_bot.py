import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import pyjokes


app = Flask(__name__)


@app.route('/', methods=["POST"])
def receive_sms():
    body = request.values.get("Body", None).lower().strip()
    resp = MessagingResponse()

    if body == "joke":
        output = pyjokes.get_joke(language="en", category="all")

    elif body == "joke neutral":
        output = pyjokes.get_joke(language="en", category="neutral")

    elif body == "joke chuck":
        output = pyjokes.get_joke(language="en", category="chuck")

    else:
        output = ("Sorry we could not understand your response. "
                  "You can respond with 'joke' to get a random joke, "
                  "'joke neutral' to get a neutral joke, 'joke twister' to "
                  "get the a tongue-twister joke.\n\nHave a great day!")
    resp.message(output)
    return str(resp)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
