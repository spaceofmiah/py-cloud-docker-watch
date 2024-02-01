# py-cloud-docker-watch
A script that creates a docker container while streaming the container logs to AWS cloudwatch

## Running the project
Poetry is the package manager used in this project and can be downloaded from https://python-poetry.org/docs/#installation

1. `poetry shell` : Activates project's shell

2. `poetry install`: Install dependencies within the activated shell

3. `python main.py [args]` : Runs script with the provided arguments. The argument options are as listed below

##### Argument options

  - `--docker-image=image_name` : _image_name_ should be a valid docker image on docker hub

  - `--base-command=script` : _script_ is a bash script to run within the docker container spinned up from the docker image

  - `--aws-cloudwatch-group=cw_group`: _cw_group_ should be replaced with an AWS cloudwatch group

  - `--aws-cloudwatch-stream=cw_stream`: _cw_stream_ should be replaced with an AWS cloudwatch stream

  - `--aws-access-key-id=aki`: _aki_ should be replaced with a valid and active AWS access key id

  - `--aws-secret-access-key=sak` _sak_ should be replaced with a valid and active AWS secret access key

  - `--aws-region=region` _region_ should be replaced with the region where the services is at

###### Example 

Run an example command with
```bash
python main.py --docker-image=python --bash-command=$'pip install pip -U && pip
install tqdm && python -c \"import time\ncounter = 0\nwhile
True:\n\tprint(counter)\n\tcounter = counter + 1\n\ttime.sleep(0.1)\"' --aws-cloudwatch-group=test-task-group-1 --aws-cloudwatch-stream=test-task-stream-1 --aws-access-key-id=valid-access-key-id --aws-secret-access-key=valid-secret-access-key --aws-region=region
```

### Getting Help
Run `python main.py --help` to get help on running the script


##### Requirements:
- argument parser: feed and parse arguments sent to script  ✅ 
- startup docker: start docker from python script 
- aws sdk: for cloud watch configuration

##### Tradeoffs:
* Docker not installed ?
  - [approach 1] Should program install docker on the machine depending on the OS ?
  - [approach 2] Should program gracefully exit with the reason/cause so user handles for it ?



