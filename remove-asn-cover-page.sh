#!/usr/bin/env bash
set -e -o pipefail
export LC_ALL=C

#Use the DOCUMENT_WORKING_PATH environment variable from Paperless
IN="$DOCUMENT_WORKING_PATH"

# Define the path to your Python script
script_path="/mnt/scripts/remove-asn-cover-page.py"

# Define the path to your virtual environment (replace 'venv' with your venv name)
venv_path="/mnt/scripts/venv"

# Activate the virtual environment
. "$venv_path/bin/activate"

# Run the Python script
python "$script_path" "$IN" 0.90

# Deactivate the virtual environment
deactivate