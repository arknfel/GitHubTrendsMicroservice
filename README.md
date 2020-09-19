# GitHubTrendsMicroservice
A simple micro-service implementation using python flask


# Functionality and Workflow

This microservice is a running flask application thats is served by a process on a particuler host machine. The application functions synchronously therefore to achieve concurrency, multiprocesses serving multiple instances of the microservice application, will be lunched. (for future developments, I will try to implement the service using multithreading or an async module)

The running flask app instance will wait for any http GET requests on the predefined end-point of the microservice "<hostname>:3200/api/v1/trends/".
once a request is recieved, method trends() will be executed by the flask application, method trends() works as follows:
  
  - Calculate the date of 30 day ago from now, format that date in iso-format that is suitable for github's end-point.
  - Send a get request to a predefined github url "https://api.github.com/search/repositories?q=created:>{date}&sort=stars&order=desc"
 
The response will be a JSON object, our targeted element is the list of repositories, the list's key name is 'items', list 'items' holds the most used repositores in the lastsub-objects
  - Iterate over 'items' while assembling the output python dict.
  - Jsonify the python dictionary.

Finally the microservice will respond to the get request made to it with the output json object as an http response. 
