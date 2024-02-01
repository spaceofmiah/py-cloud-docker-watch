from tap import Tap
import logging
import docker



logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ScriptArguments(Tap):
    docker_image: str  # Docker image name e.g nginx, redis, python
    bash_command: str # Bash command to run within the image
    aws_cloudwatch_group: str   # AWS cloudwatch group
    aws_cloudwatch_stream: str  # AWS cloudwatch stream
    aws_access_key_id: str   # AWS access secret key id
    aws_secret_access_key: str  # AWS secret access key
    aws_region: str  # AWS region


args = ScriptArguments(underscores_to_dashes=True).parse_args()

if __name__ == "__main__":
    try:
        docker_client = docker.from_env()
    except Exception as e:
        print("\n\n[ExecutionFailed]: Docker is not running on your machine. Start docker desktop and retry\n")
        exit(1)
    
    # check if the docker image exists
    print(f"Locating image {args.docker_image}...")
    image_exists = len(docker_client.images.list(name=args.docker_image)) > 0
    if image_exists is False:
        print(f"Image {args.docker_image} not found\nKindly ensure you're connected to the internet\npulling...")
        docker_client.images.pull(args.docker_image)
        print(f"Image {args.docker_image} pulled successfully")
    
    print(f"\nStarting docker container from image {args.docker_image}")
    container = docker_client.containers.run(args.docker_image, args.bash_command, detach=True)
    print(f"Docker container started with id {container.id}\n<< logs:\n\n")
    for line in container.logs(stream=True):
        print(line.strip())