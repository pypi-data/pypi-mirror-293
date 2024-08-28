#!/bin/bash

cd "$(dirname "$0")"/..

echo y | python3 -m pip uninstall sfsdk

# Run pip3 install and capture both output and exit status
install_output=$(python3 -m pip install --user . 2>&1)
install_status=$?

# Check if the command failed and if the specific PEP 668 error is present
# Works like set -e apart from it allows PEP 668
if [[ $install_status -ne 0 ]]; then
    if echo "$install_output" | grep -q "error: externally-managed-environment"; then
        python3 -m pip install --break-system-packages --user .
    else
        echo "$install_output"
        exit $install_status
    fi
else
    echo "$install_output"
fi
