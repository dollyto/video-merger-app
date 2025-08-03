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
    fileList.innerHTML = `
        <div class="alert alert-info">
            <i class="fas fa-info-circle me-2"></i>
            <strong>Tip:</strong> Drag files to reorder them. Videos will be merged in the order shown below.
        </div>
    `;
    selectedVideoFiles = [];

    Array.from(files).forEach(file => {
        console.log('Processing file:', file.name, 'Valid:', isValidVideoFile(file));
        if (isValidVideoFile(file)) {
            selectedVideoFiles.push(file);
            addFileItem(file, selectedVideoFiles.length - 1);
        }
    });
    console.log('Selected video files:', selectedVideoFiles.length);
    setupFileReordering();
}

// Add file item to the list
function addFileItem(file, index) {
    const fileList = document.getElementById('videoFileList');
    const fileItem = document.createElement('div');
    fileItem.className = 'file-item';
    fileItem.draggable = true;
    fileItem.dataset.index = index;
    fileItem.innerHTML = `
        <div style="display: flex; align-items: center;">
            <div class="file-order">${index + 1}</div>
            <i class="fas fa-grip-vertical drag-handle me-2"></i>
            <span><i class="fas fa-video me-2"></i>${file.name}</span>
        </div>
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <span class="text-muted">${formatFileSize(file.size)}</span>
            <button class="btn btn-sm btn-outline-danger delete-btn" onclick="deleteFile(${index})" title="Remove file">
                <i class="fas fa-trash"></i>
            </button>
        </div>
    `;
    fileList.appendChild(fileItem);
}

// Setup file reordering functionality
function setupFileReordering() {
    const fileItems = document.querySelectorAll('#videoFileList .file-item');
    
    fileItems.forEach(item => {
        item.addEventListener('dragstart', handleDragStart);
        item.addEventListener('dragend', handleDragEnd);
        item.addEventListener('dragover', handleDragOver);
        item.addEventListener('drop', handleDrop);
        item.addEventListener('dragenter', handleDragEnter);
        item.addEventListener('dragleave', handleDragLeave);
    });
}

// Drag and drop event handlers
function handleDragStart(e) {
    e.target.classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/html', e.target.outerHTML);
}

function handleDragEnd(e) {
    e.target.classList.remove('dragging');
}

function handleDragOver(e) {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
}

function handleDragEnter(e) {
    e.preventDefault();
    e.target.closest('.file-item').classList.add('drag-over');
}

function handleDragLeave(e) {
    e.target.closest('.file-item').classList.remove('drag-over');
}

function handleDrop(e) {
    e.preventDefault();
    const draggedItem = document.querySelector('.dragging');
    const dropTarget = e.target.closest('.file-item');
    
    if (draggedItem && dropTarget && draggedItem !== dropTarget) {
        const draggedIndex = parseInt(draggedItem.dataset.index);
        const dropIndex = parseInt(dropTarget.dataset.index);
        
        // Reorder the selectedVideoFiles array
        const [movedFile] = selectedVideoFiles.splice(draggedIndex, 1);
        selectedVideoFiles.splice(dropIndex, 0, movedFile);
        
        // Reorder the DOM elements
        if (draggedIndex < dropIndex) {
            dropTarget.parentNode.insertBefore(draggedItem, dropTarget.nextSibling);
        } else {
            dropTarget.parentNode.insertBefore(draggedItem, dropTarget);
        }
        
        // Update order numbers
        updateFileOrderNumbers();
    }
    
    // Remove drag-over class
    document.querySelectorAll('.file-item').forEach(item => {
        item.classList.remove('drag-over');
    });
}

// Delete a file from the list
function deleteFile(index) {
    const fileName = selectedVideoFiles[index].name;
    
    // Show confirmation dialog
    if (confirm(`Are you sure you want to remove "${fileName}" from the merge list?`)) {
        // Remove file from array
        selectedVideoFiles.splice(index, 1);
        
        // Remove file item from DOM
        const fileItems = document.querySelectorAll('#videoFileList .file-item');
        if (fileItems[index]) {
            fileItems[index].remove();
        }
        
        // Update order numbers for remaining files
        updateFileOrderNumbers();
        
        // Re-setup drag and drop for remaining items
        setupFileReordering();
        
        console.log('File deleted at index', index, 'Remaining files:', selectedVideoFiles.length);
        
        // Show feedback if no files remain
        if (selectedVideoFiles.length === 0) {
            const fileList = document.getElementById('videoFileList');
            fileList.innerHTML = `
                <div class="alert alert-info">
                    <i class="fas fa-info-circle me-2"></i>
                    <strong>Tip:</strong> Drag files to reorder them. Videos will be merged in the order shown below.
                </div>
            `;
        }
    }
}

// Update the order numbers displayed on file items
function updateFileOrderNumbers() {
    const fileItems = document.querySelectorAll('#videoFileList .file-item');
    fileItems.forEach((item, index) => {
        item.dataset.index = index;
        const orderNumber = item.querySelector('.file-order');
        if (orderNumber) {
            orderNumber.textContent = index + 1;
        }
        
        // Update delete button onclick with new index
        const deleteBtn = item.querySelector('.delete-btn');
        if (deleteBtn) {
            deleteBtn.onclick = () => deleteFile(index);
        }
    });
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