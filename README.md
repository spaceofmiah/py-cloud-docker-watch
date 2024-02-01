# py-cloud-docker-watch
A script that creates a docker container while streaming the container logs to AWS cloudwatch


##### Requirements:
- argument parser: feed and parse arguments sent to script
- env loader: environment variable loader for aws credentials
- aws sdk: for cloud watch configuration

##### Tradeoffs:
* Docker not installed ?
  - [approach 1] Should program install docker on the machine depending on the OS ?
  - [approach 2] Should program gracefully exit with the reason/cause so user handles for it ?

