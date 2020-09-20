import requests, json
from datetime import datetime, timedelta

from flask import Flask, jsonify, make_response


# Remap algorithm
# The function will iterate over a a list of repositories
# while assembling a dict of languages, each language has a sub-dict
# of the number of repositories and a list of those repositories names 
def remap(repos):

    langs = {} # algorithm output data

    if repos:
        for repo in repos:
            # for index readability
            lang = str(repo['language'])
            repo_name = str(repo['name'])

            # if language already exists in dict 'lang',
            # append repo to it's repositories and increment it's usage by 1
            if lang in langs.keys():
                langs[lang]['repositories'].append(repo_name)
                langs[lang]['usage'] += 1
            
            # else, reserve a sub-dict for the new language
            else:
                langs[lang] = {
                    'usage': 1,
                    'repositories': [repo_name]
                }
    return langs


# Initializing the flask app
app = Flask(__name__)

# setting the IP/site and port for the host of
# the flask microservice 
HOST, PORT = '127.0.0.1', 3000


# Microservice end-point worker
@app.route("/api/v1/trends/", methods=['GET'])
def trends():

    date = (datetime.now() - timedelta(30)).isoformat()  # The date of 30 days ago

    url = f"https://api.github.com/search/repositories?q=created:>{date}&sort=stars&order=desc"  # Target url

    res = requests.get(url) # Github's response

    payload = None

    # Handling the response from GitHub
    #
    # if the response is 'ok', call remap() to
    # assemble the output
    if res.status_code == 200:
        repos = res.json()['items']
        payload = remap(repos)
    #
    # else, forward Github's response as the microservice's output
    else:
        payload = {
            'requested_url': url,
            'response_status_code': res.status_code,
            'response_content': res.json()
        }

    # Customising the flask response to:
    # 1. Preserve the original order of dicts keys after jsonify.
    # 2. Pretty-printing the output json for user readability.
    msrv_res = make_response(json.dumps(payload, indent=4, sort_keys=False))
    msrv_res.mimetype = 'application/json'

    return msrv_res


# Main Thread starts here
if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)

