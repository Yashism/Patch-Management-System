#!/bin/bash

# Set up logging
LOG_FILE="/var/log/patch_manager.log"

# Function to log messages
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    log_message "Error: This script must be run as root"
    exit 1
fi

# Run the Python patch manager
log_message "Starting patch manager"
python3 /path/to/patch_manager.py

# Check exit status
if [ $? -eq 0 ]; then
    log_message "Patch manager completed successfully"
else
    log_message "Error: Patch manager failed"
    exit 1
fi

# Restart services if necessary
log_message "Restarting services"
systemctl restart apache2 nginx mysql

log_message "Patch management process completed"
