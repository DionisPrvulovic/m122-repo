#!/bin/bash

# Define the paths to the files and directory
current_dir=$(dirname "$(readlink -f "$0")")
currency_cron_log="$current_dir/currency_cron.log"
dump_dir="$current_dir/dump"
currency_log="$dump_dir/currency.log"
table_png="$dump_dir/table.png"

# Function to delete a file if it exists
delete_file() {
  if [ -f "$1" ]; then
    rm "$1"
    echo "Deleted: $1"
  else
    echo "File not found: $1"
  fi
}

# Delete the currency_cron.log if it exists
delete_file "$currency_cron_log"

# Check if the dump directory exists
if [ -d "$dump_dir" ]; then
  # Delete the currency.log and table.png if they exist
  delete_file "$currency_log"
  delete_file "$table_png"
else
  echo "Directory not found: $dump_dir"
fi
