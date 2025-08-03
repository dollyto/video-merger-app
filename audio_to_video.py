#!/usr/bin/env python3
"""
Audio to Video Converter - Converts audio-only .mov files to video files with black pixels.
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Optional
import logging

from moviepy import AudioFileClip, ColorClip, CompositeVideoClip
import numpy as np


class AudioToVideoConverter:
    """A class to convert audio-only files to video files with black pixels."""
    
    def __init__(self, output_dir: str = "output"):
        """
        Initialize the AudioToVideoConverter.
        
        Args:
            output_dir (str): Directory to save converted videos
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def validate_audio_file(self, file_path: str) -> bool:
        """
        Validate if a file is a valid audio file.
        
        Args:
            file_path (str): Path to the audio file
            
        Returns:
            bool: True if valid audio file, False otherwise
        """
        try:
            clip = AudioFileClip(file_path)
            clip.close()
            return True
        except Exception as e:
            self.logger.error(f"Invalid audio file {file_path}: {e}")
            return False
    
    def get_audio_info(self, file_path: str) -> Optional[dict]:
        """
        Get information about an audio file.
        
        Args:
            file_path (str): Path to the audio file
            
        Returns:
            dict: Audio information including duration, sample rate
        """
        try:
            clip = AudioFileClip(file_path)
            info = {
                'path': file_path,
                'duration': clip.duration,
                'fps': clip.fps,
                'filename': Path(file_path).name,
                'sample_rate': getattr(clip, 'fps', None)  # Audio sample rate
            }
            clip.close()
            return info
        except Exception as e:
            self.logger.error(f"Error getting audio info for {file_path}: {e}")
            return None
    
    def convert_audio_to_video(self, audio_path: str, output_name: str = None, 
                              resolution: tuple = (1920, 1080), fps: int = 30,
                              color: tuple = (0, 0, 0)) -> Optional[str]:
        """
        Convert audio file to video file with black pixels.
        
        Args:
            audio_path (str): Path to the audio file
            output_name (str): Name of the output video file (optional)
            resolution (tuple): Video resolution (width, height) - default 1920x1080
            fps (int): Frames per second - default 30
            color (tuple): RGB color for video background - default black (0,0,0)
            
        Returns:
            str: Path to the converted video file, or None if failed
        """
        if not self.validate_audio_file(audio_path):
            self.logger.error(f"Invalid audio file: {audio_path}")
            return None
        
        # Get audio info
        audio_info = self.get_audio_info(audio_path)
        if not audio_info:
            return None
        
        self.logger.info(f"Converting audio: {audio_info['filename']}")
        self.logger.info(f"Duration: {audio_info['duration']:.2f}s")
        self.logger.info(f"Resolution: {resolution[0]}x{resolution[1]}")
        self.logger.info(f"FPS: {fps}")
        
        try:
            # Load audio clip
            self.logger.info("Loading audio file...")
            audio_clip = AudioFileClip(audio_path)
            
            # Create black video clip
            self.logger.info("Creating video background...")
            video_clip = ColorClip(
                size=resolution,
                color=color,
                duration=audio_clip.duration
            )
            
            # Combine audio and video
            self.logger.info("Combining audio and video...")
            final_clip = video_clip.with_audio(audio_clip)
            
            # Set the FPS for the final clip
            final_clip = final_clip.with_fps(fps)
            
            # Generate output filename if not provided
            if output_name is None:
                audio_name = Path(audio_path).stem
                output_name = f"{audio_name}_video.mp4"
            
            # Save the video
            output_path = self.output_dir / output_name
            self.logger.info(f"Saving video to: {output_path}")
            
            final_clip.write_videofile(
                str(output_path),
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                logger=None  # Suppress moviepy's verbose output
            )
            
            # Clean up
            final_clip.close()
            audio_clip.close()
            video_clip.close()
            
            self.logger.info(f"✅ Audio to video conversion completed successfully!")
            self.logger.info(f"📁 Output file: {output_path}")
            
            return str(output_path)
            
        except Exception as e:
            self.logger.error(f"Error converting audio to video: {e}")
            return None
    
    def batch_convert(self, audio_paths: list, resolution: tuple = (1920, 1080), 
                     fps: int = 30, color: tuple = (0, 0, 0)) -> list:
        """
        Convert multiple audio files to video files.
        
        Args:
            audio_paths (list): List of audio file paths
            resolution (tuple): Video resolution (width, height)
            fps (int): Frames per second
            color (tuple): RGB color for video background
            
        Returns:
            list: List of successfully converted video file paths
        """
        successful_conversions = []
        
        for i, audio_path in enumerate(audio_paths, 1):
            self.logger.info(f"Processing file {i}/{len(audio_paths)}: {Path(audio_path).name}")
            
            result = self.convert_audio_to_video(
                audio_path=audio_path,
                resolution=resolution,
                fps=fps,
                color=color
            )
            
            if result:
                successful_conversions.append(result)
            else:
                self.logger.warning(f"Failed to convert: {audio_path}")
        
        return successful_conversions
    
    def list_supported_formats(self) -> list:
        """
        Get list of supported audio formats.
        
        Returns:
            list: List of supported audio file extensions
        """
        return ['.mov', '.mp3', '.wav', '.aac', '.m4a', '.flac', '.ogg', '.wma']


