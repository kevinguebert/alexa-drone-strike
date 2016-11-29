import logging
import requests
import os
from datetime import datetime
from datetime import date
import dateutil.parser

from flask import Flask
from flask_ask import Ask, request, session, question, statement


app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

url = 'http://api.dronestre.am/data'

strikes = []

def days_between(d1, d2):
    print d1
    print d2
    return abs(d2 - d1).days

@ask.launch
def launch():
    response = requests.get(url).json()

    global strikes
    strikes = response["strike"]
    strikes_count = len(strikes)

    last_strike = strikes[strikes_count-1]

    today = datetime.utcnow()
    l_s_date = datetime.strptime(last_strike["date"], "%Y-%m-%dT%H:%M:%S.%fZ")

    since_last_strike = days_between(today, l_s_date)

    speech_text = "Welcome to Drone Strike. It has been " + str(since_last_strike) + " days since the last drone strike."
    return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)


@ask.intent('HowManyPeopleKilled')
def get_people_killed():
    response = requests.get(url).json()

    strikes = response["strike"]
    min_counter = 0
    max_counter = 0
    unknown_counter = 0
    for strike in strikes:
        try:
            min_counter += int(strike["deaths_min"])
        except ValueError:
            unknown_counter += 1
        try:
            max_counter += int(strike["deaths_max"])
        except ValueError:
            print('invalid max')

    if max_counter > 0:
        speech_text = "While we don't have accurate numbers, we can say that between " + str(min_counter) + " and " + str(max_counter) + " people have been killed. "
    else:
        speech_text = "There have been no recorded drone strikes in the timeframe."
    if unknown_counter > 0:
        speech_text += "Unfortunately there are " + str(unknown_counter) + " drone strikes that the number of deaths is unknown, so most likely the numbers are higher."

    return statement(speech_text).simple_card("HowManyPeopleKilled", speech_text)

@ask.intent('HowManyPeopleKilledThisYear')
def get_people_killed_this_year():
    response = requests.get(url).json()

    strikes = response["strike"]
    min_counter = 0
    max_counter = 0
    unknown_counter = 0
    now = datetime.now()
    for strike in strikes:
        strike_date = dateutil.parser.parse(strike["date"])
        if strike_date.year == now.year:
            try:
                min_counter += int(strike["deaths_min"])
            except ValueError:
                unknown_counter += 1
            try:
                max_counter += int(strike["deaths_max"])
            except ValueError:
                print('invalid max')


    if max_counter > 0:
        speech_text = "While we don't have accurate numbers, we can say that between " + str(min_counter) + " and " + str(max_counter) + " people have been killed this year. "
    else:
        speech_text = "There have been no recorded drone strikes in the timeframe."
    if unknown_counter > 0:
        speech_text += "Unfortunately there are " + str(unknown_counter) + " drone strikes that the number of deaths is unknown, so most likely the numbers are higher."

    return statement(speech_text).simple_card("HowManyPeopleKilledThisYear", speech_text)

@ask.intent('HowManyPeopleKilledThisMonth')
def get_people_killed_this_month():
    response = requests.get(url).json()

    strikes = response["strike"]
    min_counter = 0
    max_counter = 0
    unknown_counter = 0
    now = datetime.now()
    for strike in strikes:
        strike_date = dateutil.parser.parse(strike["date"])
        if strike_date.month == now.month and strike_date.year == now.year:
            try:
                min_counter += int(strike["deaths_min"])
            except ValueError:
                unknown_counter += 1
            try:
                max_counter += int(strike["deaths_max"])
            except ValueError:
                print('invalid max')


    if max_counter > 0:
        speech_text = "While we don't have accurate numbers, we can say that between " + str(min_counter) + " and " + str(max_counter) + " people have been killed this month. "
    else:
        speech_text = "There have been no recorded drone strikes in the timeframe."
    if unknown_counter > 0:
        speech_text += "Unfortunately there are " + str(unknown_counter) + " drone strikes that the number of deaths is unknown, so most likely the numbers are higher."

    return statement(speech_text).simple_card("HowManyPeopleKilledThisMonth", speech_text)

@ask.intent('HowManyDroneStrikes')
def get_all_drone_strikes():
    response = requests.get(url).json()

    strikes = response["strike"]
    if len(strikes) > 0:
        speech_text = "There have been " + str(len(strikes)) + " recorded drone strikes since 2003."
    else:
        speech_text = "There have been no recorded drone strikes in the timeframe."

    return statement(speech_text).simple_card("HowManyDroneStrikes", speech_text)

@ask.intent('HowManyDroneStrikesThisYear')
def get_drone_strikes_this_year():
    response = requests.get(url).json()

    strikes = response["strike"]
    strike_counter = 0
    now = datetime.now()
    for strike in strikes:
        strike_date = dateutil.parser.parse(strike["date"])
        if strike_date.year == now.year:
            strike_counter += 1


    if len(strikes) > 0:
        speech_text = "There have been " + str(strike_counter) + " recorded drone strikes this year."
    else:
        speech_text = "There have been no recorded drone strikes in the timeframe."

    return statement(speech_text).simple_card("HowManyDroneStrikesThisYear", speech_text)

@ask.intent('HowManyDroneStrikesThisMonth')
def get_drone_stikes_this_month():
    response = requests.get(url).json()

    strikes = response["strike"]
    strike_counter = 0
    now = datetime.now()
    for strike in strikes:
        strike_date = dateutil.parser.parse(strike["date"])
        if strike_date.year == now.year and strike_date.month == now.month:
            strike_counter += 1


    if len(strikes) > 0:
        speech_text = "There have been " + str(strike_counter) + " recorded drone strikes this month."
    else:
        speech_text = "There have been no recorded drone strikes in the timeframe."

    return statement(speech_text).simple_card("HowManyDroneStrikesThisMonth", speech_text)

@ask.intent('GetRecentDroneStrike')
def get_recent_drone_strike():
    strikes_count = len(strikes)
    last_strike = strikes[strikes_count-1]

    l_s_narrative = last_strike["narrative"]
    l_s_date = dateutil.parser.parse(last_strike["date"])
    l_s_location = last_strike["location"] + " in " + last_strike["country"]

    l_s_date_text = l_s_date.strftime("%A") + " " + l_s_date.strftime("%B") + " " + l_s_date.strftime("%d") + ", " + l_s_date.strftime("%Y")

    print "************"
    print "last strike: " + str(l_s_narrative)
    print "************"
    print "last strike date: " + l_s_date_text

    last_strike_output = "The last drone strike was on " + l_s_date_text + " in " + l_s_location + ". " + l_s_narrative
    return statement(last_strike_output).simple_card('GetRecentDroneStrike', last_strike_output)


@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'You can ask me information about drone strikes since 2003. Sample question are "What was the most recent drone strike", "How many drone strikes in the past year" or "How many people have died from drone strieks."'
    return question(speech_text).reprompt(speech_text).simple_card('HelpIntent', speech_text)


@ask.session_ended
def session_ended():
    return "", 200


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    # app.run(debug=True)
