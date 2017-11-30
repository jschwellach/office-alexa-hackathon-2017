import json
import os
import logging
import zipfile
import boto3
import time
import uuid
from boto3.dynamodb.conditions import Key, Attr
from boto3 import dynamodb
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

TABLE_NAME = os.environ['DYNAMODB_TABLE']

users = {
    "amzn1.ask.account.AFYHQ32LVQ54MEE6B667C4S6FW7NAXQQ6LVZ6SCW5FPSHVZ3IK2G5Y4CU2TW4GGAII7KC2EWB25HOOVBZUZ4SAPKGB6IQFTN3KEGLQCXEQ7DJMMVTDUPFC73JVIUNBHTZYSLTJ6DXNKRMBOCAD76I2GTUUWEV7OO46AGNOC5XBMUBRGSCOWZE6NZZYB5G5CH62DNCQJUHNA7MZA" : ["Ricardo","PST"],
    "amzn1.ask.account.AFYHQ32LVQ54MEE6B667C4S6FW7GCX6TB4F6YKF6Y76SAVLVKARIIKWLKZ4NGTZGEWAE2AGMLDCOM4ZZDCNZ42RWLREYV5LYXUS2D5QRHWC3GAFI44CG3HZYSVTQN5D2RKWRAU4SRXW7ABCSAEFRLTT6LPQP4LQPYER2LFWOEDSBJC5J7AUVJ24BJMZ75VSXSJFCUN557MRJXRQ" : ["Yanos","SGT"],
    "amzn1.ask.account.AF3VSAIDNLMEUAEPQS4Y47LLP3PL5XPWMOM22PJBUPSHMQGOLDOWL5K6KQWTHW4CSWNXU7AO2VJ7622YWWV6OGK7ISDTQP6LQJ32FF4OK5GVCMUPS34PATST4H444UGCBNATYLAFPBWK2CCAXZF3NHXFAZ4XLWQOARFWYY5D3KIYO4FYWTZUZMAJ53O3KQBUCJIL55TSC7IBN4I" : ["John","GMT"]
}


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Alexa My Team. " \
                    "Please tell me what you want to do by saying one of the following commands, " \
                    "CheckIn, CheckOut"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me what you want to do by saying one of the following commands, " \
                    "CheckIn, CheckOut"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills Kit sample. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_favorite_color_attributes(favorite_color):
    return {"favoriteColor": favorite_color}


def check_in_session(intent, session):
    """
    """
    user = users[session['user']['userId']][0]

    speech_output = "Welcome {}, I checked you in.".format(user)
    reprompt_text = ""

    card_title = intent['name']
    session_attributes = {}
    should_end_session = True

    table = boto3.resource('dynamodb').Table(TABLE_NAME)
    item = {
        'name' : user.lower(),
        'checkedIn' : 'true',
        'timezone' : users[session['user']['userId']][1],
        'start_time' : '9:00',
        'end_time' : '18:00'
    }
    table.put_item(Item=item)

