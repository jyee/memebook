#Memebook

This is a sample application built with microservices. It's useful for demonstrations and workshops.

## Design/About

The memebook is a simple guestbook application with one front-end [aiohttp](https://aiohttp.readthedocs.io/en/stable/) web server. When visitors post an entry, the `memebook` service sends the text to the `lolcat` service that translates the text into lolcat (e.g. "Can I have a cheeseburger?" becomes "I can haz a cheezburger"). The `memebook` service also requests a dog photo from the `doggo` service. The `lolcat` and `doggo` services both use the [Flask](https://palletsprojects.com/p/flask/) python framework. Finally the `memebook` service combines the new text and image and saves the combination into [Redis](https://redis.io/).

This repository also contains a `traffic_generator` deployment to simulate traffic to the application and a [Datadog](http://datadoghq.com) daemonset to monitor the application.

## Running

To run the application, first create a Kubernetes secret using your [Datadog API Key](https://app.datadoghq.com/account/settings#api).

```
kubectl create secret generic datadog-api --from-literal=token=<YOUR_DATADOG_API_KEY>
```

Next, apply the yaml files from the kubernetes directory.

```
kubectl apply -f kubernetes/
```

## Development

Each service has its own directory in this repo. Each service directory contains a `Dockerfile` and an `app` directory with the service code.

There are two helper tools in the root of the project: `build.sh` and `build-n-push.sh`. The `build.sh` script will build Docker images for all of the services in the repository (i.e. any top-level directory with a `Dockerfile`). The `build-n-push.sh` script runs the build script and additionally pushes the images to the Docker Hub and updates the Kubernetes yaml files with the appropriate image build tag.

Both commands take two arguments: the version and the Docker hub prefix (i.e. your Docker username). For example:

```
./build-n-push.sh 1.0.3 my_username
```
