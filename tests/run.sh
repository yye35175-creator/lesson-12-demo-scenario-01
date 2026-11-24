#!/usr/bin/env bash
set -euo pipefail

test_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
python_bin="${PYTHON:-python3}"
if ! command -v "$python_bin" >/dev/null && [[ -z "${PYTHON:-}" ]]; then
    python_bin=python
fi
exec "$python_bin" "$test_dir/check_api.py" "$@"
