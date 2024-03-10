
# App Screenshot Generator

## Description
This tool allows users to automatically resize and fill screenshots to fit various specified dimensions, catering to different device screens like phones and tablets. It supports multiple image formats and provides options for fill color, including automatic detection based on a pixel's color.

## Features
- Resizes images to fit specified dimensions for different device screens.
- Allows custom fill colors or automatic fill color detection.
- Batch processes images from a specified directory.

## Requirements
- Python 3.x
- ImageMagick (for `convert` and `identify` commands)

## Installation
1. Ensure Python 3.x and ImageMagick are installed on your system.
2. Clone this repository to your local machine.
3. Navigate to the project directory.


### Example
```
python generate.py --screenshots ./path/to/screenshots --output ./path/to/output
```

## Contributing
Contributions are welcome! Please fork the repository and submit pull requests with your changes.
