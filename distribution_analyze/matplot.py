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
                    if duration >= 600:
                        durations.append(duration)

    if len(durations) >= 2:
        durations.sort(reverse=True)
        second_max_duration = durations[1]
        print("Second maximum duration:", second_max_duration)

    # Set custom color and edgecolor
    plt.hist(durations, bins=range(600, 1260, 10), edgecolor='white', color='#1f77b4', alpha=0.8, rwidth=0.8)
    plt.title(TITLE, fontweight='bold')
    plt.xlabel(X_LABEL)
    plt.ylabel(Y_LABEL)

    # Add a background color
    plt.gca().set_facecolor('#f2f2f2')

    # Add total count of videos to the upper right corner
    plt.text(0.95, 0.95, f'Total Videos longer than 10 mins: {len(durations)}',
             horizontalalignment='right', verticalalignment='center', transform=plt.gca().transAxes)

    # Adjust spacing
    plt.tight_layout()
    plt.show()


def main() -> int:
    generate_plot('/Users/jackgengqc/Desktop/Dr.Gedas/output',
                  'Distribution of Video Durations (YT-1B Dataset)',
                  'Duration (seconds)',
                  'Count')
    return 0


if __name__ == '__main__':
    sys.exit(main())
