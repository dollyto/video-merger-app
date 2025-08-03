#!/usr/bin/env python3
"""
Example script demonstrating how to use the VideoMerger class programmatically.
"""

from video_merger import VideoMerger
import os


def example_concatenate():
    """Example of concatenating videos sequentially."""
    print("=== Concatenate Example ===")
    
    # Create merger instance
    merger = VideoMerger(output_dir="output")
    
    # Example video files (replace with your actual video files)
    video_files = [
        "video1.mp4",
        "video2.mp4", 
        "video3.mp4"
    ]
    
    # Check if example files exist
    existing_files = [f for f in video_files if os.path.exists(f)]
    
    if not existing_files:
        print("No video files found. Please add some video files to test with.")
        print("Example files to create: video1.mp4, video2.mp4, video3.mp4")
        return
    
    print(f"Found {len(existing_files)} video files: {existing_files}")
    
    # Merge videos using concatenate method
    result = merger.merge_videos(
        video_paths=existing_files,
        output_name="concatenated_video.mp4",
        method="concatenate"
    )
    
    if result:
        print(f"✅ Concatenation successful! Output: {result}")
    else:
        print("❌ Concatenation failed!")


def example_overlay():
    """Example of overlaying videos (picture-in-picture)."""
    print("\n=== Overlay Example ===")
    
    # Create merger instance
    merger = VideoMerger(output_dir="output")
    
    # Example video files (replace with your actual video files)
    video_files = [
        "main_video.mp4",  # Background video
        "overlay1.mp4",    # Overlay video 1
        "overlay2.mp4"     # Overlay video 2
    ]
    
    # Check if example files exist
    existing_files = [f for f in video_files if os.path.exists(f)]
    
    if len(existing_files) < 2:
        print("Need at least 2 video files for overlay method.")
        print("Please add main_video.mp4 and overlay1.mp4 to test with.")
        return
    
    print(f"Found {len(existing_files)} video files: {existing_files}")
    
    # Merge videos using overlay method
    result = merger.merge_videos(
        video_paths=existing_files,
        output_name="overlay_video.mp4",
        method="overlay"
    )
    
    if result:
        print(f"✅ Overlay successful! Output: {result}")
    else:
        print("❌ Overlay failed!")


def example_video_info():
    """Example of getting video information."""
    print("\n=== Video Info Example ===")
    
    merger = VideoMerger()
    
    # Example video file
    video_file = "video1.mp4"
    
    if os.path.exists(video_file):
        info = merger.get_video_info(video_file)
        if info:
            print(f"Video: {info['filename']}")
            print(f"Duration: {info['duration']:.2f} seconds")
            print(f"Size: {info['size']}")
            print(f"FPS: {info['fps']}")
        else:
            print(f"Could not get info for {video_file}")
    else:
        print(f"Video file {video_file} not found")


def example_supported_formats():
    """Example of listing supported formats."""
    print("\n=== Supported Formats ===")
    
    merger = VideoMerger()
    formats = merger.list_supported_formats()
    
    print("Supported video formats:")
    for fmt in formats:
        print(f"  {fmt}")


def main():
    """Run all examples."""
    print("Video Merger Examples")
    print("=" * 50)
    
    # List supported formats
    example_supported_formats()
    
    # Show video info (if file exists)
    example_video_info()
    
    # Try concatenate example
    example_concatenate()
    
    # Try overlay example
    example_overlay()
    
    print("\n" + "=" * 50)
    print("Examples completed!")
    print("\nTo use with your own videos:")
    print("1. Place your video files in the project directory")
    print("2. Update the file paths in the examples")
    print("3. Run the examples again")


if __name__ == "__main__":
    main() 