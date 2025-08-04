#!/usr/bin/env python3
"""
Video Merger - A Python tool to merge/stitch multiple videos into a single video file.
"""

import os
import sys
import argparse
import gc
import psutil
from pathlib import Path
from typing import List, Optional, Tuple
import logging

from moviepy.editor import VideoFileClip, concatenate_videoclips
import numpy as np


class VideoMerger:
    """A class to handle merging multiple video files into a single video."""
    
    def __init__(self, output_dir: str = "output"):
        """
        Initialize the VideoMerger.
        
        Args:
            output_dir (str): Directory to save merged videos
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def get_memory_usage(self):
        """Get current memory usage in MB."""
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024
    
    def log_memory_usage(self, stage: str):
        """Log memory usage at different stages."""
        memory_mb = self.get_memory_usage()
        self.logger.info(f"Memory usage at {stage}: {memory_mb:.1f} MB")
    
    def validate_video_file(self, file_path: str) -> bool:
        """
        Validate if a file is a valid video file.
        
        Args:
            file_path (str): Path to the video file
            
        Returns:
            bool: True if valid video file, False otherwise
        """
        try:
            clip = VideoFileClip(file_path)
            clip.close()
            return True
        except Exception as e:
            self.logger.error(f"Invalid video file {file_path}: {e}")
            return False
    
    def get_video_info(self, file_path: str) -> Optional[dict]:
        """
        Get information about a video file.
        
        Args:
            file_path (str): Path to the video file
            
        Returns:
            dict: Video information including duration, size, fps
        """
        try:
            clip = VideoFileClip(file_path)
            info = {
                'path': file_path,
                'duration': clip.duration,
                'size': clip.size,
                'fps': clip.fps,
                'filename': Path(file_path).name
            }
            clip.close()
            return info
        except Exception as e:
            self.logger.error(f"Error getting video info for {file_path}: {e}")
            return None
    
    def merge_videos(self, video_paths: List[str], output_name: str = "merged_video.mp4", 
                    method: str = "concatenate") -> Optional[str]:
        """
        Merge multiple videos into a single video file.
        
        Args:
            video_paths (List[str]): List of video file paths to merge
            output_name (str): Name of the output video file
            method (str): Merging method ('concatenate' for sequential, 'overlay' for picture-in-picture)
            
        Returns:
            str: Path to the merged video file, or None if failed
        """
        if not video_paths:
            self.logger.error("No video files provided")
            return None
        
        self.log_memory_usage("start")
        
        # Validate all video files
        valid_videos = []
        for video_path in video_paths:
            if self.validate_video_file(video_path):
                valid_videos.append(video_path)
            else:
                self.logger.warning(f"Skipping invalid video file: {video_path}")
        
        if not valid_videos:
            self.logger.error("No valid video files found")
            return None
        
        self.logger.info(f"Found {len(valid_videos)} valid video files")
        
        # Display video information
        total_duration = 0
        for video_path in valid_videos:
            info = self.get_video_info(video_path)
            if info:
                self.logger.info(f"Video: {info['filename']} - Duration: {info['duration']:.2f}s - Size: {info['size']}")
                total_duration += info['duration']
        
        self.logger.info(f"Total duration will be: {total_duration:.2f}s")
        
        try:
            if method == "concatenate":
                return self._concatenate_videos(valid_videos, output_name)
            elif method == "overlay":
                return self._overlay_videos(valid_videos, output_name)
            else:
                self.logger.error(f"Unknown method: {method}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error merging videos: {e}")
            return None
        finally:
            # Force garbage collection
            gc.collect()
            self.log_memory_usage("end")
    
    def _concatenate_videos(self, video_paths: List[str], output_name: str) -> str:
        """
        Concatenate videos sequentially.
        
        Args:
            video_paths (List[str]): List of video file paths
            output_name (str): Output file name
            
        Returns:
            str: Path to the merged video
        """
        self.logger.info("Starting video concatenation...")
        self.log_memory_usage("concatenate_start")
        
        clips = []
        try:
            # Load all video clips
            for i, video_path in enumerate(video_paths):
                self.logger.info(f"Loading video {i+1}/{len(video_paths)}: {Path(video_path).name}")
                clip = VideoFileClip(video_path)
                clips.append(clip)
                self.log_memory_usage(f"loaded_video_{i+1}")
            
            # Concatenate clips
            self.logger.info("Concatenating videos...")
            final_clip = concatenate_videoclips(clips, method="compose")
            self.log_memory_usage("concatenated")
            
            # Save the merged video
            output_path = self.output_dir / output_name
            self.logger.info(f"Saving merged video to: {output_path}")
            final_clip.write_videofile(
                str(output_path),
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                verbose=False,
                logger=None
            )
            
            self.logger.info(f"Video merging completed successfully!")
            self.logger.info(f"Output file: {output_path}")
            
            return str(output_path)
            
        except Exception as e:
            self.logger.error(f"Error in concatenation: {e}")
            raise
        finally:
            # Clean up clips
            try:
                if 'final_clip' in locals():
                    final_clip.close()
                for clip in clips:
                    clip.close()
            except Exception as e:
                self.logger.error(f"Error closing clips: {e}")
            
            # Force garbage collection
            gc.collect()
            self.log_memory_usage("concatenate_end")
    
    def _overlay_videos(self, video_paths: List[str], output_name: str) -> str:
        """
        Overlay videos (picture-in-picture style).
        
        Args:
            video_paths (List[str]): List of video file paths
            output_name (str): Output file name
            
        Returns:
            str: Path to the merged video
        """
        self.logger.info("Starting video overlay...")
        self.log_memory_usage("overlay_start")
        
        if len(video_paths) < 2:
            self.logger.error("Overlay method requires at least 2 videos")
            return None
        
        main_clip = None
        overlay_clips = []
        
        try:
            # Load the main video (first video)
            main_clip = VideoFileClip(video_paths[0])
            
            # Load overlay videos
            for i, video_path in enumerate(video_paths[1:], 1):
                self.logger.info(f"Loading overlay video {i}: {Path(video_path).name}")
                clip = VideoFileClip(video_path)
                # Resize overlay videos to be smaller
                clip = clip.resize(width=main_clip.w // 4, height=main_clip.h // 4)
                overlay_clips.append(clip)
                self.log_memory_usage(f"loaded_overlay_{i}")
            
            # Position overlay videos in corners
            positions = [
                ('top-left', (0, 0)),
                ('top-right', (main_clip.w - overlay_clips[0].w, 0)),
                ('bottom-left', (0, main_clip.h - overlay_clips[0].h)),
                ('bottom-right', (main_clip.w - overlay_clips[0].w, main_clip.h - overlay_clips[0].h))
            ]
            
            # Create composite video
            final_clip = main_clip
            for i, (clip, (pos_name, pos)) in enumerate(zip(overlay_clips, positions)):
                if i < len(positions):
                    self.logger.info(f"Adding overlay {i+1} at {pos_name}")
                    final_clip = final_clip.set_position(pos).set_duration(clip.duration)
                    final_clip = final_clip.set_position(pos)
            
            # Save the merged video
            output_path = self.output_dir / output_name
            self.logger.info(f"Saving merged video to: {output_path}")
            final_clip.write_videofile(
                str(output_path),
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                verbose=False,
                logger=None
            )
            
            self.logger.info(f"Video overlay completed successfully!")
            self.logger.info(f"Output file: {output_path}")
            
            return str(output_path)
            
        except Exception as e:
            self.logger.error(f"Error in overlay: {e}")
            raise
        finally:
            # Clean up clips
            try:
                if 'final_clip' in locals():
                    final_clip.close()
                if main_clip:
                    main_clip.close()
                for clip in overlay_clips:
                    clip.close()
            except Exception as e:
                self.logger.error(f"Error closing clips: {e}")
            
            # Force garbage collection
            gc.collect()
            self.log_memory_usage("overlay_end")
    
    def list_supported_formats(self) -> List[str]:
        """
        Get list of supported video formats.
        
        Returns:
            List[str]: List of supported video file extensions
        """
        return ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v']


def main():
    """Main function to handle command line arguments and run the video merger."""
    parser = argparse.ArgumentParser(
        description="Merge multiple videos into a single video file",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python video_merger.py video1.mp4 video2.mp4 video3.mp4
  python video_merger.py *.mp4 -o my_merged_video.mp4
  python video_merger.py video1.mp4 video2.mp4 -m overlay
        """
    )
    
    parser.add_argument(
        'videos',
        nargs='*',
        help='Video files to merge'
    )
    
    parser.add_argument(
        '-o', '--output',
        default='merged_video.mp4',
        help='Output video filename (default: merged_video.mp4)'
    )
    
    parser.add_argument(
        '-m', '--method',
        choices=['concatenate', 'overlay'],
        default='concatenate',
        help='Merging method: concatenate (sequential) or overlay (picture-in-picture) (default: concatenate)'
    )
    
    parser.add_argument(
        '-d', '--output-dir',
        default='output',
        help='Output directory (default: output)'
    )
    
    parser.add_argument(
        '--list-formats',
        action='store_true',
        help='List supported video formats'
    )
    
    args = parser.parse_args()
    
    # Create video merger instance
    merger = VideoMerger(output_dir=args.output_dir)
    
    if args.list_formats:
        formats = merger.list_supported_formats()
        print("Supported video formats:")
        for fmt in formats:
            print(f"  {fmt}")
        return
    
    # Check if video files exist
    valid_videos = []
    for video_path in args.videos:
        if os.path.exists(video_path):
            valid_videos.append(video_path)
        else:
            print(f"Warning: Video file not found: {video_path}")
    
    if not args.list_formats and not valid_videos:
        print("Error: No valid video files provided")
        sys.exit(1)
    
    # Merge videos
    if valid_videos:
        print(f"Merging {len(valid_videos)} videos using {args.method} method...")
        result = merger.merge_videos(valid_videos, args.output, args.method)
    else:
        result = None
    
    if result:
        print(f"\n✅ Video merging completed successfully!")
        print(f"📁 Output file: {result}")
    else:
        print("\n❌ Video merging failed!")
        sys.exit(1)


if __name__ == "__main__":
    main() 