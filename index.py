import asyncio
from flask import Flask, request, jsonify, render_template
import os
import dialogflow
import requests
import json
import pusher
from jobsFind import findJob

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(silent=True)
    params=[data['queryResult']['outputContexts'][0]['parameters']['jobs'],data['queryResult']['outputContexts'][0]['parameters']['location']['city'],data['queryResult']['outputContexts'][0]['parameters']['skills']]
    jobs=findJob(params[0],params[1],params[2])
    if len(jobs)==0:
        reply = {
            "fulfillmentText": "Sorry I can't find suitable job for you",
        }
    else:
        reply = {
                "fulfillmentMessages": [
                    {
                    "payload": {
                    "facebook": {
                        "attachment":{
                              "type":"template",
                              "payload":{
                                "template_type": "generic",
                                "elements":[
                                   {
                                    "title": str(jobs[0][0]),
                                    "image_url":"https://securemedia.newjobs.com/global/img/magnifying-glass-circle.jpg",
                                    "subtitle":str(jobs[0][4]),
                                    "buttons":[
                                      {
                                        "type":"web_url",
                                        "url": str(jobs[0][5]),
                                        "title":"View job"
                                      }
                                    ]
                                  },
                                    {
                                        "title": str(jobs[1][0]),
                                        "image_url": "https://securemedia.newjobs.com/global/img/magnifying-glass-circle.jpg",
                                        "subtitle": str(jobs[1][4]),
                                        "buttons": [
                                            {
                                                "type": "web_url",
                                                "url": str(jobs[1][5]),
                                                "title": "View job"
                                            }
                                        ]
                                    },
                                ]
                              }
                        }
                    }},
                    "platform": "FACEBOOK",
                    "sendAsMessage": True,
                },
                {
                    "payload":{
                        "facebook":{
                            "text": "Do you want more?",
                            "quick_replies": [
                                {
                                    "content_type": "text",
                                    "title": "Yes",
                                    "payload": "<POSTBACK_PAYLOAD>",
                                }, {
                                    "content_type": "text",
                                    "title": "No",
                                    "payload": "<POSTBACK_PAYLOAD>",
                                }
                            ]
                        }
                    },
                    "platform": "FACEBOOK",
                    "sendAsMessage": True,
                }
                ]
        }

    return jsonify(reply)
    # if data['queryResult']['queryText'] == 'yes':
    #     reply = {
    #         "fulfillmentText": "Ok. Tickets booked successfully.",
    #     }
    #     return jsonify(reply)
    #
    # elif data['queryResult']['queryText'] == 'no':
    #     reply = {
    #         "fulfillmentText": "Ok. Booking cancelled.",
    #     }
    #     return jsonify(reply)
@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    fulfillment_text = detect_intent_texts(project_id, "unique", message, 'en')
    response_text = { "message":  fulfillment_text }
    return jsonify(response_text)

#dectect intent
def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    if text:
        text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)
        return response.query_result.fulfillment_text
# run Flask app
if __name__ == "__main__":
    app.run()
