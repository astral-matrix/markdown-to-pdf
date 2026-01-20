#!/bin/bash

# Interactive startup script for markdown2pdf
# Runs both backend and frontend with log viewing and clean shutdown

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
BACKEND_LOG="$PROJECT_ROOT/.backend.log"
FRONTEND_LOG="$PROJECT_ROOT/.frontend.log"
PID_FILE="$PROJECT_ROOT/.running_pids"

BACKEND_PID=""
FRONTEND_PID=""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Kill a process and all its children
kill_tree() {
    local pid=$1
    if [[ -z "$pid" ]]; then
        return
    fi

    # Get all child processes
    local children
    children=$(pgrep -P "$pid" 2>/dev/null)

    # Kill children first (recursively)
    for child in $children; do
        kill_tree "$child"
    done

    # Kill the process itself
    if kill -0 "$pid" 2>/dev/null; then
        kill "$pid" 2>/dev/null || true
    fi
}

cleanup() {
    echo ""
    echo -e "${YELLOW}Shutting down services...${NC}"

    if [[ -n "$BACKEND_PID" ]]; then
        echo -e "Stopping backend process tree (PID: $BACKEND_PID)..."
        kill_tree "$BACKEND_PID"
        echo -e "${GREEN}Backend stopped${NC}"
    fi

    if [[ -n "$FRONTEND_PID" ]]; then
        echo -e "Stopping frontend process tree (PID: $FRONTEND_PID)..."
        kill_tree "$FRONTEND_PID"
        echo -e "${GREEN}Frontend stopped${NC}"
    fi

    # Also kill any lingering processes on the ports
    echo -e "Cleaning up any remaining processes on ports 3000 and 8000..."
    lsof -ti:3000 2>/dev/null | xargs kill 2>/dev/null || true
    lsof -ti:8000 2>/dev/null | xargs kill 2>/dev/null || true

    # Clean up log files
    rm -f "$BACKEND_LOG" "$FRONTEND_LOG" "$PID_FILE"

    echo -e "${GREEN}All services stopped cleanly.${NC}"
    exit 0
}

trap cleanup SIGINT SIGTERM

clear_screen() {
    printf '\033[2J\033[H'
}

print_header() {
    echo -e "${BOLD}${CYAN}╔════════════════════════════════════════════════════╗${NC}"
    echo -e "${BOLD}${CYAN}║${NC}        ${BOLD}Markdown to PDF Converter${NC}                  ${BOLD}${CYAN}║${NC}"
    echo -e "${BOLD}${CYAN}╚════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_status() {
    local backend_status="${RED}stopped${NC}"
    local frontend_status="${RED}stopped${NC}"

    if [[ -n "$BACKEND_PID" ]] && kill -0 "$BACKEND_PID" 2>/dev/null; then
        backend_status="${GREEN}running${NC} (PID: $BACKEND_PID)"
    fi

    if [[ -n "$FRONTEND_PID" ]] && kill -0 "$FRONTEND_PID" 2>/dev/null; then
        frontend_status="${GREEN}running${NC} (PID: $FRONTEND_PID)"
    fi

    echo -e "${BOLD}Service Status:${NC}"
    echo -e "  ${BLUE}[1]${NC} Backend  (Python/FastAPI) : $backend_status"
    echo -e "  ${BLUE}[2]${NC} Frontend (Next.js)        : $frontend_status"
    echo ""
    echo -e "${BOLD}URLs:${NC}"
    echo -e "  Backend API : ${CYAN}http://localhost:8000${NC}"
    echo -e "  Frontend    : ${CYAN}http://localhost:3000${NC}"
    echo ""
}

print_menu() {
    echo -e "${BOLD}Commands:${NC}"
    echo -e "  ${YELLOW}1${NC} - View backend logs"
    echo -e "  ${YELLOW}2${NC} - View frontend logs"
    echo -e "  ${YELLOW}r${NC} - Refresh status"
    echo -e "  ${YELLOW}q${NC} - Quit (stops all services)"
    echo ""
}

view_logs() {
    local log_file="$1"
    local service_name="$2"

    clear_screen
    echo -e "${BOLD}${CYAN}═══ $service_name Logs ═══${NC}"
    echo -e "${YELLOW}(Press Enter to return to menu)${NC}"
    echo ""

    if [[ -f "$log_file" ]]; then
        tail -50 "$log_file"
    else
        echo -e "${RED}No logs available yet.${NC}"
    fi

    echo ""
    echo -e "${YELLOW}───────────────────────────────────${NC}"
    read -r -p "Press Enter to return to menu..."
}

start_services() {
    echo -e "${YELLOW}Starting services...${NC}"
    echo ""

    # Clear old log files
    > "$BACKEND_LOG"
    > "$FRONTEND_LOG"

    # Activate virtual environment and start backend
    echo -e "Starting backend..."
    (
        cd "$PROJECT_ROOT/markdown2pdf-backend"
        source .venv/bin/activate
        exec python3 run.py
    ) >> "$BACKEND_LOG" 2>&1 &
    BACKEND_PID=$!
    echo -e "${GREEN}Backend started (PID: $BACKEND_PID)${NC}"

    # Start frontend
    echo -e "Starting frontend..."
    (
        cd "$PROJECT_ROOT/markdown2pdf-webapp"
        exec npm run dev
    ) >> "$FRONTEND_LOG" 2>&1 &
    FRONTEND_PID=$!
    echo -e "${GREEN}Frontend started (PID: $FRONTEND_PID)${NC}"

    # Save PIDs
    echo "$BACKEND_PID $FRONTEND_PID" > "$PID_FILE"

    echo ""
    echo -e "${GREEN}All services started!${NC}"
    echo -e "${YELLOW}Waiting for services to initialize...${NC}"
    sleep 3
}

main_loop() {
    while true; do
        clear_screen
        print_header
        print_status
        print_menu

        read -r -p "Enter command: " cmd

        case "$cmd" in
            1)
                view_logs "$BACKEND_LOG" "Backend (Python/FastAPI)"
                ;;
            2)
                view_logs "$FRONTEND_LOG" "Frontend (Next.js)"
                ;;
            r|R)
                # Just refresh - loop will redraw
                ;;
            q|Q)
                cleanup
                ;;
            *)
                echo -e "${RED}Invalid command. Press Enter to continue...${NC}"
                read -r
                ;;
        esac
    done
}

# Main execution
clear_screen
print_header
start_services
main_loop
