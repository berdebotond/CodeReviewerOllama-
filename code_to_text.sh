#!/bin/bash

# Output file
output_file="file_contents.txt"

# Clear the output file
> "$output_file"

# Exclude the output file as well as the other criteria
find . -type f ! -path '*/node_modules/*' ! -name '*.json' ! -path '*/.*' ! -path './.*' ! -path "./${output_file}" | while read file; do
    if [[ -f "$file" ]] && ! file --mime "$file" | grep -qE 'binary|executable'; then
        echo "Path: $file" >> "$output_file"
        cat "$file" >> "$output_file"
        echo -e "\n________________________________________________________________________________\n" >> "$output_file"
    fi
done

echo "Process completed. Check $output_file for the output."
