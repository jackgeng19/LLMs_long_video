import os
import csv
import matplotlib.pyplot as plt

# Set the path to the folder containing the CSV files
folder_path = '/Users/jackgengqc/Desktop/Dr.Gedas/output'

# Initialize a list to store the durations of videos
durations = []

# Iterate over each CSV file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        
        # Read the CSV file and extract the durations
        with open(file_path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header row
            for row in reader:
                duration = int(row[1])
                durations.append(duration)

# Filter the durations to only include videos with a duration less than or equal to 60 seconds
filtered_durations = [duration for duration in durations if duration <= 60]

# Plot the duration distribution using a histogram
plt.hist(filtered_durations, bins=range(0, 61, 5), edgecolor='none')
plt.title('Distribution of Video Durations (YT-1B Dataset)')
plt.xlabel('Duration (seconds)')
plt.ylabel('Count')
plt.show()
