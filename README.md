# Video Merger & Audio to Video Converter

A Python tool for merging/stitching multiple videos into a single video file, and converting audio-only files to video files with black pixels. Supports both command-line and graphical user interfaces.

## Features

### Video Merger
- **Multiple Merge Methods**: Concatenate videos sequentially or overlay them picture-in-picture style
- **Multiple Formats**: Supports MP4, AVI, MOV, MKV, WMV, FLV, WebM, and M4V
- **Dual Interface**: Command-line tool and GUI application
- **Progress Tracking**: Real-time progress updates and detailed logging
- **Error Handling**: Robust error handling with informative messages

### Audio to Video Converter
- **Audio to Video**: Convert audio-only files to video files with black pixels
- **Customizable Background**: Set custom RGB colors for video background
- **Multiple Resolutions**: Support for various video resolutions (1920x1080, 1280x720, etc.)
- **Batch Processing**: Convert multiple audio files at once
- **Audio Formats**: Supports MOV, MP3, WAV, AAC, M4A, FLAC, OGG, WMA

### General
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Dual Interface**: Both command-line and GUI applications available

## Installation

### Prerequisites

- Python 3.7 or higher
- FFmpeg (automatically installed with moviepy)

### Setup

1. **Clone or download the project**
   ```bash
   # If you have the files, skip this step
   git clone <repository-url>
   cd video-merger
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Video Merger

#### Command Line Interface

##### Basic Usage
```bash
# Merge multiple videos sequentially
python video_merger.py video1.mp4 video2.mp4 video3.mp4

# Specify output filename
python video_merger.py video1.mp4 video2.mp4 -o my_merged_video.mp4

# Use overlay method (picture-in-picture)
python video_merger.py video1.mp4 video2.mp4 -m overlay

# Specify output directory
python video_merger.py video1.mp4 video2.mp4 -d /path/to/output
```

#### Command Line Options
- `videos`: Video files to merge (required)
- `-o, --output`: Output video filename (default: merged_video.mp4)
- `-m, --method`: Merging method - 'concatenate' or 'overlay' (default: concatenate)
- `-d, --output-dir`: Output directory (default: output)
- `--list-formats`: List supported video formats

#### Examples
```bash
# Merge all MP4 files in current directory
python video_merger.py *.mp4

# Create picture-in-picture video
python video_merger.py main_video.mp4 overlay_video.mp4 -m overlay -o pip_video.mp4

# List supported formats
python video_merger.py --list-formats
```

#### Graphical User Interface

Launch the GUI application:
```bash
python video_merger_gui.py
```

##### GUI Features
- **Drag & Drop**: Add multiple video files easily
- **Visual Progress**: Real-time progress bar and status updates
- **Method Selection**: Choose between concatenate and overlay methods
- **Output Options**: Customize output filename and directory
- **Log Viewer**: See detailed processing logs

### Audio to Video Converter

#### Command Line Interface

##### Basic Usage
```bash
# Convert audio file to video with black background
python audio_to_video.py audio.mov

# Specify output filename
python audio_to_video.py audio.mov -o video.mp4

# Custom resolution and FPS
python audio_to_video.py audio.mov -r 1280 720 -f 24

# Custom background color (red)
python audio_to_video.py audio.mov -c 255 0 0

# Batch convert multiple files
python audio_to_video.py *.mov --batch
```

#### Command Line Options
- `audio_files`: Audio files to convert (required)
- `-o, --output`: Output video filename (optional, auto-generated if not provided)
- `-r, --resolution`: Video resolution WIDTH HEIGHT (default: 1920 1080)
- `-f, --fps`: Frames per second (default: 30)
- `-c, --color`: Background color RGB values (default: 0 0 0 for black)
- `-d, --output-dir`: Output directory (default: output)
- `--batch`: Process multiple files in batch mode
- `--list-formats`: List supported audio formats

#### Examples
```bash
# Convert audio file to video
python audio_to_video.py audio.mov

# Convert with custom settings
python audio_to_video.py audio.mov -r 1280 720 -f 24 -c 0 0 255

# Batch convert all MOV files
python audio_to_video.py *.mov --batch

# List supported formats
python audio_to_video.py --list-formats
```

#### Graphical User Interface

Launch the GUI application:
```bash
python audio_to_video_gui.py
```

##### GUI Features
- **File Selection**: Add multiple audio files easily
- **Customizable Settings**: Set resolution, FPS, and background color
- **Color Preview**: Visual preview of background color
- **Batch Processing**: Convert multiple files at once
- **Real-time Progress**: Progress bar and detailed logging
- **Output Options**: Customize output directory and filenames

## Merge Methods

### Concatenate (Sequential)
Joins videos end-to-end in the order specified. This is the default method.

```
Video 1 → Video 2 → Video 3 → Final Video
```

### Overlay (Picture-in-Picture)
Places additional videos as overlays on the main video. The first video becomes the background.

```
Main Video + Overlay 1 + Overlay 2 → Final Video
```

## Supported Formats

### Input Formats
- MP4 (.mp4)
- AVI (.avi)
- MOV (.mov)
- MKV (.mkv)
- WMV (.wmv)
- FLV (.flv)
- WebM (.webm)
- M4V (.m4v)

### Output Format
- MP4 (.mp4) with H.264 video codec and AAC audio codec

## Project Structure

```
video-merger/
├── venv/                    # Virtual environment
├── output/                  # Default output directory
├── video_merger.py         # Video merger command-line tool
├── video_merger_gui.py     # Video merger GUI application
├── audio_to_video.py       # Audio to video converter command-line tool
├── audio_to_video_gui.py   # Audio to video converter GUI application
├── example.py              # Example usage script
├── requirements.txt        # Python dependencies
├── activate.sh             # Easy activation script
└── README.md              # This file
```

## Dependencies

- **moviepy**: Video editing and processing
- **opencv-python**: Computer vision library for video processing
- **numpy**: Numerical computing library
- **python-dotenv**: Environment variable management

## Troubleshooting

### Common Issues

1. **"No module named 'moviepy'"**
   - Make sure you've activated the virtual environment
   - Run `pip install -r requirements.txt`

2. **"FFmpeg not found"**
   - MoviePy will automatically download FFmpeg on first use
   - If issues persist, install FFmpeg manually for your system

3. **"Permission denied"**
   - Ensure you have write permissions for the output directory
   - Try running with appropriate permissions

4. **"Video file not found"**
   - Check that video files exist and paths are correct
   - Use absolute paths if needed

### Performance Tips

- **Large Files**: For very large videos, consider processing in smaller chunks
- **Memory**: Ensure sufficient RAM for processing multiple videos simultaneously
- **Storage**: Make sure you have enough disk space for output files

## Development

### Adding New Features

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Testing

```bash
# Test video merger
python video_merger.py --help
python video_merger_gui.py

# Test audio to video converter
python audio_to_video.py --help
python audio_to_video_gui.py

# Run examples
python example.py
```

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## Support

If you encounter any issues or have questions, please:
1. Check the troubleshooting section above
2. Search existing issues
3. Create a new issue with detailed information

---

**Happy Video Merging! 🎬** 