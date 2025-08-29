class ScreenRecorder {
    constructor() {
        this.mediaRecorder = null;
        this.recordedChunks = [];
        this.isRecording = false;
        this.stream = null;
        this.recordingStartTime = null;
        this.recordingDuration = 0;
    }

    async startRecording() {
        try {
            // Request screen capture permission
            this.stream = await navigator.mediaDevices.getDisplayMedia({
                video: {
                    mediaSource: 'screen',
                    width: { ideal: 1920 },
                    height: { ideal: 1080 }
                },
                audio: true
            });

            // Create MediaRecorder
            this.mediaRecorder = new MediaRecorder(this.stream, {
                mimeType: 'video/webm;codecs=vp9'
            });

            // Set up event handlers
            this.mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    this.recordedChunks.push(event.data);
                }
            };

            this.mediaRecorder.onstop = () => {
                this.createRecordingBlob();
            };

            // Start recording
            this.mediaRecorder.start(1000); // Collect data every second
            this.isRecording = true;
            this.recordingStartTime = Date.now();
            
            // Update UI
            this.updateRecordingUI(true);
            
            return true;
        } catch (error) {
            console.error('Error starting recording:', error);
            return false;
        }
    }

    stopRecording() {
        if (this.mediaRecorder && this.isRecording) {
            this.mediaRecorder.stop();
            this.isRecording = false;
            this.recordingDuration = Date.now() - this.recordingStartTime;
            
            // Stop all tracks
            if (this.stream) {
                this.stream.getTracks().forEach(track => track.stop());
            }
            
            this.updateRecordingUI(false);
        }
    }

    createRecordingBlob() {
        const blob = new Blob(this.recordedChunks, { type: 'video/webm' });
        const url = URL.createObjectURL(blob);
        
        // Create download link
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = `screen-recording-${Date.now()}.webm`;
        document.body.appendChild(a);
        a.click();
        
        // Clean up
        setTimeout(() => {
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
        }, 100);
        
        // Store recording data for tour
        this.saveRecordingData(blob);
    }

    async saveRecordingData(blob) {
        // Convert blob to base64 for storage
        const reader = new FileReader();
        reader.onloadend = () => {
            const base64data = reader.result;
            
            // Store in localStorage for now (in production, send to server)
            const recordingData = {
                id: Date.now(),
                timestamp: new Date().toISOString(),
                duration: this.recordingDuration,
                data: base64data,
                size: blob.size
            };
            
            localStorage.setItem('screenRecording', JSON.stringify(recordingData));
            
            // Trigger event for tour integration
            const event = new CustomEvent('recordingSaved', { detail: recordingData });
            document.dispatchEvent(event);
        };
        reader.readAsDataURL(blob);
    }

    updateRecordingUI(isRecording) {
        const recordBtn = document.getElementById('recordBtn');
        const stopBtn = document.getElementById('stopBtn');
        const recordingIndicator = document.getElementById('recordingIndicator');
        
        if (recordBtn) recordBtn.style.display = isRecording ? 'none' : 'inline-block';
        if (stopBtn) stopBtn.style.display = isRecording ? 'inline-block' : 'none';
        if (recordingIndicator) recordingIndicator.style.display = isRecording ? 'block' : 'none';
        
        // Update recording time display
        if (isRecording) {
            this.startTimeDisplay();
        }
    }

    startTimeDisplay() {
        if (!this.isRecording) return;
        
        const timeDisplay = document.getElementById('recordingTime');
        if (!timeDisplay) return;
        
        const updateTime = () => {
            if (this.isRecording && this.recordingStartTime) {
                const elapsed = Date.now() - this.recordingStartTime;
                const seconds = Math.floor(elapsed / 1000);
                const minutes = Math.floor(seconds / 60);
                const hours = Math.floor(minutes / 60);
                
                timeDisplay.textContent = `${hours.toString().padStart(2, '0')}:${(minutes % 60).toString().padStart(2, '0')}:${(seconds % 60).toString().padStart(2, '0')}`;
            }
        };
        
        this.timeInterval = setInterval(updateTime, 1000);
    }

    getRecordingStats() {
        return {
            isRecording: this.isRecording,
            duration: this.recordingDuration,
            startTime: this.recordingStartTime
        };
    }
}

// Initialize screen recorder
window.screenRecorder = new ScreenRecorder();

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ScreenRecorder;
}
