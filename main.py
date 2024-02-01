from tap import Tap



class ScriptArguments(Tap):
    docker_image: str  # Docker image name e.g nginx, redis, python
    bash_command: str # Bash command to run within the image
    aws_cloudwatch_group: str   # AWS cloudwatch group
    aws_cloudwatch_stream: str  # AWS cloudwatch stream
    aws_access_key_id: str   # AWS access secret key id
    aws_secret_access_key: str  # AWS secret access key
    aws_region: str  # AWS region



args = ScriptArguments(underscores_to_dashes=True).parse_args()

print(
"Docker Image: ", args.docker_image, "\nAWS CWG: ", 
args.aws_cloudwatch_group, "\nAWS CWS: ", 
args.aws_cloudwatch_stream, "\nAWS AKID: ", 
args.aws_access_key_id, "\nAWS SAK: ", 
args.aws_secret_access_key, "\nBash Script: \n\n", 
args.bash_command, "\n\n",
)