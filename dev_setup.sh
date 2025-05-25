#!/bin/bash
set -e

# Script to install development tools for Markup2PDF

echo "Setting up development linters and type checkers..."

# Install Node.js linters
echo "Installing ESLint packages..."
cd markup2pdf-webapp
npm install --save-dev eslint @typescript-eslint/eslint-plugin @typescript-eslint/parser
cd ..

# Install Python linters in the virtual environment
cd markup2pdf-backend
if [ ! -d .venv ]; then
    echo "Python virtual environment not found. Creating..."
    python3 -m venv .venv
fi

echo "Activating Python virtual environment..."
source .venv/bin/activate

echo "Installing Python linting dependencies..."
python3 -m pip install pylint mypy

deactivate
cd ..

echo "Development setup complete!"

echo "To activate the Python environment, run: source markup2pdf-backend/.venv/bin/activate"
echo "To run ESLint: cd markup2pdf-webapp && npx eslint ."
echo "To run mypy: cd markup2pdf-backend && mypy app"
echo "To run pylint: cd markup2pdf-backend && pylint app"
