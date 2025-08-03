#!/bin/bash
# Video Merger Activation Script

echo "🎬 Video Merger - Activation Script"
echo "=================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python3 -m venv venv"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import moviepy" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

echo "✅ Virtual environment activated!"
echo ""
echo "Available commands:"
echo "  # Video Merger:"
echo "  python video_merger.py --help          # Show video merger help"
echo "  python video_merger_gui.py             # Launch video merger GUI"
echo ""
echo "  # Audio to Video Converter:"
echo "  python audio_to_video.py --help        # Show audio converter help"
echo "  python audio_to_video_gui.py           # Launch audio converter GUI"
echo ""
echo "  # Examples:"
echo "  python example.py                      # Run examples"
echo ""
echo "Example usage:"
echo "  # Video merging:"
echo "  python video_merger.py video1.mp4 video2.mp4"
echo "  python video_merger.py *.mp4 -o merged.mp4"
echo ""
echo "  # Audio to video conversion:"
echo "  python audio_to_video.py audio.mov"
echo "  python audio_to_video.py audio.mov -r 1280 720 -f 24"
echo ""

# Keep the virtual environment active
echo "Virtual environment is now active. Run 'deactivate' to exit."
echo "" 