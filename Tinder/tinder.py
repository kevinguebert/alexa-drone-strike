import logging
import requests
import os
from datetime import datetime
from datetime import date
import dateutil.parser

from flask import Flask
from flask_ask import Ask, request, session, question, statement
import pynder

# FBTOKEN = "EAAGm0PX4ZCpsBAFEqKmMSlnDVm7NYA42KeP7kuqAPA4AZB33JPbBqPN7ULwzSGnU64MSbmJZBwkPMCiu2z4txTfMZBZB4DGCQPHKamLRPdhzMCzcyrbD517C8ZAeR7Ooc3ezrhZAzzkbS7pp0UgiOnze5TkdqWQpzj76EKStoVWabM0JsDBrf22VjS5XsjYZC9BH8L84WHJWIAy8lMZCRhK8sXz31dGDne1iIFHcuiYECnwZDZD"
# FBID = "6369662488793022844"

FBTOKEN = "EAAGm0PX4ZCpsBAFEqKmMSlnDVm7NYA42KeP7kuqAPA4AZB33JPbBqPN7ULwzSGnU64MSbmJZBwkPMCiu2z4txTfMZBZB4DGCQPHKamLRPdhzMCzcyrbD517C8ZAeR7Ooc3ezrhZAzzkbS7pp0UgiOnze5TkdqWQpzj76EKStoVWabM0JsDBrf22VjS5XsjYZC9BH8L84WHJWIAy8lMZCRhK8sXz31dGDne1iIFHcuiYECnwZDZD"
FBID = "6369966487696698529"

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)
session = pynder.Session(FBID, FBTOKEN)

@ask.launch
def launch():

    return question("hello and welcome").simple_card('HelloWorld', "speech_text")


@ask.intent('GetClosestBiography')
def get_closest_biography():
    users = session.nearby_users()
    user = users[0]

    print(user.age)
    speech_text = "Name: " + user.name.encode('ascii', 'ignore').decode('ascii') + ", Age: " + str(user.age) + ", Biography: " + user.bio.encode('ascii', 'ignore').decode('ascii')

    return question(speech_text).simple_card("GetClosestBiography", speech_text)

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
