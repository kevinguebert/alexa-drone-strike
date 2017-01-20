from flask import Flask
from flask_ask import Ask, request, session, question, statement

import requests
import dateutil.parser
from datetime import date

app = Flask(__name__)
ask = Ask(app, "/")

url = 'http://api.dronestre.am/data'

@ask.launch
def launch():
    speech_text = "Hello, welcome to Drone Strike"
    return statement(speech_text).simple_card('Welcome', speech_text)

@ask.intent('GetRecentDroneStrike')
def get_recent_drone_strike():
    response = requests.get(url).json()

    strikes = response["strike"]
    strikes_count = len(strikes)
    last_strike = strikes[strikes_count-1]

    l_s_narrative = last_strike["narrative"]
    l_s_date = dateutil.parser.parse(last_strike["date"])
    l_s_location = last_strike["location"] + " in " + last_strike["country"]

    l_s_date_text = l_s_date.strftime("%A") + " " + l_s_date.strftime("%B") + " " + l_s_date.strftime("%d") + ", " + l_s_date.strftime("%Y")

    last_strike_output = "The last drone strike was on " + l_s_date_text + " in " + l_s_location + ". " + l_s_narrative
    return statement(last_strike_output).simple_card('GetRecentDroneStrike', last_strike_output)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = 5000
    app.run(host='0.0.0.0', port=port)
