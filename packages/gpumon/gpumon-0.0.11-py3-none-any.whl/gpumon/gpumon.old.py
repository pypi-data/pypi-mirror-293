import os
import subprocess
import sys
import time
import re
import psutil
import argparse
import signal

# Check for GPUtil and install if not found
try:
    import GPUtil
except ImportError:
    print("GPUtil not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "gputil"])
    import GPUtil

# ANSI escape codes for cursor visibility
HIDE_CURSOR = '\033[?25l'
SHOW_CURSOR = '\033[?25h'

def move_cursor_up(lines):
    print(f"\033[{lines}A", end='')

def get_gpu_clock_frequencies(gpu_id):
    try:
        output = subprocess.check_output(
            ["nvidia-smi", "-i", str(gpu_id), "--query-gpu=clocks.gr,clocks.max.gr", "--format=csv,noheader,nounits"]
        ).decode()
        current_freq, max_freq = map(int, re.findall(r'\d+', output))
        return current_freq, max_freq
    except Exception as e:
        print("Error fetching GPU clock frequencies:", e)
        return 0, 0

def get_gpu_fan_speed(gpu_id):
    try:
        output = subprocess.check_output(
            ["nvidia-smi", "-i", str(gpu_id), "--query-gpu=fan.speed", "--format=csv,noheader,nounits"]
        ).decode().strip()
        fan_speed = int(re.findall(r'\d+', output)[0])
        return fan_speed
    except Exception as e:
        print("Error fetching GPU fan speed:", e)
        return 0

def get_gpu_power_usage(gpu_id):
    try:
        output = subprocess.check_output(
            ["nvidia-smi", "-i", str(gpu_id), "--query-gpu=power.draw", "--format=csv,noheader,nounits"]
        ).decode().strip()
        power_usage = float(re.findall(r'\d+\.\d+', output)[0])
        return power_usage
    except Exception as e:
        print("Error fetching GPU power usage:", e)
        return 0.0

def print_progress_bar(percentage, max_value=100, bar_length=6, bar_character='█', empty_character='░', color='\033[92m'):
    filled_length = int(round(bar_length * percentage / float(max_value)))
    bar = bar_character * filled_length + empty_character * (bar_length - filled_length)
    return color + bar + '\033[0m'

def get_color_code(value, thresholds):
    if value < thresholds[0]:
        return '\033[94m'  # Blue
    elif value < thresholds[1]:
        return '\033[92m'  # Green
    else:
        return '\033[91m'  # Red

def print_gpu_stats(gpu, current_freq, max_freq, fan_speed, power_usage, bar_length):
    temp_color = get_color_code(gpu.temperature, [50, 70])
    power_color = get_color_code(power_usage, [100, 200])  # Assuming thresholds for power usage
    fan_color = get_color_code(fan_speed, [50, 70])

    gpu_name_color = '\033[96m'  # Bright cyan color for GPU name and ID
    title_color = '\033[93m'     # Bright yellow color for titles
    reset_color = '\033[0m'      # Reset color

    temp_bar = print_progress_bar(gpu.temperature, max_value=100, bar_length=bar_length, color=temp_color)
    load_bar = print_progress_bar(gpu.load * 100, bar_length=bar_length, color=temp_color)
    mem_bar = print_progress_bar((gpu.memoryUsed / gpu.memoryTotal) * 100, bar_length=bar_length, color=temp_color)
    freq_bar = print_progress_bar(current_freq, max_freq, bar_length=bar_length, color=temp_color)

    print(f"{gpu_name_color}[{gpu.id}]-{gpu.name:<24}{reset_color} {title_color}Fan:{reset_color} {fan_color}{fan_speed:>3}%{reset_color} {title_color}Power:{reset_color} {power_color}{power_usage:>6.2f} W{reset_color} {title_color}Temp:{reset_color} {int(gpu.temperature):>3}C [{temp_bar}] {title_color}Load:{reset_color} {int(gpu.load * 100):>3}% [{load_bar}] {title_color}Mem:{reset_color} {int(gpu.memoryUsed):>5}/{int(gpu.memoryTotal):<5} MB [{mem_bar}] {title_color}Freq:{reset_color} {int(current_freq):>4}/{int(max_freq):<4} MHz [{freq_bar}]", end=' ')

def main():
    parser = argparse.ArgumentParser(description="Real-time GPU monitoring script.")
    parser.add_argument('--bar-length', type=int, default=5, help='Length of the progress bars.')
    parser.add_argument('--gpus-per-row', type=int, default=1, help='Number of GPUs to display per row.')
    parser.add_argument('--refresh-rate', type=float, default=0.5, help='Refresh rate in seconds.')
    parser.add_argument('--continuous', type=bool, default=True, help='Set to False for one-time status display.')

    args = parser.parse_args()

    def signal_handler(sig, frame):
        print(SHOW_CURSOR)  # Show cursor
        print("\nGoodbye!")
        sys.exit(0)

    # Handle signals to gracefully exit
    signal.signal(signal.SIGINT, signal_handler)  # Handle Ctrl+C
    signal.signal(signal.SIGTSTP, signal_handler) # Handle Ctrl+Z

    print(HIDE_CURSOR)  # Hide cursor
    first_run = True
    lines_to_move_up = 0

    try:
        while True:
            gpus = GPUtil.getGPUs()
            if not first_run:
                move_cursor_up(lines_to_move_up)
            lines_to_move_up = 0
            gpu_count = 0
            for gpu in gpus:
                current_freq, max_freq = get_gpu_clock_frequencies(gpu.id)
                fan_speed = get_gpu_fan_speed(gpu.id)
                power_usage = get_gpu_power_usage(gpu.id)
                print_gpu_stats(gpu, current_freq, max_freq, fan_speed, power_usage, args.bar_length)
                gpu_count += 1
                if gpu_count % args.gpus_per_row == 0:
                    print()
            if gpu_count % args.gpus_per_row != 0:
                print()
            lines_to_move_up = (gpu_count // args.gpus_per_row + (1 if gpu_count % args.gpus_per_row > 0 else 0)) * 1  # Adjust based on the output complexity
            first_run = False
            if not args.continuous:
                break
            time.sleep(args.refresh_rate)  # Refresh rate
    except KeyboardInterrupt:
        signal_handler(None, None)
    finally:
        print(SHOW_CURSOR)  # Ensure cursor is shown when exiting

if __name__ == "__main__":
    main()
