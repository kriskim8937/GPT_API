# Define variables
VENV_DIR = venv
REQUIREMENTS = requirements.txt
PYTHON = python3
SRC_DIR = src
# Default target
all: venv install

# Target to create virtual environment
venv:
	@echo "Creating virtual environment..."
	@$(PYTHON) -m venv $(VENV_DIR)

# Target to activate virtual environment and install requirements
install: venv
	@echo "Activating virtual environment and installing requirements..."
	@$(VENV_DIR)/bin/pip install -r $(REQUIREMENTS)

lint:
	echo 'Start formatting...'
	@ruff format $(SRC_DIR) 
	echo 'Start linting...'
	@ruff check --fix $(SRC_DIR)

# Target to clean the virtual environment
clean:
	@echo "Removing virtual environment..."
	@rm -rf $(VENV_DIR)

# Target to run the main script (if needed)
run: venv install
	@echo "Running the main script..."
	@$(VENV_DIR)/bin/python main.py

# Phony targets to avoid conflicts with file names
.PHONY: all venv install clean run
