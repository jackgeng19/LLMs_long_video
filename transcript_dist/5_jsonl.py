import json
import gzip
import os
import numpy as np

# Define the number of files to process in each batch
batch_size = 10
total_rows_added = 0

# Iterate over the range of file numbers (0000 to 1023) in batches
for batch_start in range(512, 1023, batch_size):
    batch_end = batch_start + batch_size

    # Process the current batch of files
    for file_number in range(batch_start, batch_end):
        # Format the file number as a four-digit string
        file_number_str = f"{file_number:04d}"

        input_file_name = f"./../../shanw25/data/YT1B/metadata/yttemporal1b_train_{file_number_str}of1024.jsonl.gz"
        output_file_name = f"./filtered_metadata/filtered_yttemporal1b_train_{file_number_str}of1024.jsonl.gz"

        # Open the gzipped input file for reading and the gzipped output file for writing
        with gzip.open(input_file_name, 'rt') as gz_input_file, gzip.open(output_file_name, 'wt') as gz_output_file:
            # Process each line in the JSONL file
            for line in gz_input_file:
                data = json.loads(line)
                duration = data["duration"]

                if duration < 600:
                    continue

                subtitles_t_start = data["subtitles_t_start"]
                subtitles_t_end = data["subtitles_t_end"]

                # Calculate time deltas between consecutive words
                time_deltas = [start - end for start, end in zip(subtitles_t_start[1:], subtitles_t_end[:-1])]

                # Calculate the mean of the time deltas
                mean_time_delta = np.mean(time_deltas)

                if mean_time_delta > 0.001665:
                    continue

                total_rows_added += 1

                # Write the qualified video data to the new gzipped JSONL file
                gz_output_file.write(json.dumps(data) + '\n')

    # Output progress after processing each batch
    print(f"Processed files {batch_start} to {batch_end - 1}")
    print(f"Total rows added: {total_rows_added}")

print("All files processed.")
