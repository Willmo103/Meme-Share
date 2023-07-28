#!/bin/bash

# Function to display help message
function show_help {
    echo "Usage: $0 <environment>"
    echo "  environment: Specify the environment (dev or prod)."
    echo "Examples:"
    echo "  $0 dev"
    echo "  $0 prod"
}

# Check if an argument is provided
if [ $# -eq 0 ]; then
    echo "Error: No arguments provided."
    show_help
    exit 1
fi

# Check if the provided environment is valid
if [ "$1" != "dev" ] && [ "$1" != "prod" ]; then
    echo "Error: Invalid environment specified. Use 'dev' or 'prod'."
    show_help
    exit 1
fi

# Activate the virtual environment and run Flask accordingly
if [ "$1" == "dev" ]; then
    source ./.venv/bin/activate
    flask run --reload --debugger
elif [ "$1" == "prod" ]; then
    source ./.venv/bin/activate
    flask run
fi
