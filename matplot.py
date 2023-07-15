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

    # Set custom color and edgecolor
    plt.hist(filtered_durations, bins=range(10, 61, 1), edgecolor='white', color='#1f77b4', alpha=0.8, rwidth=0.8)
    plt.title(TITLE)
    plt.xlabel(X_LABEL)
    plt.ylabel(Y_LABEL)


    # Add a background color
    plt.gca().set_facecolor('#f2f2f2')

    # Adjust spacing
    plt.tight_layout()

    # # Save the plot as an image file
    # plt.savefig('video_durations.png', dpi=300)

    # Show the plot
    plt.show()


def main() -> int:
    generate_plot('/Users/jackgengqc/Desktop/Dr.Gedas/output',
                  'Distribution of Video Durations (YT-1B Dataset)',
                  'Duration (seconds)',
                  'Count')
    return 0


if __name__ == '__main__':
    sys.exit(main())
