from tap import Tap
import docker
import boto3
import time


class ScriptArguments(Tap):
    docker_image: str  # Docker image name e.g nginx, redis, python
    bash_command: str # Bash command to run within the image
    aws_cloudwatch_group: str   # AWS cloudwatch group
    aws_cloudwatch_stream: str  # AWS cloudwatch stream
    aws_access_key_id: str   # AWS access secret key id
    aws_secret_access_key: str  # AWS secret access key
    aws_region: str  # AWS region


class CloudLog:
    """Logger class streaming application logs to AWS CloudWatch"""

    def __init__(self, group:str, stream:str, region, key_id, secret_id):
        """CloudLog initializer
        
        :param group: cloud watch log group name
        
        :param stream: cloud watch log stream name

        :param region: AWS region

        :param key_id: AWS access key id

        :param secret_id: AWS secret access key id
        
        :example:
        
        >>> from cloud_log import CloudLog
        >>> cloud_log = CloudLog(group='test-group', stream='test-stream', region='us-east-1', key_id='XXXXXXXXXXXXXXXXXXXX', secret_id='XXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
        >>> cloud_log.put_log_events([{'timestamp': int(time.time() * 1000), 'message': 'Hello World'}])
        """
        self._client = boto3.client(
            'logs', 
            region_name=region,
            aws_access_key_id=key_id, 
            aws_secret_access_key=secret_id
        )
        self.group = group
        self.stream = stream
        self.setup()

    def put_log_events(self, log_events):
        """
        Sends log event to cloud

        :param log_event: Event to send to cloudwatch
        """
        return self._client.put_log_events(
            logGroupName=self.group, 
            logStreamName=self.stream, 
            logEvents=log_events
        )

    def setup(self):
        """
        Configures instance ensuring the log group and log stream provided are available
        and creating them if not available.
        """
        try:
            response = self._client.describe_log_groups(logGroupNamePrefix=self.group)
            # check if the log group exists
            if len(response['logGroups']) > 0:
                return response['logGroups'][0]['logGroupName']
            else:
                # create the log group
                self._client.create_log_group(logGroupName=self.group)

            response = self._client.describe_log_streams(logGroupName=self.group, logStreamNamePrefix=self.stream)
            if len(response['logStreams']) > 0:
                return response['logStreams'][0]['logStreamName']
            else:
                self._client.create_log_stream(logGroupName=self.group, logStreamName=self.stream)
        except Exception as e:
            print(f"<< [ExecutionFailed]: CloudLog setup failed \n\n{e}")



args = ScriptArguments(underscores_to_dashes=True).parse_args()



# Run program on file invocation from shell/terminal/cmd
if __name__ == "__main__":
    # Ensure docker is installed and is running as a daemon or desktop app otherwise alert user so they can start docker
    try:
        docker_client = docker.from_env()
    except Exception as e:
        print("\n\n<< [ExecutionFailed]: Docker is not running on your machine. Start docker desktop and retry\n")
        exit(1)
    
    # check if the docker image exists
    print(f"<< Locating image {args.docker_image}...")
    image_exists = len(docker_client.images.list(name=args.docker_image)) > 0
    if image_exists is False:
        try:
            # Pull image from docker hub
            print(f"<< Image {args.docker_image} not found\nKindly ensure you're connected to the internet\npulling...")
            docker_client.images.pull(args.docker_image)
            print(f"<< Image {args.docker_image} pulled successfully")
        except Exception as e:
            print(f"<< [ExecutionFailed]: Failed to pull image {args.docker_image} \n\n{e}")
            exit(1)
    
    # Create docker container instance
    try:
        print(f"\n<< Starting docker container from image {args.docker_image}")
        container = docker_client.containers.run(args.docker_image, command=args.bash_command, auto_remove=True, detach=True)
        print(f"<< Docker container started with id {container.id}\n<< logs:\n\n")
    except Exception as e:
        print(f"<< [ExecutionFailed]: Docker container setup failed \n\n{e}")
        exit(1)

    # Create CloudWatch logger instance
    try:
        cloud_logger = CloudLog(
            secret_id=args.aws_secret_access_key,
            stream=args.aws_cloudwatch_stream, 
            group=args.aws_cloudwatch_group, 
            key_id=args.aws_access_key_id, 
            region=args.aws_region,
        )
    except Exception as e:
        print(f"<< [ExecutionFailed]: CloudLog setup failed \n\n{e}")
        exit(1)

    
    for line in container.logs(stream=True):
        try:
            response = cloud_logger.put_log_events(
                [
                    {
                        "timestamp": int(time.time() * 1000), 
                        "message": f"{line.strip()}"
                    }
                ]
            )
            print(response)
        except Exception as e:
            print(f"<< [ExecutionFailed]: Failed to send log to cloud \n\n{e}")
            exit(1)