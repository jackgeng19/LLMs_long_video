import os
import csv
import sys
import matplotlib.pyplot as plt


def generate_plot(PATH, TITLE, X_LABEL, Y_LABEL):
    # Plot the duration distribution using a histogram
    durations = []

    for filename in os.listdir(PATH):
        if filename.endswith('.csv'):
            file_path = os.path.join(PATH, filename)
            
            with open(file_path, 'r') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip the header row
                for row in reader:
                    duration = int(row[1])
                    durations.append(duration)

    filtered_durations = [duration for duration in durations if duration <= 60]

    plt.hist(filtered_durations, bins=range(0, 61, 5), edgecolor='none')
    plt.title(TITLE)
    plt.xlabel(X_LABEL)
    plt.ylabel(Y_LABEL)
    plt.show()


def main() -> int:
    generate_plot('/Users/jackgengqc/Desktop/Dr.Gedas/output',
                  'Distribution of Video Durations (YT-1B Dataset)',
                  'Duration (seconds)',
                  'Count')
    return 0


if __name__ == '__main__':
    sys.exit(main())