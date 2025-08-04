# Video Merger Deployment Guide

## Render.com Deployment

This application is optimized for Render.com's free tier with the following constraints:

### Resource Limits (Free Tier)
- **Memory**: 512MB RAM
- **CPU**: Limited processing power
- **Storage**: 1GB disk space
- **Timeout**: 15 minutes for web requests

### Optimizations Made

1. **Reduced File Size Limits**:
   - Max file size: 100MB per file
   - Max total size: 200MB per request

2. **Gunicorn Configuration**:
   - Single worker to prevent memory issues
   - 5-minute timeout for video processing
   - Max 10 requests per worker before restart

3. **Memory Management**:
   - Automatic garbage collection
   - File cleanup after processing
   - Memory usage monitoring

4. **Error Handling**:
   - Timeout handling for long operations
   - Graceful cleanup on errors
   - Better error messages

### Troubleshooting

#### Worker Timeout Issues
If you see `WORKER TIMEOUT` errors:

1. **Reduce file sizes**: Upload smaller video files
2. **Check file formats**: Use MP4 format for best compatibility
3. **Monitor memory**: Check `/health` endpoint for system status

#### Memory Issues
If you see `SIGKILL` errors:

1. **Restart the service**: Memory leaks are cleaned up on restart
2. **Wait between requests**: Allow time for garbage collection
3. **Use smaller videos**: Reduce resolution or duration

#### File Upload Issues
If uploads fail:

1. **Check file size**: Ensure files are under 100MB
2. **Check file format**: Use supported formats only
3. **Check total size**: Multiple files must be under 200MB total

### Health Check

Visit `/health` to check:
- System status
- Available disk space
- Memory usage
- Current file size limits

### Best Practices

1. **File Preparation**:
   - Compress videos before uploading
   - Use MP4 format for best compatibility
   - Keep individual files under 50MB for reliable processing

2. **Processing**:
   - Process one request at a time
   - Wait for completion before starting new requests
   - Monitor the health endpoint

3. **Monitoring**:
   - Check logs for memory usage
   - Monitor disk space
   - Watch for timeout errors

### Environment Variables

The following environment variables can be adjusted:

```yaml
MAX_FILE_SIZE: 100000000  # 100MB per file
MAX_TOTAL_SIZE: 200000000  # 200MB total
GUNICORN_TIMEOUT: 300  # 5 minutes
GUNICORN_WORKERS: 1  # Single worker
```

### Upgrading to Paid Tier

For better performance, consider upgrading to a paid tier which provides:
- More memory (1GB+)
- More CPU resources
- Longer timeouts
- Better reliability

### Support

If issues persist:
1. Check the application logs in Render.com dashboard
2. Monitor the `/health` endpoint
3. Try with smaller test files first
4. Consider upgrading to a paid tier for production use 