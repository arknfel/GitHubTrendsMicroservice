# GitHubTrendsMicroservice
A simple micro-service implementation using python flask
(python 3.7.4)


# Functionality and Workflow

This microservice is a running flask application thats is served by a process on a particuler host machine. The application functions synchronously therefore to achieve concurrency, multiprocesses serving multiple instances of the microservice application, will be lunched. (for future developments, I will try to implement the service using multithreading or an async module)

The running flask app instance will wait for any http GET requests on the predefined end-point of the microservice "hostname:3200/api/v1/trends/", once a request is recieved, method trends() will be called by the flask application, method trends() works as follows:
  
  - Calculate the date of 30 day ago from now, format that date in an iso-format that is suitable for github's end-point, which is "ISO 8601",
  - Send a GET request to a predefined github url "https://api.github.com/search/repositories?q=created:>{date}&sort=stars&order=desc":
  ```python
    @app.route("/api/v1/trends/", methods=['GET'])
    def trends():

        date = (datetime.now() - timedelta(30)).isoformat()
        url = f"https://api.github.com/search/repositories?q=created:>{date}&sort=stars&order=desc"

        res = requests.get(url) # github's response
        repos = res.json()['items']  # a list of repositories in github's json response
  ```
The response will be a JSON object, our targeted element is the list of repositories, the list's key name is 'items', list 'items' holds repositores created in the last 30 days.
  - Iterate over 'items' while assembling the output python dict:
  ```python
  langs = {} # algorithm output data

  for repo in repos:
      # for index readability
      lang = repo['language']
      repo_name = repo['name']

      # for repo in repos if 'language' or 'name' is a none type object,
      # replace it with a string value 'None'
      if lang is None:
          lang = 'None'

      if repo_name is None:
          repo_name = 'None'

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
  ```
  - Jsonify the python dictionary:
  ```python
    msrv_res = make_response(json.dumps(langs,indent=4, sort_keys=False))
    msrv_res.mimetype = 'application/json'
  ```

Finally the microservice will respond to the get request made to it with the output json object as an http response.

# Future Developments

- To use docker which allows an easy deployment in a production environment.
- Concurrency, for a great performance using minimal resources while serving high traffic. 
