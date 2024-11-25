DOCKERFILE_PATH = ./server/Dockerfile
BACKEND_DIR = ./server
CLIENT_DIR = ./client
SERVER_CONFIG_FILE = ${BACKEND_DIR}/pyproject.toml
CLIENT_CONFIG_FILE = ${CLIENT_DIR}/pyproject.toml
PYTHON_LOCK_FILE = ${BACKEND_DIR}/uv.lock
PYTHON_REQ_FILE = ${BACKEND_DIR}/requirements.txt
DOCKER_NAMESPACE ?= openapm
DOCKER_REPO ?= backend
DOCKER_TAG ?= latest

########################################################
# Code checks
########################################################


install-quality: ${PYTHON_CONFIG_FILE}
	uv export --no-hashes --locked --only-dev -o ${PYTHON_REQ_FILE} --project ${BACKEND_DIR}
	uv pip install --system -r ${PYTHON_REQ_FILE}

lint-check: ${SERVER_CONFIG_FILE} ${CLIENT_CONFIG_FILE}
	ruff format --check ${BACKEND_DIR} --config ${SERVER_CONFIG_FILE}
	ruff check ${BACKEND_DIR} --config ${SERVER_CONFIG_FILE}
	ruff format --check ${CLIENT_DIR} --config ${CLIENT_CONFIG_FILE}
	ruff check ${CLIENT_DIR} --config ${CLIENT_CONFIG_FILE}

lint-format: ${SERVER_CONFIG_FILE} ${CLIENT_CONFIG_FILE}
	ruff format ${BACKEND_DIR} --config ${SERVER_CONFIG_FILE}
	ruff check --fix ${BACKEND_DIR} --config ${SERVER_CONFIG_FILE}
	ruff format ${CLIENT_DIR} --config ${CLIENT_CONFIG_FILE}
	ruff check --fix ${CLIENT_DIR} --config ${CLIENT_CONFIG_FILE}

precommit: ${PYTHON_CONFIG_FILE} .pre-commit-config.yaml
	pre-commit run --all-files

typing-check: ${SERVER_CONFIG_FILE} ${CLIENT_CONFIG_FILE}
	mypy --config-file ${SERVER_CONFIG_FILE}
	mypy --config-file ${CLIENT_CONFIG_FILE}

deps-check: .github/verify_deps_sync.py
	python .github/verify_deps_sync.py

# this target runs checks on all files
quality: lint-check typing-check deps-check

style: lint-format precommit

########################################################
# Build
########################################################

lock: ${PYTHON_CONFIG_FILE}
	uv lock --project ${BACKEND_DIR}

req: ${PYTHON_CONFIG_FILE} ${PYTHON_LOCK_FILE}
	uv export --no-hashes --locked --no-dev -q -o ${PYTHON_REQ_FILE} --project ${BACKEND_DIR}

# Build the docker
build: req ${DOCKERFILE_PATH}
	docker build --platform linux/amd64 ${BACKEND_DIR} -t ${DOCKER_NAMESPACE}/${DOCKER_REPO}:${DOCKER_TAG}

push: build
	docker push ${DOCKER_NAMESPACE}/${DOCKER_REPO}:${DOCKER_TAG}

# Run the docker
start: build docker-compose.yml
	docker compose up -d --wait

# Run the docker
stop: docker-compose.yml
	docker compose down
