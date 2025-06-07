#!/bin/bash

#Run this script from the project root directory
# Print commands and exit on errors
set -ex

echo "Setting up Markdown2PDF development environment..."

# Create Python virtual environment in backend directory
echo "Creating Python virtual environment..."
cd markdown2pdf-backend
python3 -m venv .venv

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
python3 -m pip install -r requirements.txt
cd ..

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
cd markdown2pdf-webapp
npm install
cd ..

echo "Installation complete!"
echo "To activate the Python environment, run: source .venv/bin/activate"
echo "To start the backend server: cd markdown2pdf-backend && python3 run.py"
echo "To start the frontend server: cd markdown2pdf-webapp && npm run dev" 
echo "To run ESLint: cd markdown2pdf-webapp && npx eslint ."
echo "To run mypy: cd markdown2pdf-backend && mypy app"
echo "To run pylint: cd markdown2pdf-backend && pylint app"