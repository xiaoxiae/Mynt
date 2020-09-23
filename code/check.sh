#!/bin/bash
set -euo pipefail

black **/*.py
pylint **/*.py --fail-under=9
isort **/*.py
