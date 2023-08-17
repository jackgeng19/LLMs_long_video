import csv
import json
import gzip
import shutil
import os
import numpy as np

# Define the number of files to process in each batch
batch_size = 10
total_rows_added = 0

# Iterate over the range of file numbers (0000 to 1023) in batches
for batch_start in range(513, 1025, batch_size):
    batch_end = batch_start + batch_size

    # Process the current batch of files
    for file_number in range(batch_start, batch_end):
        # Format the file number as a four-digit string
        file_number_str = f"{file_number:04d}"

        input_file_name = f"./../../shanw25/data/YT1B/metadata/yttemporal1b_train_{file_number_str}of1024.jsonl.gz"

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
                # writer = csv.writer(csv_file)

                # Write the header row in the CSV file
                # writer.writerow(['URL', 'Duration(second)','Standard Deviation'])

                # Process each line in the JSONL file
                for line in json_file:
                    data = json.loads(line)
                    link = data["webpage_url"]
                    duration = data["duration"]

                    try:
                        words_per_30s = data["_words_per_30s"]
                    except KeyError:
                        continue  # Skip this entry if "_words_per_30s" is missing

                    # Skip videos with duration < 300 seconds
                    if len (words_per_30s) < 20 or duration < 600:
                        continue

                    # Possible solution:
                    # Find delta between each 30s and 1.  std of these deltas 2. mean of these deltas (lower mean means a less sparse transcript)
                    # to see whether the speaker is speaking in a constant speed(pace).

            

                    std_deviation = np.std(words_per_30s)

                    if std_deviation >= 20:
                        continue
                    
                    total_rows_added += 1
                    # Write the data row in the CSV file
                    # writer.writerow([link, duration, std_deviation])
        os.remove(unzipped_file_name)

    # Output progress after processing each batch
    print(f"Processed files {batch_start} to {batch_end - 1}")

    print(f"Total rows added: {total_rows_added}")

print("All files processed.")
