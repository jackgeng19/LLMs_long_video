import csv
import json
import gzip
import shutil
import os
import numpy as np

# Iterate over the range of file numbers (0000 to 1023) in batches
file_number_str = "0000"

input_file_name = f"./..shanw25/data/YT1B/metadata/yttemporal1b_train_{file_number_str}of1024.jsonl.gz"

# Build the temporary unzipped file name
unzipped_file_name = f"./yttemporal1b_train_{file_number_str}of1024.jsonl"

# Extract the JSONL file from the gzip file
with gzip.open(input_file_name, 'rb') as gz_file:
    with open(unzipped_file_name, 'wb') as json_file:
        shutil.copyfileobj(gz_file, json_file)

# Open the JSONL file for reading
with open(unzipped_file_name, 'r') as json_file:
    # Build the output CSV file name
    output_file_name = f"./{file_number_str}.csv"

    # Open the CSV file for writing
    with open(output_file_name, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        # Write the header row in the CSV file

        # Process each line in the JSONL file
        for line in json_file:
            data = json.loads(line)
            subtitles_t_start = data["_subtitles_t_start"]
            subtitles_t_end = data["_subtitles_t_end"]
            # Calculate time deltas between consecutive words
            time_deltas = [end - start for start, end in zip(subtitles_t_start[:-1], subtitles_t_end[1:])]

            # Calculate the mean of the time deltas
            mean_time_delta = sum(time_deltas) / len(time_deltas)

            # if mean_time_delta >= 20:
            #     continue

            print(mean_time_delta)

    os.remove(unzipped_file_name)

# Output progress after processing each batch
print("All files processed.")
