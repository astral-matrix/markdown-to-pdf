#!/bin/bash

# Script to start the markup2pdf backend and webapp

# Store the project root directory
PROJECT_ROOT="$(pwd)"

# Activate the Python virtual environment
echo "Activating Python virtual environment..."
source .venv/bin/activate || { echo "Failed to activate virtual environment"; exit 1; }
echo "Virtual environment activated successfully"

# Start the backend
echo "Starting markup2pdf backend..."
cd "$PROJECT_ROOT/markup2pdf-backend" && python3 run.py &
BACKEND_PID=$!
echo "Backend started with PID: $BACKEND_PID"

# Start the webapp - use absolute paths to avoid directory navigation issues
echo "Starting markup2pdf webapp..."
cd "$PROJECT_ROOT/markup2pdf-webapp" && npm run dev &
WEBAPP_PID=$!
echo "Webapp started with PID: $WEBAPP_PID"

echo "Both services started in background."
echo "To stop them, run: kill $BACKEND_PID $WEBAPP_PID"

# Save PIDs to a file for later termination if needed
cd "$PROJECT_ROOT"
echo "$BACKEND_PID $WEBAPP_PID" > .running_pids

echo "PIDs saved to .running_pids file" 