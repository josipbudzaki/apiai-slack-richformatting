#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


# def processRequest(req):
#     if req.get("result").get("action") != "yahooWeatherForecast":
#         return {}
#     baseurl = "https://query.yahooapis.com/v1/public/yql?"
#     yql_query = makeYqlQuery(req)
#     if yql_query is None:
#         return {}
#     yql_url = baseurl + urllib.urlencode({'q': yql_query}) + "&format=json"
#     print(yql_url)

#     result = urllib.urlopen(yql_url).read()
#     print("yql result: ")
#     print(result)

#     data = json.loads(result)
#     res = makeWebhookResult(data)
#     return res


def processRequest(req):
    if req.get("result").get("action") != "getPurpose":
        return {}
    baseurl = "https://app.holaspirit.com//api/public/organizations/advertima/roles/administration-ber"

    result = urllib.urlopen(baseurl).read()

    data = json.loads(result)
    res = makeWebhookResult(data)
    return res


# def makeYqlQuery(req):
#     result = req.get("result")
#     parameters = result.get("parameters")
#     city = parameters.get("geo-city")
#     if city is None:
#         return None

#     return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"


def makeWebhookResult(data):
    purpose = data.get('purpose')
    if purpose is None:
        return {}

    # result = query.get('result')
    # if result is None:
    #     return {}

    # channel = result.get('channel')
    # if channel is None:
    #     return {}

    # item = channel.get('item')
    # location = channel.get('location')
    # units = channel.get('units')
    # if (location is None) or (item is None) or (units is None):
    #     return {}

    # condition = item.get('condition')
    # if condition is None:
    #     return {}

    # # print(json.dumps(item, indent=4))

    speech = "Purpose is" + data.get('purpose')

    print("Response:")
    print(speech)

    slack_message = {
        "text": speech,
        "attachments": [
            {
                "title": channel.get('title'),
                "title_link": channel.get('link'),
                "color": "#36a64f",

                "fields": [
                    {
                        "title": "Circles",
                        "value": "Circle " + data.get('name'),
                        "short": "false"
                    }
                ]
            }
        ]
    }

    print(json.dumps(slack_message))

    return {
        "speech": speech,
        "displayText": speech,
        "data": {"slack": slack_message},
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=False, port=port, host='0.0.0.0')
