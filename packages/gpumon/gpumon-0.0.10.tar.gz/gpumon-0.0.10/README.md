# GPU Monitor (`gpumon`)

`gpumon` is a real-time GPU monitoring tool designed to display various metrics for NVIDIA GPUs, including temperature, fan speed, memory usage, load, and power consumption. It provides color-coded output for easy identification of critical values and can operate in both continuous and one-time monitoring modes.

## Features

- **Real-time Monitoring**: Continuously monitors NVIDIA GPU statistics.
- **Detailed Metrics**: Displays temperature, fan speed, memory usage, GPU load, and power consumption.
- **Color-Coded Output**: Highlights different levels of each metric with distinct colors for easy visualization.
- **Customizable**: Users can adjust the bar length and refresh rate.
- **Single or Continuous Mode**: Option to display GPU status once or continuously update.

## Installation

### Prerequisites

- **Python 3.x**
- **NVIDIA drivers**
- **`nvidia-smi` command-line utility**

### Install using pip

To install `gpumon`, use the following command:

```bash
pip install gpumon
```

## Usage

Run the tool using the command line:

### Continuous Monitoring (default mode)

```bash
gpumon
```

This command will start `gpumon` in continuous monitoring mode, refreshing the display every 0.5 seconds.

### One-Time Status Display

To display the GPU status once and then exit:

```bash
gpumon --continuous False
```

### Custom Bar Length and Refresh Rate

You can customize the appearance and behavior of the monitoring display:

```bash
gpumon --bar-length 5 --refresh-rate 1.0
```

- `--bar-length`: Sets the length of the progress bars (default is 5).
- `--refresh-rate`: Sets the refresh rate in seconds (default is 0.5 seconds).

### Command-Line Arguments

- `--bar-length`: The length of the progress bars. This controls how much detail is displayed in the bar representation.
- `--refresh-rate`: The rate in seconds at which the display refreshes.
- `--continuous`: Set to `False` for a one-time status display, otherwise the tool runs continuously (default is `True`).

## Example Output

```
[0]-NVIDIA A100              Fan:  70% Power: 250.00 W Temp:  72C [███░░] Load:  90% [███░░] Mem:  80000/80000 MB [██████] Freq: 1500/2100 MHz [███░░]
[1]-NVIDIA A100              Fan:  75% Power: 245.00 W Temp:  73C [███░░] Load:  85% [███░░] Mem:  78000/80000 MB [██████] Freq: 1550/2100 MHz [███░░]
[2]-NVIDIA A100              Fan:  65% Power: 260.00 W Temp:  70C [███░░] Load:  80% [███░░] Mem:  77000/80000 MB [██████] Freq: 1600/2100 MHz [███░░]
[3]-NVIDIA A100              Fan:  68% Power: 255.00 W Temp:  71C [███░░] Load:  75% [███░░] Mem:  76000/80000 MB [██████] Freq: 1650/2100 MHz [███░░]
[4]-NVIDIA A100              Fan:  72% Power: 240.00 W Temp:  74C [███░░] Load:  95% [███░░] Mem:  80000/80000 MB [██████] Freq: 1700/2100 MHz [███░░]
[5]-NVIDIA A100              Fan:  60% Power: 250.00 W Temp:  72C [███░░] Load:  85% [███░░] Mem:  79000/80000 MB [██████] Freq: 1500/2100 MHz [███░░]
[6]-NVIDIA A100              Fan:  70% Power: 250.00 W Temp:  72C [███░░] Load:  90% [███░░] Mem:  80000/80000 MB [██████] Freq: 1500/2100 MHz [███░░]
[7]-NVIDIA A100              Fan:  70% Power: 250.00 W Temp:  72C [███░░] Load:  90% [███░░] Mem:  80000/80000 MB [██████] Freq: 1500/2100 MHz [███░░]
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### Notes

- Ensure that the `nvidia-smi` tool is available on your system, as `gpumon` relies on it to gather GPU metrics.


