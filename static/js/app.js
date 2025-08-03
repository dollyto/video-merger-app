// Global variables
let currentDownloadUrl = '';
let currentFilename = '';
let selectedVideoFiles = [];
let selectedAudioFile = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    setupDragAndDrop();
    setupColorPreview();
    setupFileInputs();
});

// Setup drag and drop functionality
function setupDragAndDrop() {
    const videoUploadArea = document.getElementById('videoUploadArea');
    const audioUploadArea = document.getElementById('audioUploadArea');

    // Video upload area
    videoUploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        this.classList.add('dragover');
    });

    videoUploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        this.classList.remove('dragover');
    });

    videoUploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        this.classList.remove('dragover');
        const files = e.dataTransfer.files;
        console.log('Video files dropped:', files.length);
        handleVideoFiles(files);
    });

    // Audio upload area
    audioUploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        this.classList.add('dragover');
    });

    audioUploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        this.classList.remove('dragover');
    });

    audioUploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        this.classList.remove('dragover');
        const files = e.dataTransfer.files;
        console.log('Audio file dropped:', files.length);
        if (files.length > 0) {
            handleAudioFile(files[0]);
        }
    });
}

// Setup color preview functionality
function setupColorPreview() {
    const colorInputs = ['colorR', 'colorG', 'colorB'];
    const colorPreview = document.getElementById('colorPreview');

    colorInputs.forEach(id => {
        document.getElementById(id).addEventListener('input', function() {
            const r = document.getElementById('colorR').value || 0;
            const g = document.getElementById('colorG').value || 0;
            const b = document.getElementById('colorB').value || 0;
            colorPreview.style.background = `rgb(${r},${g},${b})`;
        });
    });
}

// Setup file input handlers
function setupFileInputs() {
    const videoFilesInput = document.getElementById('videoFiles');
    const audioFileInput = document.getElementById('audioFile');

    videoFilesInput.addEventListener('change', function(e) {
        handleVideoFiles(e.target.files);
    });

    audioFileInput.addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
            handleAudioFile(e.target.files[0]);
        }
    });
}



// Handle video files
function handleVideoFiles(files) {
    console.log('handleVideoFiles called with', files.length, 'files');
    const fileList = document.getElementById('videoFileList');
    fileList.innerHTML = '';
    selectedVideoFiles = [];

    Array.from(files).forEach(file => {
        console.log('Processing file:', file.name, 'Valid:', isValidVideoFile(file));
        if (isValidVideoFile(file)) {
            selectedVideoFiles.push(file);
            const fileItem = document.createElement('div');
            fileItem.className = 'file-item';
            fileItem.innerHTML = `
                <span><i class="fas fa-video me-2"></i>${file.name}</span>
                <span class="text-muted">${formatFileSize(file.size)}</span>
            `;
            fileList.appendChild(fileItem);
        }
    });
    console.log('Selected video files:', selectedVideoFiles.length);
}

// Handle audio file
function handleAudioFile(file) {
    if (isValidAudioFile(file)) {
        selectedAudioFile = file;
        const fileInfo = document.getElementById('audioFileInfo');
        fileInfo.innerHTML = `
            <div class="file-item">
                <span><i class="fas fa-music me-2"></i>${file.name}</span>
                <span class="text-muted">${formatFileSize(file.size)}</span>
            </div>
        `;
    }
}

// Validate video file
function isValidVideoFile(file) {
    const allowedExtensions = ['mp4', 'avi', 'mov', 'mkv', 'wmv', 'flv', 'webm', 'm4v'];
    const extension = file.name.split('.').pop().toLowerCase();
    return allowedExtensions.includes(extension);
}

// Validate audio file
function isValidAudioFile(file) {
    const allowedExtensions = ['mov', 'mp3', 'wav', 'aac', 'm4a', 'flac', 'ogg', 'wma'];
    const extension = file.name.split('.').pop().toLowerCase();
    return allowedExtensions.includes(extension);
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Merge videos function
function mergeVideos() {
    const method = document.getElementById('mergeMethod').value;
    const outputName = document.getElementById('outputName').value;

    if (selectedVideoFiles.length < 2) {
        showError('Please select at least 2 video files.');
        return;
    }

    const formData = new FormData();
    selectedVideoFiles.forEach(file => {
        formData.append('files', file);
    });
    formData.append('method', method);
    formData.append('output_name', outputName);

    showProgress('Merging videos...');
    hideResults();
    hideError();

    fetch('/merge-videos', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        hideProgress();
        if (data.success) {
            currentDownloadUrl = data.download_url;
            currentFilename = data.filename;
            showSuccess(data.message, `File: ${data.filename}`);
        } else {
            showError(data.error);
        }
    })
    .catch(error => {
        hideProgress();
        showError('An error occurred while processing your request.');
        console.error('Error:', error);
    });
}

// Convert audio function
function convertAudio() {
    const resolutionWidth = document.getElementById('resolutionWidth').value;
    const resolutionHeight = document.getElementById('resolutionHeight').value;
    const fps = document.getElementById('fps').value;
    const colorR = document.getElementById('colorR').value;
    const colorG = document.getElementById('colorG').value;
    const colorB = document.getElementById('colorB').value;
    const outputName = document.getElementById('audioOutputName').value;

    if (!selectedAudioFile) {
        showError('Please select an audio file.');
        return;
    }

    const formData = new FormData();
    formData.append('file', selectedAudioFile);
    formData.append('resolution_width', resolutionWidth);
    formData.append('resolution_height', resolutionHeight);
    formData.append('fps', fps);
    formData.append('color_r', colorR);
    formData.append('color_g', colorG);
    formData.append('color_b', colorB);
    formData.append('output_name', outputName);

    showProgress('Converting audio to video...');
    hideResults();
    hideError();

    fetch('/convert-audio', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        hideProgress();
        if (data.success) {
            currentDownloadUrl = data.download_url;
            currentFilename = data.filename;
            showSuccess(data.message, `File: ${data.filename}`);
        } else {
            showError(data.error);
        }
    })
    .catch(error => {
        hideProgress();
        showError('An error occurred while processing your request.');
        console.error('Error:', error);
    });
}

// Download file function
function downloadFile() {
    if (currentDownloadUrl) {
        const link = document.createElement('a');
        link.href = currentDownloadUrl;
        link.download = currentFilename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}

// Show progress
function showProgress(message) {
    document.getElementById('progressSection').style.display = 'block';
    document.getElementById('progressText').textContent = message;
}

// Hide progress
function hideProgress() {
    document.getElementById('progressSection').style.display = 'none';
}

// Show success
function showSuccess(message, details) {
    document.getElementById('successMessage').textContent = message;
    document.getElementById('resultDetails').textContent = details;
    document.getElementById('resultsSection').style.display = 'block';
}

// Hide results
function hideResults() {
    document.getElementById('resultsSection').style.display = 'none';
}

// Show error
function showError(message) {
    document.getElementById('errorMessage').textContent = message;
    document.getElementById('errorSection').style.display = 'block';
}

// Hide error
function hideError() {
    document.getElementById('errorSection').style.display = 'none';
} 