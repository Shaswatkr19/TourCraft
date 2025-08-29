class TourEditor {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.steps = [];
        this.currentStep = 0;
        this.isEditing = false;
        this.draggedElement = null;
        this.highlightMode = false;
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.createEditorInterface();
        this.loadExistingSteps();
    }

    setupEventListeners() {
        // Global event listeners
        document.addEventListener('recordingSaved', (e) => this.handleRecordingSaved(e.detail));
        
        // Drag and drop events
        document.addEventListener('dragover', (e) => e.preventDefault());
        document.addEventListener('drop', (e) => this.handleDrop(e));
    }

    createEditorInterface() {
        this.container.innerHTML = `
            <div class="tour-editor">
                <div class="editor-header">
                    <h2>Tour Editor</h2>
                    <div class="editor-controls">
                        <button id="addStepBtn" class="btn btn-primary">Add Step</button>
                        <button id="previewBtn" class="btn btn-info">Preview</button>
                        <button id="saveBtn" class="btn btn-success">Save Tour</button>
                    </div>
                </div>
                
                <div class="editor-main">
                    <div class="steps-panel">
                        <h3>Tour Steps</h3>
                        <div id="stepsList" class="steps-list"></div>
                        <div class="step-actions">
                            <button id="addStepBtn2" class="btn btn-outline-primary btn-sm">+ Add Step</button>
                        </div>
                    </div>
                    
                    <div class="step-editor">
                        <div id="stepEditor" class="step-editor-content">
                            <div class="no-step-selected">
                                <p>Select a step to edit or create a new one</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="recording-panel">
                    <h3>Screen Recording</h3>
                    <div class="recording-controls">
                        <button id="recordBtn" class="btn btn-danger">Start Recording</button>
                        <button id="stopBtn" class="btn btn-secondary" style="display: none;">Stop Recording</button>
                        <div id="recordingIndicator" class="recording-indicator" style="display: none;">
                            <span class="recording-dot"></span>
                            <span id="recordingTime">00:00:00</span>
                        </div>
                    </div>
                </div>
            </div>
        `;

        this.bindEditorEvents();
    }

    bindEditorEvents() {
        // Add step button
        document.getElementById('addStepBtn').addEventListener('click', () => this.addNewStep());
        document.getElementById('addStepBtn2').addEventListener('click', () => this.addNewStep());
        
        // Preview and save buttons
        document.getElementById('previewBtn').addEventListener('click', () => this.previewTour());
        document.getElementById('saveBtn').addEventListener('click', () => this.saveTour());
        
        // Recording controls
        document.getElementById('recordBtn').addEventListener('click', () => this.startRecording());
        document.getElementById('stopBtn').addEventListener('click', () => this.stopRecording());
    }

    addNewStep() {
        const stepNumber = this.steps.length + 1;
        const newStep = {
            id: Date.now(),
            stepNumber: stepNumber,
            title: `Step ${stepNumber}`,
            description: '',
            screenshot: null,
            highlightArea: null,
            recording: null
        };

        this.steps.push(newStep);
        this.renderStepsList();
        this.selectStep(newStep.id);
        this.updateStepNumbers();
    }

    renderStepsList() {
        const stepsList = document.getElementById('stepsList');
        stepsList.innerHTML = '';

        this.steps.forEach((step, index) => {
            const stepElement = document.createElement('div');
            stepElement.className = 'step-item';
            stepElement.draggable = true;
            stepElement.dataset.stepId = step.id;
            
            stepElement.innerHTML = `
                <div class="step-header">
                    <span class="step-number">${step.stepNumber}</span>
                    <span class="step-title">${step.title}</span>
                </div>
                <div class="step-actions">
                    <button class="btn btn-sm btn-outline-primary edit-step" data-step-id="${step.id}">Edit</button>
                    <button class="btn btn-sm btn-outline-danger delete-step" data-step-id="${step.id}">Delete</button>
                </div>
            `;

            // Add event listeners
            stepElement.querySelector('.edit-step').addEventListener('click', () => this.selectStep(step.id));
            stepElement.querySelector('.delete-step').addEventListener('click', () => this.deleteStep(step.id));
            
            // Drag and drop events
            stepElement.addEventListener('dragstart', (e) => this.handleDragStart(e, step.id));
            stepElement.addEventListener('dragover', (e) => this.handleDragOver(e));
            stepElement.addEventListener('drop', (e) => this.handleStepDrop(e, step.id));
            
            stepsList.appendChild(stepElement);
        });
    }

    selectStep(stepId) {
        const step = this.steps.find(s => s.id === stepId);
        if (!step) return;

        this.currentStep = stepId;
        this.renderStepEditor(step);
        this.updateStepSelection();
    }

    renderStepEditor(step) {
        const stepEditor = document.getElementById('stepEditor');
        
        stepEditor.innerHTML = `
            <div class="step-editor-form">
                <h4>Editing Step ${step.stepNumber}</h4>
                
                <div class="form-group">
                    <label>Step Title</label>
                    <input type="text" class="form-control" value="${step.title}" 
                           onchange="tourEditor.updateStepField(${step.id}, 'title', this.value)">
                </div>
                
                <div class="form-group">
                    <label>Description</label>
                    <textarea class="form-control" rows="3" 
                              onchange="tourEditor.updateStepField(${step.id}, 'description', this.value)">${step.description}</textarea>
                </div>
                
                <div class="form-group">
                    <label>Screenshot</label>
                    <div class="screenshot-upload">
                        ${step.screenshot ? 
                            `<img src="${step.screenshot}" class="screenshot-preview" alt="Screenshot">` :
                            `<div class="upload-placeholder">No screenshot uploaded</div>`
                        }
                        <input type="file" accept="image/*" class="form-control" 
                               onchange="tourEditor.uploadScreenshot(${step.id}, this)">
                    </div>
                </div>
                
                <div class="form-group">
                    <label>Highlight Area</label>
                    <div class="highlight-controls">
                        <button type="button" class="btn btn-outline-warning" 
                                onclick="tourEditor.toggleHighlightMode(${step.id})">
                            ${step.highlightArea ? 'Edit Highlight' : 'Add Highlight'}
                        </button>
                        ${step.highlightArea ? 
                            `<button type="button" class="btn btn-outline-danger" 
                                     onclick="tourEditor.removeHighlight(${step.id})">Remove</button>` : ''
                        }
                    </div>
                    ${step.highlightArea ? 
                        `<div class="highlight-preview">Highlight area: ${JSON.stringify(step.highlightArea)}</div>` : ''
                    }
                </div>
                
                <div class="form-group">
                    <label>Screen Recording</label>
                    <div class="recording-info">
                        ${step.recording ? 
                            `<div class="recording-preview">
                                <span>Recording: ${step.recording.duration}ms</span>
                                <button type="button" class="btn btn-sm btn-outline-danger" 
                                        onclick="tourEditor.removeRecording(${step.id})">Remove</button>
                             </div>` :
                            `<div class="no-recording">No recording attached</div>`
                        }
                    </div>
                </div>
            </div>
        `;
    }

    updateStepField(stepId, field, value) {
        const step = this.steps.find(s => s.id === stepId);
        if (step) {
            step[field] = value;
        }
    }

    uploadScreenshot(stepId, input) {
        const file = input.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (e) => {
            this.updateStepField(stepId, 'screenshot', e.target.result);
            this.renderStepEditor(this.steps.find(s => s.id === stepId));
        };
        reader.readAsDataURL(file);
    }

    toggleHighlightMode(stepId) {
        this.highlightMode = !this.highlightMode;
        
        if (this.highlightMode) {
            this.enableHighlightMode(stepId);
        } else {
            this.disableHighlightMode();
        }
    }

    enableHighlightMode(stepId) {
        // Create overlay for highlight selection
        const overlay = document.createElement('div');
        overlay.id = 'highlightOverlay';
        overlay.className = 'highlight-overlay';
        overlay.innerHTML = `
            <div class="highlight-instructions">
                <p>Click and drag to create a highlight area</p>
                <button class="btn btn-primary" onclick="tourEditor.finishHighlight(${stepId})">Done</button>
            </div>
        `;
        
        document.body.appendChild(overlay);
        
        // Add highlight selection logic
        this.setupHighlightSelection(overlay, stepId);
    }

    disableHighlightMode() {
        const overlay = document.getElementById('highlightOverlay');
        if (overlay) {
            overlay.remove();
        }
        this.highlightMode = false;
    }

    setupHighlightSelection(overlay, stepId) {
        let isDrawing = false;
        let startX, startY;
        let highlightBox;

        overlay.addEventListener('mousedown', (e) => {
            isDrawing = true;
            startX = e.clientX;
            startY = e.clientY;
            
            highlightBox = document.createElement('div');
            highlightBox.className = 'highlight-box';
            highlightBox.style.left = startX + 'px';
            highlightBox.style.top = startY + 'px';
            overlay.appendChild(highlightBox);
        });

        overlay.addEventListener('mousemove', (e) => {
            if (!isDrawing || !highlightBox) return;
            
            const width = e.clientX - startX;
            const height = e.clientY - startY;
            
            highlightBox.style.width = Math.abs(width) + 'px';
            highlightBox.style.height = Math.abs(height) + 'px';
            highlightBox.style.left = (width < 0 ? e.clientX : startX) + 'px';
            highlightBox.style.top = (height < 0 ? e.clientY : startY) + 'px';
        });

        overlay.addEventListener('mouseup', () => {
            if (isDrawing && highlightBox) {
                const rect = highlightBox.getBoundingClientRect();
                const highlightData = {
                    x: rect.left,
                    y: rect.top,
                    width: rect.width,
                    height: rect.height
                };
                
                this.updateStepField(stepId, 'highlightArea', highlightData);
                this.disableHighlightMode();
                this.renderStepEditor(this.steps.find(s => s.id === stepId));
            }
            isDrawing = false;
        });
    }

    removeHighlight(stepId) {
        this.updateStepField(stepId, 'highlightArea', null);
        this.renderStepEditor(this.steps.find(s => s.id === stepId));
    }

    removeRecording(stepId) {
        this.updateStepField(stepId, 'recording', null);
        this.renderStepEditor(this.steps.find(s => s.id === stepId));
    }

    handleRecordingSaved(recordingData) {
        if (this.currentStep) {
            this.updateStepField(this.currentStep, 'recording', recordingData);
            this.renderStepEditor(this.steps.find(s => s.id === this.currentStep));
        }
    }

    startRecording() {
        if (window.screenRecorder) {
            window.screenRecorder.startRecording();
        }
    }

    stopRecording() {
        if (window.screenRecorder) {
            window.screenRecorder.stopRecording();
        }
    }

    // Drag and drop methods
    handleDragStart(e, stepId) {
        this.draggedElement = stepId;
        e.dataTransfer.effectAllowed = 'move';
    }

    handleDragOver(e) {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
    }

    handleStepDrop(e, targetStepId) {
        e.preventDefault();
        
        if (this.draggedElement && this.draggedElement !== targetStepId) {
            this.reorderSteps(this.draggedElement, targetStepId);
        }
        
        this.draggedElement = null;
    }

    reorderSteps(draggedId, targetId) {
        const draggedIndex = this.steps.findIndex(s => s.id === draggedId);
        const targetIndex = this.steps.findIndex(s => s.id === targetId);
        
        if (draggedIndex === -1 || targetIndex === -1) return;
        
        // Remove dragged element
        const [draggedStep] = this.steps.splice(draggedIndex, 1);
        
        // Insert at target position
        this.steps.splice(targetIndex, 0, draggedStep);
        
        // Update step numbers
        this.updateStepNumbers();
        this.renderStepsList();
    }

    updateStepNumbers() {
        this.steps.forEach((step, index) => {
            step.stepNumber = index + 1;
        });
    }

    updateStepSelection() {
        // Update visual selection in steps list
        document.querySelectorAll('.step-item').forEach(item => {
            item.classList.remove('selected');
            if (item.dataset.stepId == this.currentStep) {
                item.classList.add('selected');
            }
        });
    }

    deleteStep(stepId) {
        if (confirm('Are you sure you want to delete this step?')) {
            this.steps = this.steps.filter(s => s.id !== stepId);
            this.updateStepNumbers();
            this.renderStepsList();
            
            if (this.currentStep === stepId) {
                this.currentStep = this.steps.length > 0 ? this.steps[0].id : null;
                if (this.currentStep) {
                    this.selectStep(this.currentStep);
                } else {
                    this.showNoStepSelected();
                }
            }
        }
    }

    showNoStepSelected() {
        const stepEditor = document.getElementById('stepEditor');
        stepEditor.innerHTML = `
            <div class="no-step-selected">
                <p>Select a step to edit or create a new one</p>
            </div>
        `;
    }

    loadExistingSteps() {
        // Load steps from existing tour data if available
        const tourData = this.getTourData();
        if (tourData && tourData.steps) {
            this.steps = tourData.steps;
            this.renderStepsList();
        }
    }

    getTourData() {
        // Get tour data from the page or localStorage
        const tourId = this.container.dataset.tourId;
        if (tourId) {
            // In a real app, fetch from server
            return JSON.parse(localStorage.getItem(`tour_${tourId}`) || '{}');
        }
        return {};
    }

    previewTour() {
        // Create preview modal
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.innerHTML = `
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Tour Preview</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div id="tourPreview" class="tour-preview"></div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Initialize Bootstrap modal
        const bootstrapModal = new bootstrap.Modal(modal);
        bootstrapModal.show();
        
        // Render preview
        this.renderTourPreview();
        
        // Clean up
        modal.addEventListener('hidden.bs.modal', () => {
            document.body.removeChild(modal);
        });
    }

    renderTourPreview() {
        const preview = document.getElementById('tourPreview');
        if (!preview) return;
        
        let previewHTML = '<div class="tour-preview-content">';
        
        this.steps.forEach((step, index) => {
            previewHTML += `
                <div class="preview-step" data-step="${index}">
                    <h4>Step ${step.stepNumber}: ${step.title}</h4>
                    ${step.description ? `<p>${step.description}</p>` : ''}
                    ${step.screenshot ? `<img src="${step.screenshot}" class="preview-screenshot" alt="Step ${step.stepNumber}">` : ''}
                    ${step.highlightArea ? `<div class="preview-highlight">Highlight area included</div>` : ''}
                    ${step.recording ? `<div class="preview-recording">Recording: ${step.recording.duration}ms</div>` : ''}
                </div>
            `;
        });
        
        previewHTML += '</div>';
        preview.innerHTML = previewHTML;
        
        // Add navigation
        this.addPreviewNavigation(preview);
    }

    addPreviewNavigation(preview) {
        const nav = document.createElement('div');
        nav.className = 'preview-navigation';
        nav.innerHTML = `
            <button class="btn btn-primary" onclick="tourEditor.navigatePreview('prev')">Previous</button>
            <span class="preview-counter">1 of ${this.steps.length}</span>
            <button class="btn btn-primary" onclick="tourEditor.navigatePreview('next')">Next</button>
        `;
        preview.appendChild(nav);
    }

    navigatePreview(direction) {
        const currentStep = parseInt(document.querySelector('.preview-step.active')?.dataset.step) || 0;
        let newStep = currentStep;
        
        if (direction === 'next' && currentStep < this.steps.length - 1) {
            newStep = currentStep + 1;
        } else if (direction === 'prev' && currentStep > 0) {
            newStep = currentStep - 1;
        }
        
        // Update active step
        document.querySelectorAll('.preview-step').forEach((step, index) => {
            step.classList.toggle('active', index === newStep);
        });
        
        // Update counter
        const counter = document.querySelector('.preview-counter');
        if (counter) {
            counter.textContent = `${newStep + 1} of ${this.steps.length}`;
        }
    }

    saveTour() {
        // Save tour data
        const tourData = {
            steps: this.steps,
            lastModified: new Date().toISOString()
        };
        
        // In a real app, send to server
        localStorage.setItem('tour_draft', JSON.stringify(tourData));
        
        // Show success message
        this.showSaveSuccess();
    }

    showSaveSuccess() {
        const alert = document.createElement('div');
        alert.className = 'alert alert-success alert-dismissible fade show';
        alert.innerHTML = `
            Tour saved successfully!
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        this.container.insertBefore(alert, this.container.firstChild);
        
        // Auto-dismiss after 3 seconds
        setTimeout(() => {
            alert.remove();
        }, 3000);
    }
}

// Initialize tour editor when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const editorContainer = document.getElementById('tourEditorContainer');
    if (editorContainer) {
        window.tourEditor = new TourEditor('tourEditorContainer');
    }
});
