import requests, json
from datetime import datetime, timedelta

from flask import Flask, jsonify, make_response


# Initializing the flask app
app = Flask(__name__)

# Setting the IP/site and port for the host of
# the flask microservice 
HOST, PORT = '0.0.0.0', 3000

# Microservice worker
@app.route("/api/v1/trends/", methods=['GET'])
def trends():

    date = (datetime.now() - timedelta(30)).isoformat()

    url = f"https://api.github.com/search/repositories?q=created:>{date}&sort=stars&order=desc"

    res = requests.get(url) # github's response

    # Handles and returns non-ok responses from github
    if res.status_code != 200:

        payload = {
            'requested_url': url,
            'response_status_code': res.status_code,
            'resonse_content': res.json()
        }

        payload = json.dumps(payload, indent=4, sort_keys=False)
        msrv_res = make_response(payload)
        msrv_res.mimetype = 'application/json'
        return msrv_res

    repos = res.json()['items']  # a list of repositories in github's json response

    # if there are available items returned from the github request,
    # proceed to the remapping algorithm, else, notate that no data were found.
    if len(repos) > 0:

        # Remapping algorithm

        langs = {} # algorithm output data

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

        # minimal tweaks to flask's default response that holds
        # the JSON object of dict 'langs'
        msrv_res = make_response(json.dumps(langs,indent=4, sort_keys=False))
        msrv_res.mimetype = 'application/json'
        
        # returns a valid JSON object
        return msrv_res
    
    # len(repos) == 0 (if repos had no elements)
    # returns a JSON object of the url and a warning message
    else:
        return jsonify(url=url, error="No repositories were returned")


# Main Thread starts here
if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
