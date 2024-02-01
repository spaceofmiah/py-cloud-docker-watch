.phony: test

test:
	python main.py --docker-image=python --bash-command='sh -c "pip install pip -U && pip install tqdm && python -c \"import time\ncounter = 0\""' --aws-cloudwatch-group=test-task-group-1 --aws-cloudwatch-stream=test-task-stream-1 --aws-access-key-id=valid-access-key-id --aws-secret-access-key=valid-secret-access-key --aws-region=region