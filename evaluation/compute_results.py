#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import csv
import argparse
from collections import defaultdict
from math import sqrt
import matplotlib.pyplot as plt
from collections import Counter

def compute_pearson(x, y):
    n = len(x)
    if n == 0:
        return float('nan')
    sum_x = sum(x)
    sum_y = sum(y)
    sum_x2 = sum(val ** 2 for val in x)
    sum_y2 = sum(val ** 2 for val in y)
    sum_xy = sum(a * b for a, b in zip(x, y))

    numerator = sum_xy - (sum_x * sum_y / n)
    denominator = sqrt((sum_x2 - (sum_x ** 2) / n) * (sum_y2 - (sum_y ** 2) / n))
    if denominator == 0:
        return float('nan')
    return numerator / denominator

def compute_stddev(sum_vals, sum_squares, count):
    if count == 0:
        return float('nan')
    mean = sum_vals / count
    variance = (sum_squares / count) - (mean ** 2)
    return sqrt(variance) if variance >= 0 else float('nan')

def main():
    parser = argparse.ArgumentParser(description="Compute average metrics, standard deviations, generate plots, and optionally correlation.")
    parser.add_argument("tsv_file", nargs="?", type=str, help="Input TSV file (or stdin if omitted)")
    parser.add_argument("--correlate", nargs=2, metavar=("METRIC1", "METRIC2"),
                        help="Compute correlation between two metrics")
    parser.add_argument("--show-plots", action="store_true", help="Display plots instead of saving them to files")
    args = parser.parse_args()

    input_stream = open(args.tsv_file, 'r') if args.tsv_file else sys.stdin
    reader = csv.reader(input_stream, delimiter='\t')

    header = next(reader)
    if len(header) < 3:
        print("Input must have at least three columns: filename, system, and at least one metric.")
        return

    metric_names = header[2:]
    system_data = defaultdict(lambda: defaultdict(lambda: [0.0, 0.0, 0]))
    flat_metric_data = defaultdict(list)

    for row in reader:
        system = row[1]
        values = row[2:]

        for metric, value in zip(metric_names, values):
            try:
                val = float(value)
                data = system_data[system][metric]
                data[0] += val
                data[1] += val ** 2
                data[2] += 1
                flat_metric_data[metric].append(val)
            except ValueError:
                continue

    # Prepare headers
    extended_headers = []
    for metric in metric_names:
        extended_headers.extend([f"{metric}_avg", f"{metric}_std"])
    print("System\t" + "\t".join(extended_headers))

    # Print values and collect for plotting
    metric_plot_data = defaultdict(lambda: {"systems": [], "averages": [], "stddevs": []})
    for system in sorted(system_data):
        row_values = []
        for metric in metric_names:
            total, total_sq, count = system_data[system][metric]
            avg = total / count if count > 0 else float('nan')
            stddev = compute_stddev(total, total_sq, count)
            row_values.extend([f"{avg:.4f}", f"{stddev:.4f}"])
            metric_plot_data[metric]["systems"].append(system)
            metric_plot_data[metric]["averages"].append(avg)
            metric_plot_data[metric]["stddevs"].append(stddev)
        print(f"{system}\t" + "\t".join(row_values))

    # Plotting
    for metric, data in metric_plot_data.items():
        systems = data["systems"]
        averages = data["averages"]
        stddevs = data["stddevs"]

        plt.figure(figsize=(8, 6))
        plt.bar(systems, averages, yerr=stddevs, capsize=5, color='skyblue', edgecolor='black')
        plt.ylabel(metric)
        plt.title(f"{metric} by System")
        plt.xticks(rotation=45)
        plt.tight_layout()

        if args.show_plots:
            plt.show()
        else:
            plt.savefig(f"{metric}_by_system.png")
        plt.close()

    # Compute correlation if requested
    if args.correlate:
        m1, m2 = args.correlate
        if m1 not in flat_metric_data or m2 not in flat_metric_data:
            print(f"\nError: One or both metrics '{m1}' and '{m2}' not found.")
            return
        x = flat_metric_data[m1]
        y = flat_metric_data[m2]
        if len(x) != len(y):
            print(f"\nError: Unequal number of values for {m1} and {m2}")
            return
        corr = compute_pearson(x, y)
        print(f"\nPearson correlation between {m1} and {m2}: {corr:.4f}")


        # Count occurrences of each (x, y) pair
        coord_counts = Counter(zip(x, y))
        unique_coords = list(coord_counts.keys())
        frequencies = [coord_counts[pt] for pt in unique_coords]
        x_unique, y_unique = zip(*unique_coords)

        plt.figure(figsize=(7, 6))
        scatter = plt.scatter(
            x_unique,
            y_unique,
            s=[20 + 30 * f for f in frequencies],  # Scale size by frequency
            c=frequencies,
            cmap='viridis',
            edgecolor='black',
            alpha=0.8
        )
        plt.xlabel(m1)
        plt.ylabel(m2)
        plt.title(f"Correlation between {m1} and {m2}\nPearson r = {corr:.4f}")
        plt.colorbar(scatter, label='Frequency')
        plt.grid(True)
        plt.tight_layout()

        if args.show_plots:
            plt.show()
        else:
            plt.savefig(f"correlation_{m1}_vs_{m2}.png")
        plt.close()

if __name__ == "__main__":
    main()


