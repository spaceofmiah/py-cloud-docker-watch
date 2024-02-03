# py-cloud-docker-watch
A script that creates a docker container while streaming the container logs to AWS cloudwatch

## Running the project
Poetry is the package manager used in this project and can be downloaded from https://python-poetry.org/docs/#installation

1. `poetry shell` : Activates project's shell

2. `poetry install`: Install dependencies within the activated shell

3. `python main.py [args]` : Runs script with the provided arguments. The argument options are as listed below

##### Argument options

  - `--docker-image=image_name` : _image_name_ should be a valid docker image on docker hub

  - `--bash-command=script` : _script_ is a bash script to run within the docker container spinned up from the docker image

  - `--aws-cloudwatch-group=cw_group`: _cw_group_ should be replaced with an AWS cloudwatch group

  - `--aws-cloudwatch-stream=cw_stream`: _cw_stream_ should be replaced with an AWS cloudwatch stream

  - `--aws-access-key-id=aki`: _aki_ should be replaced with a valid and active AWS access key id

  - `--aws-secret-access-key=sak` _sak_ should be replaced with a valid and active AWS secret access key

  - `--aws-region=region` _region_ should be replaced with the region where the services is at

###### Example 

Run an example command with
```bash
python main.py \
--docker-image=python \
--aws-cloudwatch-group=cloud \
--aws-cloudwatch-stream=stream \
--aws-access-key-id=accesskeyid \
--aws-secret-access-key=secretaccesskey \
--aws-region=us-east-1 \
--bash-command=$'bash -c \"pip install pip -U && pip install tqdm && python -c \'
import time
counter = 0
while True:
    print(counter)
    counter +=1
    time.sleep(0.1)
\'\"'
```

**--bash-command code breakdown**: the bash command is a script `$"xxxxxxx xxxxxx"`. The script contains a bash command `bash -c` and the program run by the bash command is `pip install pip -U` which upgrade pip version,  `&& pip install tqdm` which installs _tqdm_ library and `&& python -c` which is a python command that runs a python script.

> we're running a script that run a bash script command which also contains a python script command. The python script is within the bash script command

Due to the presence of different command to be run (most of which are complex command [contains more than one statement]) there's need to pay attention to how we differentiate the commands. e.g for the bash script we fed the command with double quotes 

`\"pip install pip -U && pip install tqdm && python -c `. 

Given the python script also needs to accounted for within the bash script, we needed to pass its program in single quote 
```bash
\"pip xxx xxxx && python -c \'
 # all other python program follows in the next line and structured like a normal python program (use space and tabs appropriately)
\'\"
```

Notice the `\` before each command are fed and when they end ? this is so that we don't mistakenly close outer script command. So we're escaping the symbol after the `\` which in our case is either `"` (double quote) or `'` single quote.

If you're running the program appropriately (with above example), your terminal would look like this 

<img width="1010" alt="Constructing Script Command" src="https://github.com/spaceofmiah/py-cloud-docker-watch/assets/37231237/9477f629-3d09-4724-a885-ee404c735579">


_Should in case you'll be using a different script for the `--bash-command` kindly **pay attention to the structure** of your script_

> Following the above NOTE, you'll be able to feed the bash command with the right formatting.

### Getting Help
Run `python main.py --help` to get help on running the script


##### Requirements:
- argument parser: feed and parse arguments sent to script  ✅
- startup docker: start docker from python script ✅
- aws sdk: for cloud watch configuration ✅




