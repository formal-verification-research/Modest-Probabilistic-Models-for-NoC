#!/usr/bin/env python3
"""
Script to analyze .time.txt files in result subdirectories.
Extracts total elapsed times and maximum memory usage per subdirectory.
"""

import os
import re
from pathlib import Path
from datetime import timedelta
from collections import defaultdict


def parse_time_to_seconds(time_str):
    """Convert HH:MM:SS.SS format to seconds."""
    try:
        parts = time_str.split(':')
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = float(parts[2])
        return hours * 3600 + minutes * 60 + seconds
    except (ValueError, IndexError):
        return None


def seconds_to_time_str(seconds):
    """Convert seconds back to HH:MM:SS.SS format."""
    hours = int(seconds) // 3600
    remaining = int(seconds) % 3600
    minutes = remaining // 60
    secs = seconds - (hours * 3600 + minutes * 60)
    return f"{hours:02d}:{minutes:02d}:{secs:05.2f}"


def process_time_file(filepath):
    """
    Extract total elapsed time and peak memory usage from a .time.txt file.
    
    Returns:
        tuple: (total_time_in_seconds, max_memory_mb) or (None, None) if parsing fails
    """
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Extract total elapsed time
        time_match = re.search(r'Total elapsed time:\s*(\d{2}:\d{2}:\d{2}\.\d{2})', content)
        total_time_seconds = None
        if time_match:
            total_time_seconds = parse_time_to_seconds(time_match.group(1))
        
        # Extract all peak memory usage lines and find the maximum
        memory_matches = re.findall(r'Peak memory usage:\s*(\d+)\s*MB', content)
        max_memory_mb = None
        if memory_matches:
            max_memory_mb = max(int(m) for m in memory_matches)
        
        return total_time_seconds, max_memory_mb
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return None, None


def main():
    """Main function to analyze all .time.txt files in subdirectories."""
    
    # Base results directory
    results_dir = Path(__file__).parent.parent / 'results'
    
    if not results_dir.exists():
        print(f"Results directory not found: {results_dir}")
        return
    
    # Dictionary to store stats per subdirectory and noise type
    # Structure: {subdir_name: {noise_type: {'total_time': 0, 'max_memory': 0, 'file_count': 0}}}
    stats_by_dir = defaultdict(lambda: defaultdict(lambda: {'total_time': 0, 'max_memory': 0, 'file_count': 0}))
    
    # Find all .time.txt files
    time_files = sorted(results_dir.glob('*/*.time.txt'))
    
    if not time_files:
        print("No .time.txt files found in subdirectories")
        return
    
    # Process each file
    for filepath in time_files:
        subdir_name = filepath.parent.name
        filename = filepath.stem.lower()
        
        # Determine noise type from filename
        noise_type = None
        if 'inductive' in filename:
            noise_type = 'inductive'
        elif 'resistive' in filename:
            noise_type = 'resistive'
        else:
            noise_type = 'unknown'
        
        total_time, max_memory = process_time_file(filepath)
        
        if total_time is not None and max_memory is not None:
            stats_by_dir[subdir_name][noise_type]['total_time'] += total_time
            stats_by_dir[subdir_name][noise_type]['max_memory'] = max(
                stats_by_dir[subdir_name][noise_type]['max_memory'],
                max_memory
            )
            stats_by_dir[subdir_name][noise_type]['file_count'] += 1
    
    # Print results
    print("=" * 80)
    print("RESULTS ANALYSIS SUMMARY")
    print("=" * 80)
    print()
    
    # Sort by directory name
    for subdir_name in sorted(stats_by_dir.keys()):
        noise_stats = stats_by_dir[subdir_name]
        total_files = sum(s['file_count'] for s in noise_stats.values())
        
        print(f"Directory: {subdir_name}")
        print(f"  Files processed: {total_files}")
        
        # Print stats for each noise type in a consistent order
        for noise_type in sorted(noise_stats.keys()):
            stats = noise_stats[noise_type]
            total_time_str = seconds_to_time_str(stats['total_time'])
            max_memory = stats['max_memory']
            
            if stats['file_count'] > 0:
                print(f"  Total elapsed time - {noise_type}: {total_time_str} ({stats['total_time']:.2f} seconds)")
                print(f"  Maximum memory usage - {noise_type}: {max_memory} MB")
        
        print()
    
    # Print overall summary
    print("=" * 80)
    print("OVERALL SUMMARY")
    print("=" * 80)
    
    # Calculate totals across all directories and noise types
    total_all_time = 0
    max_all_memory = 0
    total_file_count = 0
    all_noise_types = set()
    
    for subdir_stats in stats_by_dir.values():
        for noise_type, stats in subdir_stats.items():
            total_all_time += stats['total_time']
            max_all_memory = max(max_all_memory, stats['max_memory'])
            total_file_count += stats['file_count']
            all_noise_types.add(noise_type)
    
    print(f"Total directories: {len(stats_by_dir)}")
    print(f"Total files processed: {total_file_count}")
    
    # Print summary by noise type
    for noise_type in sorted(all_noise_types):
        noise_total_time = 0
        noise_max_memory = 0
        noise_file_count = 0
        
        for subdir_stats in stats_by_dir.values():
            if noise_type in subdir_stats:
                stats = subdir_stats[noise_type]
                noise_total_time += stats['total_time']
                noise_max_memory = max(noise_max_memory, stats['max_memory'])
                noise_file_count += stats['file_count']
        
        if noise_file_count > 0:
            print(f"Total elapsed time - {noise_type}: {seconds_to_time_str(noise_total_time)}")
            print(f"Maximum memory usage - {noise_type}: {noise_max_memory} MB")
    
    print(f"Cumulative elapsed time (across all files): {seconds_to_time_str(total_all_time)}")
    print(f"Overall maximum memory usage: {max_all_memory} MB")


if __name__ == "__main__":
    main()