#    if 'Color' in intent['slots']:
#        favorite_color = intent['slots']['Color']['value']
#        session_attributes = create_favorite_color_attributes(favorite_color)
#        speech_output = "I now know your favorite color is " + \
#                        favorite_color + \
#                        ". You can ask me your favorite color by saying, " \
#                        "what's my favorite color?"
#        reprompt_text = "You can ask me your favorite color by saying, " \
#                        "what's my favorite color?"
#    else:
#        speech_output = "I'm not sure what your favorite color is. " \
#                        "Please try again."
#        reprompt_text = "I'm not sure what your favorite color is. " \
#                        "You can tell me your favorite color by saying, " \
#                        "my favorite color is red."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def checkout_session(intent, session):
    user = users[session['user']['userId']][0]

    speech_output = "Welcome {}, I checked you out.".format(user)
    reprompt_text = ""

    card_title = intent['name']
    session_attributes = {}
    should_end_session = True

    table = boto3.resource('dynamodb').Table(TABLE_NAME)
    item = {
        'name' : user.lower(),
        'checkedIn' : 'false',
        'timezone' : users[session['user']['userId']][1]

    }
    table.put_item(Item=item)
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def meeting_request_session(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = True
    user = users[session['user']['userId']][0]
    table = boto3.resource('dynamodb').Table(TABLE_NAME)
    dynamodb_response = table.get_item(
                    Key={
                        'name': str(user.lower())
                    }
                )
    if ('Item' in dynamodb_response):
        if dynamodb_response['Item']['checkedIn'] != 'true':
            shouldEndSession = False
            speech_output = "You are not checked in. Please check in with saying check in first"
            reprompt_text = "You are not checked in. Please check in with saying check in first"
            return build_response(session_attributes, build_speechlet_response(
                card_title, speech_output, reprompt_text, should_end_session))
        else:
            if 'person' in intent['slots']:
                logger.info("searching for %s" % intent['slots']['person']['value'].lower())
                item = table.get_item(
                    Key={
                        'name': str(intent['slots']['person']['value'].lower())
                    }
                )
                if ('Item' not in item):
                    logger.error("couldn't find item")
                    item = {
                        'name': 'John',
                        'timezone' : 'GMT',
                        'start_time' : '9:00',
                        'end_time' : '18:00',
                        'checkedId' : 'true'
                    }
                    speech_output = "I can't find someone with the name {}. " \
                                    "Please try again. ".format(intent['slots']['person']['value'])
                    reprompt_text = "I can't find someone with the name {}. " \
                                    "Please try again. ".format(intent['slots']['person']['value'])
                    should_end_session = False
                    return build_response(session_attributes, build_speechlet_response(
                        card_title, speech_output, reprompt_text, should_end_session))
                logger.info("Person %s" % item)
                person = item['Item']
                if person['checkedIn'] == 'false':
                    speech_output = "I'm sorry {}, {} is asleep at the moment, would you like to try again in 5 hours when it's {} in {}'s timezone?".format(user,person['name'],person['start_time'],person['name'])
                    reprompt_text = ""
                    shouldEndSession = False
                else:
                    speech_output = "Congratulations {}, {} is available now, let me get him on the phone for you?".format(user,person['name'])
                    reprompt_text = ""
                    shouldEndSession = False
            else:
                speech_output = "I'm not sure with whom I should schedule the meeting. " \
                                "You can tell me the name of the person by saying, "\
                                "is person available for a meeting"
                reprompt_text = "I'm not sure with whom I should schedule the meeting. " \
                                "You can tell me the name of the person by saying, "\
                                "is person available for a meeting"
                should_end_session = False

            return build_response(session_attributes, build_speechlet_response(
                card_title, speech_output, reprompt_text, should_end_session))
    else:
        speech_output = "I'm sorry, I can't find the user in the database."
        reprompt_text = ""
        shouldEndSession = True
        return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, reprompt_text, should_end_session))


def get_color_from_session(intent, session):
    session_attributes = {}
    reprompt_text = None

    if session.get('attributes', {}) and "favoriteColor" in session.get('attributes', {}):
        favorite_color = session['attributes']['favoriteColor']
        speech_output = "Your favorite color is " + favorite_color + \
                        ". Goodbye."
        should_end_session = True
    else:
        speech_output = "I'm not sure what your favorite color is. " \
                        "You can say, my favorite color is red."
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    print("intent_name %s" % intent_name)
    # Dispatch to your skill's intent handlers
    if intent_name == "checkIn":
        return check_in_session(intent, session)
    elif intent_name == "checkOut":
        return checkout_session(intent, session)
    elif intent_name == "meetingRequest":
        return meeting_request_session(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        return get_welcome_response()


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

#    if (event['session']['application']['applicationId'] !=
#        "amzn1.ask.skill.42d881a4-20f3-4fe4-897b-3f063403a463"):
#
#        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
