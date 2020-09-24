#!/bin/bash
set -euo pipefail

black **/*.py
isort **/*.py
pylint **/*.py --fail-under=9
