import json
import gzip
import numpy as np
import matplotlib.pyplot as plt

# ** CHANGE MINS THRESHOLD HERE ** #
minute_limit = 5
numb_of_interval = 100
batch_size = 10


def is_non_speaking_subtitle(subtitle):
    return subtitle.startswith('[') and subtitle.endswith(']')

def load_and_process_data(input_file_name, total, minute):
    mean_time_deltas = []

    with gzip.open(input_file_name, 'rt') as input_file:  # Adjusted for gzip
        for line in input_file:
            total += 1
            data = json.loads(line)
            duration = data["duration"]
            if duration < minute * 60:
                continue
            mean_time_delta = calculate_mean_time_delta(data)
            mean_time_deltas.append(mean_time_delta)

    return mean_time_deltas

def calculate_mean_time_delta(data):
    subtitles_t_start = data["subtitles_t_start"]
    subtitles_t_end = data["subtitles_t_end"]
    subtitles_words = data["subtitles_words"]

    time_deltas = []
    i = 0
    while i < len(subtitles_words) - 1:
        if is_non_speaking_subtitle(subtitles_words[i+1]):
            if i+2 < len(subtitles_t_start):
                time_deltas.append(subtitles_t_start[i+2] - subtitles_t_end[i])
                i += 2
            else:
                break
        else:
            time_deltas.append(subtitles_t_start[i+1] - subtitles_t_end[i])
            i += 1

    return np.mean(time_deltas)

def plot_cumulative_distribution(interval_count, mean_time_deltas, min_val, max_val, minute):
    interval_size = (max_val - min_val) / interval_count
    counts = [0] * interval_count

    for delta in mean_time_deltas:
        if min_val <= delta < max_val:
            idx = int((delta - min_val) / interval_size)
            if idx == interval_count:
                idx -= 1
            counts[idx] += 1

    cumulative_counts = np.cumsum(counts)
    total_videos = len(mean_time_deltas)

    bin_edges = [min_val + i * interval_size for i in range(interval_count + 1)]
    plt.figure(figsize=(20, 5))
    plt.plot(bin_edges[:-1], cumulative_counts, marker='o', linestyle='-')

    plt.title('Cumulative Distribution of Average Subtitle Time Gap')
    plt.xlabel('Average Subtitle Time Gap (sec)')
    plt.ylabel('Total Number of Videos')
    ticks = np.arange(0, max_val + 0.025, 0.025)
    plt.xticks(ticks)
    plt.axhline(total_videos, color='green', linestyle='--', label=f'Total videos longer than {minute} mins: {total_videos}')
    plt.legend(loc="upper right", bbox_to_anchor=(1, 0.85))
    plt.grid(False)
    plt.savefig(f"cumulative_plot_{minute}mins.png")

    return total_videos

all_mean_time_deltas = []
total_amount = 0

for batch_start in range(0, 1024, batch_size):
    batch_end = batch_start + batch_size

    for file_number in range(batch_start, batch_end):
        file_number_str = f"{file_number:04d}"
        input_file_name = f"./../../shanw25/data/YT1B/metadata/yttemporal1b_train_{file_number_str}of1024.jsonl.gz"

        current_file_mean_time_deltas = load_and_process_data(input_file_name, total_amount, minute_limit)
        all_mean_time_deltas.extend(current_file_mean_time_deltas)

        # Output progress after processing each file
        print(f"Processed file {file_number_str}")

    print(f"Processed files {batch_start} to {batch_end - 1}")

print("All files processed..")

# Once all files are processed, plot the cumulative distribution
min_val = min(all_mean_time_deltas)
max_val = 0.7
filtered_amount = plot_cumulative_distribution(numb_of_interval, all_mean_time_deltas, min_val, max_val, minute_limit)
print(f"Total amount videos are {filtered_amount} / {total_amount}.")