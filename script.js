document.addEventListener('DOMContentLoaded', function() {
    // Initialize PDF.js worker
    pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';

    const accordions = document.querySelectorAll('.accordion');

    accordions.forEach(accordion => {
        const header = accordion.querySelector('.accordion-header');
        header.addEventListener('click', () => {
            accordion.classList.toggle('active');
            const content = accordion.querySelector('.accordion-content');
            if (accordion.classList.contains('active')) {
                content.style.maxHeight = content.scrollHeight + 'px';
            } else {
                content.style.maxHeight = null;
            }
        });
    });

    const fileUpload = document.querySelector('.file-upload');
    const fileUploadInput = document.querySelector('.file-upload-input');
    const fileUploadText = document.querySelector('.file-upload-text');
    const fileUploadIcon = document.querySelector('.file-upload-icon');
    const fileUploadPreview = document.querySelector('.file-upload-preview');
    const previewTitle = document.querySelector('.preview-title');
    const previewContent = document.querySelector('.preview-content');
    const previewExpand = document.querySelector('.preview-expand');

    async function extractTextFromPdf(file) {
        try {
            const arrayBuffer = await file.arrayBuffer();
            const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
            let fullText = '';

            // Get total pages
            const numPages = pdf.numPages;
            
            // Extract text from each page
            for (let i = 1; i <= numPages; i++) {
                const page = await pdf.getPage(i);
                const textContent = await page.getTextContent();
                const pageText = textContent.items
                    .map(item => item.str)
                    .join(' ');
                fullText += pageText + '\n\n';
            }

            return fullText;
        } catch (error) {
            console.error('Error extracting text:', error);
            throw error;
        }
    }

    fileUploadInput.addEventListener('change', async function(e) {
        const file = e.target.files[0];
        if (file && file.type === 'application/pdf') {
            try {
                // Show loading state in preview
                previewContent.textContent = 'Loading PDF content...';
                fileUploadPreview.style.display = 'block';
                fileUploadText.style.display = 'none';
                fileUploadIcon.style.display = 'none';

                // Extract text
                extractedText = await extractTextFromPdf(file);

                // Show preview with formatted text
                previewContent.textContent = extractedText;

                // Update preview title with filename
                previewTitle.textContent = file.name;

            } catch (error) {
                console.error('Error reading PDF:', error);
                previewContent.textContent = 'Error reading PDF file';
                alert('Error reading PDF file');
            }
        }
    });

    previewExpand.addEventListener('click', function() {
        previewContent.classList.toggle('expanded');
        this.textContent = previewContent.classList.contains('expanded') ? 'Show Less' : 'Show More';
    });

    const generateBtn = document.getElementById('generateBtn');
    const resultsSection = document.getElementById('resultsSection');
    const visaTypeSelect = document.getElementById('visaType');
    const additionalInfo = document.getElementById('additionalInfo');

    // Content elements
    const crsScoreContent = document.getElementById('crsScoreContent');
    const jobRolesContent = document.getElementById('jobRolesContent');
    const nocCodesContent = document.getElementById('nocCodesContent');
    const roadmapContent = document.getElementById('roadmapContent');

    let extractedText = '';

    // Initialize markdown parser with options
    marked.setOptions({
        breaks: true,
        gfm: true
    });

    function renderMarkdown(content) {
        return marked.parse(content);
    }

    function setupMarkdownEditing(contentId) {
        const contentDiv = document.getElementById(contentId);
        const editor = contentDiv.nextElementSibling;
        const editButton = document.createElement('button');
        editButton.className = 'edit-button';
        editButton.textContent = 'Edit';
        
        contentDiv.parentElement.insertBefore(editButton, contentDiv);

        editButton.addEventListener('click', () => {
            if (editor.classList.contains('hidden')) {
                // Switch to edit mode
                editor.value = contentDiv.getAttribute('data-markdown') || contentDiv.textContent;
                editor.classList.remove('hidden');
                contentDiv.classList.add('hidden');
                editButton.textContent = 'Save';
            } else {
                // Save changes and render
                const markdown = editor.value;
                contentDiv.setAttribute('data-markdown', markdown);
                contentDiv.innerHTML = renderMarkdown(markdown);
                editor.classList.add('hidden');
                contentDiv.classList.remove('hidden');
                editButton.textContent = 'Edit';
            }
        });
    }

    // Update the display results code
    function displayResults(data) {
        resultsSection.style.display = 'block';
        
        if (data.crs_score) {
            const content = document.getElementById('crsScoreContent');
            content.setAttribute('data-markdown', data.crs_score);
            content.innerHTML = renderMarkdown(data.crs_score);
        }
        
        if (data.job_roles) {
            const content = document.getElementById('jobRolesContent');
            content.setAttribute('data-markdown', data.job_roles);
            content.innerHTML = renderMarkdown(data.job_roles);
        }
        
        if (data.noc_codes) {
            const content = document.getElementById('nocCodesContent');
            const nocText = Array.isArray(data.noc_codes) 
                ? data.noc_codes.join('\n- ')
                : data.noc_codes;
            content.setAttribute('data-markdown', '- ' + nocText);
            content.innerHTML = renderMarkdown('- ' + nocText);
        }
        
        if (data.roadmap) {
            const content = document.getElementById('roadmapContent');
            content.setAttribute('data-markdown', data.roadmap);
            content.innerHTML = renderMarkdown(data.roadmap);
        }
    }

    // Initialize markdown editing for all content sections
    setupMarkdownEditing('crsScoreContent');
    setupMarkdownEditing('jobRolesContent');
    setupMarkdownEditing('nocCodesContent');
    setupMarkdownEditing('roadmapContent');

    generateBtn.addEventListener('click', async function() {
        if (!extractedText || !visaTypeSelect.value) {
            alert('Please upload a PDF file and select a visa type');
            return;
        }

        const spinnerOverlay = document.getElementById('spinnerOverlay');

        try {
            // Show spinner
            spinnerOverlay.style.display = 'flex';

            // Create URL with query parameters
            const params = new URLSearchParams({
                questionnaire: extractedText,
                roadmap_type: visaTypeSelect.value.toLowerCase()
            });
            
            if (additionalInfo.value) {
                params.append('additional_information', additionalInfo.value);
            }

            const url = `https://latestvisaroadmap-247572588539.us-central1.run.app/generate_roadmap?${params.toString()}`;

            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'accept': 'application/json'
                },
                mode: 'cors'
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            displayResults(data);

        } catch (error) {
            console.error('Error:', error);
            alert('Error generating roadmap. Please try again.');
        } finally {
            // Hide spinner
            spinnerOverlay.style.display = 'none';
        }
    });

    // Handle PDF download
    document.getElementById('downloadBtn').addEventListener('click', async function() {
        // Get the roadmap content
        const roadmapContent = document.getElementById('roadmapContent');
        const markdownContent = roadmapContent.getAttribute('data-markdown') || roadmapContent.textContent;

        try {
            // Convert markdown to HTML
            const htmlContent = marked.parse(markdownContent);
            
            // Create a simple HTML template with basic styling
            const htmlTemplate = `
                <!DOCTYPE html>
                <html>
                <head>
                    <style>
                        body { 
                            font-family: Arial, sans-serif;
                            line-height: 1.6;
                            margin: 2cm;
                        }
                        h1, h2, h3 { margin-top: 1em; }
                        p { margin-bottom: 1em; }
                        ul, ol { margin-left: 2em; }
                    </style>
                </head>
                <body>
                    <h1>Canada Immigration Roadmap</h1>
                    ${htmlContent}
                </body>
                </html>
            `;

            // Create PDF using browser's print to PDF functionality
            const printWindow = window.open('', '_blank');
            printWindow.document.write(htmlTemplate);
            printWindow.document.close();
            
            // Add small delay to ensure content is loaded
            setTimeout(() => {
                printWindow.print();
                printWindow.close();
            }, 250);

        } catch (error) {
            console.error('Error generating PDF:', error);
            alert('Error generating PDF. Please try again.');
        }
    });
});