def main():
    """Main function to handle command line arguments and run the converter."""
    parser = argparse.ArgumentParser(
        description="Convert audio-only files to video files with black pixels",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python audio_to_video.py audio.mov
  python audio_to_video.py audio.mov -o video.mp4
  python audio_to_video.py audio.mov -r 1280 720 -f 24
  python audio_to_video.py *.mov --batch
        """
    )
    
    parser.add_argument(
        'audio_files',
        nargs='*',
        help='Audio files to convert'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output video filename (default: auto-generated)'
    )
    
    parser.add_argument(
        '-r', '--resolution',
        nargs=2,
        type=int,
        default=[1920, 1080],
        metavar=('WIDTH', 'HEIGHT'),
        help='Video resolution (default: 1920 1080)'
    )
    
    parser.add_argument(
        '-f', '--fps',
        type=int,
        default=30,
        help='Frames per second (default: 30)'
    )
    
    parser.add_argument(
        '-c', '--color',
        nargs=3,
        type=int,
        default=[0, 0, 0],
        metavar=('R', 'G', 'B'),
        help='Background color RGB values (default: 0 0 0 for black)'
    )
    
    parser.add_argument(
        '-d', '--output-dir',
        default='output',
        help='Output directory (default: output)'
    )
    
    parser.add_argument(
        '--batch',
        action='store_true',
        help='Process multiple files in batch mode'
    )
    
    parser.add_argument(
        '--list-formats',
        action='store_true',
        help='List supported audio formats'
    )
    
    args = parser.parse_args()
    
    # Create converter instance
    converter = AudioToVideoConverter(output_dir=args.output_dir)
    
    if args.list_formats:
        formats = converter.list_supported_formats()
        print("Supported audio formats:")
        for fmt in formats:
            print(f"  {fmt}")
        return
    
    # Check if audio files exist
    valid_files = []
    for audio_path in args.audio_files:
        if os.path.exists(audio_path):
            valid_files.append(audio_path)
        else:
            print(f"Warning: Audio file not found: {audio_path}")
    
    if not args.list_formats and not valid_files:
        print("Error: No valid audio files provided")
        sys.exit(1)
    
    # Convert audio to video
    if valid_files:
        if args.batch or len(valid_files) > 1:
            print(f"Converting {len(valid_files)} audio files to video...")
            results = converter.batch_convert(
                audio_paths=valid_files,
                resolution=tuple(args.resolution),
                fps=args.fps,
                color=tuple(args.color)
            )
            
            if results:
                print(f"\n✅ Successfully converted {len(results)} files:")
                for result in results:
                    print(f"  📁 {result}")
            else:
                print("\n❌ No files were converted successfully!")
                sys.exit(1)
        else:
            # Single file conversion
            print(f"Converting audio to video...")
            result = converter.convert_audio_to_video(
                audio_path=valid_files[0],
                output_name=args.output,
                resolution=tuple(args.resolution),
                fps=args.fps,
                color=tuple(args.color)
            )
            
            if result:
                print(f"\n✅ Audio to video conversion completed successfully!")
                print(f"📁 Output file: {result}")
            else:
                print("\n❌ Audio to video conversion failed!")
                sys.exit(1)


if __name__ == "__main__":
    main() 