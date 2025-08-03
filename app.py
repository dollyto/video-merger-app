#!/usr/bin/env python3
"""
Video Merger & Audio to Video Converter Web Application
"""

import os
import uuid
import tempfile
import shutil
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from werkzeug.utils import secure_filename
import logging
from datetime import datetime

from video_merger import VideoMerger
from audio_to_video import AudioToVideoConverter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# File size configuration (in bytes)
MAX_FILE_SIZE = int(os.environ.get('MAX_FILE_SIZE', 500 * 1024 * 1024))  # 500MB per file
MAX_TOTAL_SIZE = int(os.environ.get('MAX_TOTAL_SIZE', 1024 * 1024 * 1024))  # 1GB total
app.config['MAX_CONTENT_LENGTH'] = MAX_TOTAL_SIZE
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')

# Create necessary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Allowed file extensions
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'wmv', 'flv', 'webm', 'm4v'}
ALLOWED_AUDIO_EXTENSIONS = {'mov', 'mp3', 'wav', 'aac', 'm4a', 'flac', 'ogg', 'wma'}

def allowed_file(filename, allowed_extensions):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def format_file_size(size_bytes):
    """Format file size in human readable format."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes // 1024} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes // (1024 * 1024)} MB"
    else:
        return f"{size_bytes // (1024 * 1024 * 1024)} GB"

def cleanup_old_files():
    """Clean up old uploaded and output files (older than 1 hour)."""
    current_time = datetime.now()
    for folder in [app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER']]:
        if os.path.exists(folder):
            for filename in os.listdir(folder):
                filepath = os.path.join(folder, filename)
                if os.path.isfile(filepath):
                    file_time = datetime.fromtimestamp(os.path.getctime(filepath))
                    if (current_time - file_time).total_seconds() > 3600:  # 1 hour
                        try:
                            os.remove(filepath)
                            logger.info(f"Cleaned up old file: {filepath}")
                        except Exception as e:
                            logger.error(f"Error cleaning up {filepath}: {e}")

@app.route('/')
def index():
    """Main page with upload forms."""
    cleanup_old_files()
    return render_template('index.html')

@app.route('/merge-videos', methods=['POST'])
def merge_videos():
    """Handle video merging request."""
    try:
        if 'files' not in request.files:
            return jsonify({'error': 'No files uploaded'}), 400
        
        files = request.files.getlist('files')
        if not files or files[0].filename == '':
            return jsonify({'error': 'No files selected'}), 400
        
        # Validate files and check sizes
        video_files = []
        total_size = 0
        
        for file in files:
            if file and allowed_file(file.filename, ALLOWED_VIDEO_EXTENSIONS):
                # Check individual file size
                file.seek(0, 2)  # Seek to end
                file_size = file.tell()
                file.seek(0)  # Reset to beginning
                
                if file_size > MAX_FILE_SIZE:
                    return jsonify({'error': f'File {file.filename} is too large. Maximum size is {format_file_size(MAX_FILE_SIZE)}'}), 400
                
                total_size += file_size
                
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                video_files.append(filepath)
            else:
                return jsonify({'error': f'Invalid file type: {file.filename}'}), 400
        
        # Check total size
        if total_size > MAX_TOTAL_SIZE:
            return jsonify({'error': f'Total file size ({format_file_size(total_size)}) exceeds limit ({format_file_size(MAX_TOTAL_SIZE)})'}), 400
        
        if len(video_files) < 2:
            return jsonify({'error': 'At least 2 video files are required'}), 400
        
        # Get parameters
        method = request.form.get('method', 'concatenate')
        output_name = request.form.get('output_name', 'merged_video.mp4')
        
        # Create unique output filename
        unique_id = str(uuid.uuid4())[:8]
        output_filename = f"{Path(output_name).stem}_{unique_id}.mp4"
        
        # Merge videos
        merger = VideoMerger(output_dir=app.config['OUTPUT_FOLDER'])
        result = merger.merge_videos(video_files, output_filename, method)
        
        if result:
            # Clean up uploaded files
            for filepath in video_files:
                try:
                    os.remove(filepath)
                except:
                    pass
            
            return jsonify({
                'success': True,
                'message': 'Videos merged successfully!',
                'download_url': url_for('download_file', filename=Path(result).name),
                'filename': Path(result).name
            })
        else:
            return jsonify({'error': 'Failed to merge videos'}), 500
            
    except Exception as e:
        logger.error(f"Error merging videos: {e}")
        return jsonify({'error': f'Error: {str(e)}'}), 500

@app.route('/convert-audio', methods=['POST'])
def convert_audio():
    """Handle audio to video conversion request."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename, ALLOWED_AUDIO_EXTENSIONS):
            return jsonify({'error': f'Invalid file type: {file.filename}'}), 400
        
        # Check file size
        file.seek(0, 2)  # Seek to end
        file_size = file.tell()
        file.seek(0)  # Reset to beginning
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({'error': f'File {file.filename} is too large. Maximum size is {format_file_size(MAX_FILE_SIZE)}'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Get parameters
        resolution_width = int(request.form.get('resolution_width', 1920))
        resolution_height = int(request.form.get('resolution_height', 1080))
        fps = int(request.form.get('fps', 30))
        color_r = int(request.form.get('color_r', 0))
        color_g = int(request.form.get('color_g', 0))
        color_b = int(request.form.get('color_b', 0))
        output_name = request.form.get('output_name', '')
        
        # Create unique output filename
        unique_id = str(uuid.uuid4())[:8]
        if output_name:
            output_filename = f"{Path(output_name).stem}_{unique_id}.mp4"
        else:
            output_filename = f"{Path(filename).stem}_video_{unique_id}.mp4"
        
        # Convert audio to video
        converter = AudioToVideoConverter(output_dir=app.config['OUTPUT_FOLDER'])
        result = converter.convert_audio_to_video(
            audio_path=filepath,
            output_name=output_filename,
            resolution=(resolution_width, resolution_height),
            fps=fps,
            color=(color_r, color_g, color_b)
        )
        
        if result:
            # Clean up uploaded file
            try:
                os.remove(filepath)
            except:
                pass
            
            return jsonify({
                'success': True,
                'message': 'Audio converted to video successfully!',
                'download_url': url_for('download_file', filename=Path(result).name),
                'filename': Path(result).name
            })
        else:
            return jsonify({'error': 'Failed to convert audio to video'}), 500
            
    except Exception as e:
        logger.error(f"Error converting audio: {e}")
        return jsonify({'error': f'Error: {str(e)}'}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """Download a file from the output folder."""
    try:
        filepath = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        return jsonify({'error': 'Error downloading file'}), 500

@app.route('/health')
def health():
    """Health check endpoint for Render.com."""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False) 