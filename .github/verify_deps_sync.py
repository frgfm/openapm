# Copyright (C) 2024, François-Guillaume Fernandez.

# This program is licensed under the Apache License 2.0.
# See LICENSE or go to <https://www.apache.org/licenses/LICENSE-2.0> for full license details.

import re
import tomllib
from pathlib import Path

import yaml

SERVER_DOCKERFILE_PATH = "server/Dockerfile"
SERVER_PRECOMMIT_PATH = ".pre-commit-config.yaml"
SERVER_PYPROJECT_PATH = "server/pyproject.toml"
CLIENT_PYPROJECT_PATH = "client/pyproject.toml"


def main():
    # Retrieve & parse all deps files
    deps_dict = {}
    # UV: Dockerfile, precommit, .github
    # Parse Dockerfile
    with Path(SERVER_DOCKERFILE_PATH).open("r") as f:
        dockerfile = f.read()
    uv_version = re.search(r"ghcr\.io/astral-sh/uv:(\d+\.\d+\.\d+)", dockerfile).group(1)
    deps_dict["uv"] = [{"file": SERVER_DOCKERFILE_PATH, "version": uv_version}]
    # Parse precommit
    with Path(SERVER_PRECOMMIT_PATH).open("r") as f:
        precommit = yaml.safe_load(f)

    for repo in precommit["repos"]:
        if repo["repo"] == "https://github.com/astral-sh/uv-pre-commit":
            deps_dict["uv"].append({"file": SERVER_PRECOMMIT_PATH, "version": repo["rev"].lstrip("v")})
        elif repo["repo"] == "https://github.com/charliermarsh/ruff-pre-commit":
            deps_dict["ruff"] = [{"file": SERVER_PRECOMMIT_PATH, "version": repo["rev"].lstrip("v")}]

    # Parse pyproject.toml
    with Path(SERVER_PYPROJECT_PATH).open("rb") as f:
        pyproject = tomllib.load(f)

    dev_deps = pyproject["tool"]["uv"]["dev-dependencies"]
    for dep in dev_deps:
        if dep.startswith("ruff=="):
            deps_dict["ruff"].append({"file": SERVER_PYPROJECT_PATH, "version": dep.split("==")[1]})

    with Path(CLIENT_PYPROJECT_PATH).open("rb") as f:
        pyproject = tomllib.load(f)

    dev_deps = pyproject["project"]["optional-dependencies"]["quality"]
    for dep in dev_deps:
        if dep.startswith("ruff=="):
            deps_dict["ruff"].append({"file": CLIENT_PYPROJECT_PATH, "version": dep.split("==")[1]})

    # Parse github/workflows/...
    for workflow_file in Path(".github/workflows").glob("*.yml"):
        with workflow_file.open("r") as f:
            workflow = yaml.safe_load(f)
            if "env" in workflow and "UV_VERSION" in workflow["env"]:
                deps_dict["uv"].append({
                    "file": str(workflow_file),
                    "version": workflow["env"]["UV_VERSION"].lstrip("v"),
                })

    # Assert all deps are in sync
    troubles = []
    for dep, versions in deps_dict.items():
        _versions = {v["version"] for v in versions}
        if len(_versions) != 1:
            inv_dict = {v: set() for v in _versions}
            for version in versions:
                inv_dict[version["version"]].add(version["file"])
            troubles.extend([
                f"{dep}:",
                "\n".join(f"- '{v}': {', '.join(files)}" for v, files in inv_dict.items()),
            ])

    if len(troubles) > 0:
        raise AssertionError("Some dependencies are out of sync:\n\n" + "\n".join(troubles))


if __name__ == "__main__":
    main()
