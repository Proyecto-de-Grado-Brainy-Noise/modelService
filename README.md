# CNN model Service 👾
Microservice made with Django, it has the CNN model integreated and also helps to received the requests for predictions, and then submits the results to the mongo database **predictionsResultsDB**.


## Runnning
First, you need to pull the docker-compose repository, over there you can follow the steps to organize the project to run it successfully, here is the link to the repo:

[Docker-compose file repo](https://github.com/Proyecto-de-Grado-Brainy-Noise/docker-compose/tree/develop)

Just to let you know, the port to which you can send request is the port:

```sh
9004
```

Once the complete project is deployed the IP address will change and probably it won't be localhost, so, you just have to change the localhost in the endpoints with the IP you need. 🧐

### Endpoints
| Request Type | Endpoints |Description|Params|Body|
| ------ | ------ | ------ | ------ | ------ |
| POST | http://localhost:9004/model/makePrediction/ |This endpoint has the unique purpose to received the nifiti file and generate the prediction of the CNN and then it summits the result to the mongo database||**resonance_file**(Nifti file),  **metadata**(JSON file),  **email**(String)|

👽 Feel free to make any changes in the code 👽

