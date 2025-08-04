#!/usr/bin/env python3
"""
Simple monitoring script for the Video Merger application.
"""

import psutil
import os
import time
from datetime import datetime

def get_system_info():
    """Get current system information."""
    # Memory info
    memory = psutil.virtual_memory()
    
    # Disk info
    disk = psutil.disk_usage('.')
    
    # CPU info
    cpu_percent = psutil.cpu_percent(interval=1)
    
    return {
        'timestamp': datetime.now().isoformat(),
        'memory': {
            'total_mb': round(memory.total / (1024 * 1024), 2),
            'available_mb': round(memory.available / (1024 * 1024), 2),
            'used_mb': round(memory.used / (1024 * 1024), 2),
            'percent': round(memory.percent, 2)
        },
        'disk': {
            'total_gb': round(disk.total / (1024**3), 2),
            'free_gb': round(disk.free / (1024**3), 2),
            'used_gb': round(disk.used / (1024**3), 2),
            'percent': round((disk.used / disk.total) * 100, 2)
        },
        'cpu_percent': round(cpu_percent, 2)
    }

def check_upload_directories():
    """Check upload and output directories."""
    directories = ['uploads', 'output']
    info = {}
    
    for dir_name in directories:
        if os.path.exists(dir_name):
            files = os.listdir(dir_name)
            total_size = 0
            for file in files:
                file_path = os.path.join(dir_name, file)
                if os.path.isfile(file_path):
                    total_size += os.path.getsize(file_path)
            info[dir_name] = {
                'file_count': len(files),
                'total_size_mb': round(total_size / (1024 * 1024), 2)
            }
        else:
            info[dir_name] = {'file_count': 0, 'total_size_mb': 0}
    
    return info

def main():
    """Main monitoring function."""
    print("Video Merger System Monitor")
    print("=" * 40)
    
    while True:
        try:
            # Get system info
            sys_info = get_system_info()
            
            # Get directory info
            dir_info = check_upload_directories()
            
            # Print status
            print(f"\n[{sys_info['timestamp']}]")
            print(f"Memory: {sys_info['memory']['used_mb']:.1f}MB / {sys_info['memory']['total_mb']:.1f}MB ({sys_info['memory']['percent']:.1f}%)")
            print(f"Disk: {sys_info['disk']['used_gb']:.1f}GB / {sys_info['disk']['total_gb']:.1f}GB ({sys_info['disk']['percent']:.1f}%)")
            print(f"CPU: {sys_info['cpu_percent']:.1f}%")
            
            print("\nDirectories:")
            for dir_name, info in dir_info.items():
                print(f"  {dir_name}: {info['file_count']} files, {info['total_size_mb']:.1f}MB")
            
            # Check for warnings
            warnings = []
            if sys_info['memory']['percent'] > 80:
                warnings.append("High memory usage!")
            if sys_info['disk']['percent'] > 80:
                warnings.append("High disk usage!")
            if sys_info['cpu_percent'] > 80:
                warnings.append("High CPU usage!")
            
            if warnings:
                print("\n⚠️  Warnings:")
                for warning in warnings:
                    print(f"  {warning}")
            
            print("\n" + "-" * 40)
            
            # Wait 30 seconds
            time.sleep(30)
            
        except KeyboardInterrupt:
            print("\nMonitoring stopped.")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(30)

if __name__ == "__main__":
    main() 