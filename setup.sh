#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Text colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the directory of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

# Get the name of the current directory (project name)
PROJECT_NAME=$(basename "$SCRIPT_DIR")

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for required commands
for cmd in sed grep; do
    if ! command_exists "$cmd"; then
        echo -e "${RED}Error: $cmd is required but not installed. Please install it and try again.${NC}"
        exit 1
    fi
done

# Check Python version
if command -v python3.10 &>/dev/null; then
    PYTHON=python3.10
elif command -v python3 &>/dev/null && [[ $(python3 -c 'import sys; print(sys.version_info[1])') -eq 10 ]]; then
    PYTHON=python3
else
    echo -e "${RED}Python 3.10 is required but it's not installed. Please install it and try again.${NC}"
    exit 1
fi

echo -e "${GREEN}Using Python: $($PYTHON --version)${NC}"

# Create virtual environment
if [ ! -d "$PROJECT_NAME" ]; then
    echo -e "${BLUE}Creating virtual environment...${NC}"
    $PYTHON -m venv "$PROJECT_NAME"
else
    echo -e "${YELLOW}Virtual environment already exists. Skipping creation.${NC}"
fi

source "$PROJECT_NAME/bin/activate"

# Upgrade pip
echo -e "${BLUE}Upgrading pip...${NC}"
pip install --upgrade pip

# Install project dependencies
echo -e "${BLUE}Installing project dependencies...${NC}"
pip install -r requirements.txt

# Install development dependencies
echo -e "${BLUE}Installing development dependencies...${NC}"
pip install pre-commit pytest

# Set up pre-commit hooks
echo -e "${BLUE}Setting up pre-commit hooks...${NC}"
pre-commit install

# Copy .env.sample to .env if it doesn't exist
if [ ! -f .env ]; then
    if [ -f .env.sample ]; then
        cp .env.sample .env
        echo -e "${YELLOW}Copied .env.sample to .env. Please edit .env with your actual configuration.${NC}"
    else
        echo -e "${RED}Error: .env.sample file not found. Please create a .env file manually.${NC}"
    fi
else
    echo -e "${YELLOW}.env file already exists. Skipping copy.${NC}"
fi

# Add PROJECT_NAME/ to .gitignore if not already present
if ! grep -q "^$PROJECT_NAME/$" .gitignore 2>/dev/null; then
    echo "$PROJECT_NAME/" >> .gitignore
    echo -e "${YELLOW}Added $PROJECT_NAME/ to .gitignore${NC}"
else
    echo -e "${YELLOW}$PROJECT_NAME/ already in .gitignore. Skipping.${NC}"
fi

# Update .pre-commit-config.yaml entry
PRE_COMMIT_CONFIG_FILE=".pre-commit-config.yaml"
if [ -f "$PRE_COMMIT_CONFIG_FILE" ]; then
    # Use sed to replace any 'source */bin/activate' pattern with the correct path
    sed -i.bak "s|source .*/bin/activate|source $PROJECT_NAME/bin/activate|g" "$PRE_COMMIT_CONFIG_FILE"
    
    # Also update the python command to use the correct path
    sed -i.bak "s|python -m unittest|$PROJECT_NAME/bin/python -m unittest|g" "$PRE_COMMIT_CONFIG_FILE"
    
    echo -e "${YELLOW}Updated the .pre-commit-config.yaml with the correct virtual environment path.${NC}"
else
    echo -e "${RED}.pre-commit-config.yaml file not found. Please ensure it exists in the project directory.${NC}"
fi

# Final instructions
echo -e "${GREEN}
Setup completed successfully!

To activate the virtual environment, run:
${BLUE}source $PROJECT_NAME/bin/activate${GREEN}

To deactivate the virtual environment, run:
${BLUE}deactivate${GREEN}

Please complete these manual steps:
1. Edit the .env file with your actual configuration.
2. Set up your MongoDB database and ensure it's running.
3. Obtain an OpenAI API key and add it to your .env file.

To run the application:
${BLUE}python app.py${GREEN}

To run tests:
${BLUE}python -m unittest discover tests${GREEN}

Happy coding!
${NC}"