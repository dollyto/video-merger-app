# Video Merger & Audio to Video Converter

A web application for merging multiple videos and converting audio files to video with customizable backgrounds.

## Features

### Video Merger
- ✅ Upload multiple video files (MP4, AVI, MOV, MKV, WMV, FLV, WebM, M4V)
- ✅ Choose merge method (concatenate/overlay)
- ✅ Custom output filename
- ✅ Drag & drop interface
- ✅ Progress tracking

### Audio to Video Converter
- ✅ Upload audio files (MP3, WAV, AAC, M4A, FLAC, OGG, WMA)
- ✅ Customizable resolution (1920x1080 default)
- ✅ Adjustable FPS (30fps default)
- ✅ Custom background colors
- ✅ Real-time color preview

### System Features
- ✅ Modern, responsive UI
- ✅ File validation and size limits
- ✅ Automatic cleanup (30 minutes)
- ✅ Download functionality
- ✅ Error handling and timeout management
- ✅ Memory usage monitoring
- ✅ Health check endpoint

## Deployment

### Render.com (Optimized for Free Tier)

This application is specifically optimized for Render.com's free tier with the following constraints:

- **Memory**: 512MB RAM
- **Storage**: 1GB disk space
- **Timeout**: 15 minutes for web requests

#### Optimizations Made:
1. **Reduced file size limits**: 100MB per file, 200MB total
2. **Single worker configuration**: Prevents memory issues
3. **5-minute processing timeout**: Prevents worker timeouts
4. **Automatic garbage collection**: Manages memory usage
5. **File cleanup**: Removes temporary files after processing

#### Quick Deploy:
1. Fork this repository
2. Connect to Render.com
3. Deploy as a Web Service
4. Use the provided `render.yaml` configuration

### Local Development

```bash
# Clone the repository
git clone <repository-url>
cd video-merger

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Access the application at `http://localhost:8080`

## Usage

### Video Merging
1. Go to the "Merge Videos" tab
2. Upload 2 or more video files
3. Choose merge method:
   - **Concatenate**: Videos play sequentially
   - **Overlay**: Picture-in-picture style
4. Set custom output filename (optional)
5. Click "Merge Videos"
6. Download the merged video when complete

### Audio to Video Conversion
1. Go to the "Audio to Video" tab
2. Upload an audio file
3. Customize settings:
   - Resolution (width x height)
   - FPS (frames per second)
   - Background color (RGB values)
4. Set custom output filename (optional)
5. Click "Convert"
6. Download the video when complete

## File Size Limits

### Free Tier (Render.com)
- **Individual files**: 100MB maximum
- **Total upload**: 200MB maximum
- **Processing timeout**: 5 minutes

### Local Development
- **Individual files**: 500MB maximum
- **Total upload**: 1GB maximum
- **No processing timeout**

## Health Monitoring

Visit `/health` to check:
- System status
- Available disk space
- Memory usage
- Current file size limits

## Troubleshooting

### Common Issues

#### Worker Timeout
- **Cause**: Video processing taking too long
- **Solution**: Use smaller files or reduce video quality

#### Memory Issues (SIGKILL)
- **Cause**: Application using too much memory
- **Solution**: Restart the service or use smaller files

#### File Upload Failures
- **Cause**: File too large or unsupported format
- **Solution**: Check file size and format requirements

### Best Practices

1. **File Preparation**:
   - Compress videos before uploading
   - Use MP4 format for best compatibility
   - Keep files under 50MB for reliable processing

2. **Processing**:
   - Process one request at a time
   - Wait for completion before starting new requests
   - Monitor the health endpoint

3. **Monitoring**:
   - Check logs for memory usage
   - Monitor disk space
   - Watch for timeout errors

## Environment Variables

```bash
MAX_FILE_SIZE=100000000          # 100MB per file
MAX_TOTAL_SIZE=200000000        # 200MB total
GUNICORN_TIMEOUT=300            # 5 minutes
GUNICORN_WORKERS=1              # Single worker
SECRET_KEY=your-secret-key      # Flask secret key
```

## Supported Formats

### Video Input
- MP4, AVI, MOV, MKV, WMV, FLV, WebM, M4V

### Audio Input
- MP3, WAV, AAC, M4A, FLAC, OGG, WMA

### Output
- MP4 (H.264 video, AAC audio)

## Technical Details

### Dependencies
- **Flask**: Web framework
- **MoviePy**: Video processing
- **Gunicorn**: WSGI server
- **psutil**: System monitoring

### Architecture
- Single-threaded processing for memory efficiency
- Automatic file cleanup
- Memory usage monitoring
- Timeout handling for long operations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
1. Check the `/health` endpoint
2. Review the deployment guide
3. Check Render.com logs
4. Try with smaller test files first 