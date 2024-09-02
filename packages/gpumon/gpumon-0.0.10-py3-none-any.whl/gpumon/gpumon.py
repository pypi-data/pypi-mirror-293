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
RED_COLOR = '\033[91m'
RESET_COLOR = '\033[0m'

def move_cursor_up(lines):
    print(f"\033[{lines}A", end='')

def get_gpu_clock_frequencies(gpu_id):
    try:
        output = subprocess.check_output(
            ["nvidia-smi", "-i", str(gpu_id), "--query-gpu=clocks.gr,clocks.max.gr", "--format=csv,noheader,nounits"]
        ).decode()
        current_freq, max_freq = map(int, re.findall(r'\d+', output))
        return current_freq, max_freq
    except Exception:
        return 0, 0

def get_gpu_fan_speed(gpu_id):
    try:
        output = subprocess.check_output(
            ["nvidia-smi", "-i", str(gpu_id), "--query-gpu=fan.speed", "--format=csv,noheader,nounits"]
        ).decode().strip()
        fan_speed = int(re.findall(r'\d+', output)[0])
        return fan_speed
    except Exception:
        return None

def get_gpu_power_usage(gpu_id):
    try:
        output = subprocess.check_output(
            ["nvidia-smi", "-i", str(gpu_id), "--query-gpu=power.draw", "--format=csv,noheader,nounits"]
        ).decode().strip()
        power_usage = float(re.findall(r'\d+\.\d+', output)[0])
        return power_usage
    except Exception:
        return None

def print_progress_bar(percentage, max_value=100, bar_length=6, bar_character='█', empty_character='░', color='\033[92m'):
    filled_length = int(round(bar_length * percentage / float(max_value)))
    bar = bar_character * filled_length + empty_character * (bar_length - filled_length)
    return color + bar + RESET_COLOR

def get_color_code(value, thresholds):
    if value is None:
        return RED_COLOR
    if value < thresholds[0]:
        return '\033[94m'  # Blue
    elif value < thresholds[1]:
        return '\033[92m'  # Green
    else:
        return '\033[91m'  # Red

def print_gpu_stats(gpu, current_freq, max_freq, fan_speed, power_usage, bar_length, max_name_length):
    temp_color = get_color_code(gpu.temperature, [50, 70])
    power_color = get_color_code(power_usage, [100, 200])
    fan_color = get_color_code(fan_speed, [50, 70])

    gpu_name_color = '\033[96m'  # Bright cyan color for GPU name and ID
    title_color = '\033[93m'     # Bright yellow color for titles

    temp_bar = print_progress_bar(gpu.temperature, max_value=100, bar_length=bar_length, color=temp_color)
    load_bar = print_progress_bar(gpu.load * 100, bar_length=bar_length, color=temp_color)
    mem_bar = print_progress_bar((gpu.memoryUsed / gpu.memoryTotal) * 100, bar_length=bar_length, color=temp_color)
    freq_bar = print_progress_bar(current_freq, max_freq, bar_length=bar_length, color=temp_color)

    fan_speed_display = f"{fan_speed:>3}%" if fan_speed is not None else f"{RED_COLOR} 00%{RESET_COLOR}"
    power_usage_display = f"{power_usage:>6.2f} W" if power_usage is not None else f"{RED_COLOR}--{RESET_COLOR}"
    current_freq_display = f"{int(current_freq):>4}" if current_freq != 0 else f"{RED_COLOR}--{RESET_COLOR}"
    max_freq_display = f"{int(max_freq):<4}" if max_freq != 0 else f"{RED_COLOR}--{RESET_COLOR}"

    gpu_name_padded = f"{gpu.name:<{max_name_length}}"

    print(f"{gpu_name_color}[{gpu.id}]-{gpu_name_padded}{RESET_COLOR} {title_color}Fan:{RESET_COLOR} {fan_color}{fan_speed_display}{RESET_COLOR} {title_color}Power:{RESET_COLOR} {power_color}{power_usage_display}{RESET_COLOR} {title_color}Temp:{RESET_COLOR} {int(gpu.temperature):>3}C [{temp_bar}] {title_color}Load:{RESET_COLOR} {int(gpu.load * 100):>3}% [{load_bar}] {title_color}Mem:{RESET_COLOR} {int(gpu.memoryUsed):>5}/{int(gpu.memoryTotal):<5} MB [{mem_bar}] {title_color}Freq:{RESET_COLOR} {current_freq_display}/{max_freq_display} MHz [{freq_bar}]", end=' ')

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
            max_name_length = max(len(gpu.name) for gpu in gpus)
            if not first_run:
                move_cursor_up(lines_to_move_up)
            lines_to_move_up = 0
            gpu_count = 0
            for gpu in gpus:
                current_freq, max_freq = get_gpu_clock_frequencies(gpu.id)
                fan_speed = get_gpu_fan_speed(gpu.id)
                power_usage = get_gpu_power_usage(gpu.id)
                print_gpu_stats(gpu, current_freq, max_freq, fan_speed, power_usage, args.bar_length, max_name_length)
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
