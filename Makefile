DOCKERFILE_PATH = ./server/Dockerfile
BACKEND_DIR = ./server
PYTHON_CONFIG_FILE = ${BACKEND_DIR}/pyproject.toml
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

lint-check: ${PYTHON_CONFIG_FILE}
	ruff format --check . --config ${PYTHON_CONFIG_FILE}
	ruff check . --config ${PYTHON_CONFIG_FILE}

lint-format: ${PYTHON_CONFIG_FILE}
	ruff format . --config ${PYTHON_CONFIG_FILE}
	ruff check --fix . --config ${PYTHON_CONFIG_FILE}

precommit: ${PYTHON_CONFIG_FILE} .pre-commit-config.yaml
	pre-commit run --all-files

typing-check: ${PYTHON_CONFIG_FILE}
	mypy --config-file ${PYTHON_CONFIG_FILE}

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