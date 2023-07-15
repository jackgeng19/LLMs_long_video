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

    plt.hist(filtered_durations, bins=range(10, 61, 1), edgecolor='white', color='#1f77b4', alpha=0.8, rwidth=0.8)
    plt.title(TITLE, fontweight='bold')
    plt.xlabel(X_LABEL)
    plt.ylabel(Y_LABEL)
    plt.gca().set_facecolor('#f2f2f2')

    counts, bins, _ = plt.hist(filtered_durations, bins=range(10, 61, 1), edgecolor='white', color='#1f77b4', alpha=0.8, rwidth=0.8)
    top_counts_indices = (-counts).argsort()[:2]  # Get indices of top two counts
    for index in top_counts_indices:
        count = int(counts[index])
        bin_value = bins[index] + 0.5
        plt.annotate(f'{count}', xy=(bin_value, count), xytext=(0, 10), textcoords='offset points',
                     ha='center', va='bottom')

    plt.tight_layout()
    # plt.savefig('video_durations.png', dpi=300)
    plt.show()


def main() -> int:
    generate_plot('/Users/jackgengqc/Desktop/Dr.Gedas/output',
                  'Distribution of Video Durations (YT-1B Dataset)',
                  'Duration (seconds)',
                  'Count')
    return 0


if __name__ == '__main__':
    sys.exit(main())
