# trackdir

**trackdir** is a Python package designed to monitor and track changes in a specified directory. It detects file creations, deletions, and modifications, providing real-time feedback either as a command-line tool or as a Python module in your scripts.

## Features

- **Real-Time Monitoring**: Instantly detects file creations, deletions, and modifications.
- **Flexible Usage**: Can be used both as a command-line tool and a Python module.
- **Detailed Change Information**: Returns detailed information about the type of change and the affected file.

## Installation

You can install the `trackdir` package using `pip`:

```bash
pip install trackdir
```

## Usage

### Command-Line Tool

To monitor a directory from the command line:

```bash
trackdir C:/telegram
```

This command will print details of any file changes (creation, deletion, modification) detected in the specified directory.

### Python Module

You can also use `trackdir` within your Python scripts:

```python
from trackdir import track_changes

# Track changes in the specified directory
change = track_changes("C:/telegram")
if change:
    event_type = change["type"]
    event_path = change["path"]
    if event_type == 'modified':
        print(f"File modified: {event_path}")
    elif event_type == 'created':
        print(f"File created: {event_path}")
    elif event_type == 'deleted':
        print(f"File deleted: {event_path}")
```

### Example

Here’s an example of using `trackdir` in a Python script:

```python
from trackdir import track_changes

directory_to_monitor = "C:/telegram"

# Continuously monitor the directory
while True:
    change = track_changes(directory_to_monitor)
    if change:
        event_type = change["type"]
        event_path = change["path"]
        print(f"Detected {event_type} at {event_path}")
```

### Contributions

Contributions are welcome! Please feel free to submit a pull request or open an issue on the [GitHub repository](https://github.com/bytebreach/trackdir).

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

Special thanks to the [watchdog](https://github.com/gorakhargosh/watchdog) library, which powers the file system monitoring capabilities of this package.

## Thank You

A heartfelt thank you to everyone who has supported and contributed to this project. Your encouragement and feedback are deeply appreciated and motivate me to continue improving and innovating.