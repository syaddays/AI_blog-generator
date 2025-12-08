const form = document.getElementById('blog-form');
const promptInput = document.getElementById('prompt');
const generateBtn = document.getElementById('generate-btn');
const spinner = document.querySelector('.spinner');
const btnText = document.querySelector('.btn-text');
const validationMsg = document.getElementById('validation-msg');
const charCounter = document.getElementById('char-counter');
const outputCard = document.getElementById('output-card');
const blogContent = document.getElementById('blog-content');
const wordCount = document.getElementById('word-count');
const statusChip = document.getElementById('status-chip');

// Rate limiting
let lastRequestTime = 0;
const REQUEST_COOLDOWN = 3000; // 3 seconds between requests

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const prompt = promptInput.value.trim();

    // Validation
    if (prompt.length === 0 || prompt.length > 600) {
        validationMsg.style.display = 'flex';
        validationMsg.textContent = '⚠ Please enter a prompt between 1 and 600 characters.';
        promptInput.style.borderColor = 'var(--error-color)';
        return;
    }

    // Rate limiting
    const now = Date.now();
    if (now - lastRequestTime < REQUEST_COOLDOWN) {
        const waitTime = Math.ceil((REQUEST_COOLDOWN - (now - lastRequestTime)) / 1000);
        showToast(`Please wait ${waitTime} seconds before generating again.`, 'error');
        return;
    }
    lastRequestTime = now;

    resetState();
    setLoading(true);

    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 60000); // 60s timeout

        const response = await fetch('/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt: prompt }),
            signal: controller.signal
        });

        clearTimeout(timeoutId);

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();

        if (data.error) {
            throw new Error(data.error);
        }

        renderBlog(data.blog);
        showToast('Blog generated successfully!', 'success');

        // Auto-scroll with slight delay for animation
        setTimeout(() => {
            outputCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 100);

    } catch (error) {
        if (error.name === 'AbortError') {
            showToast('Request timed out. Please try again.', 'error');
        } else if (error.message.includes('Failed to fetch')) {
            showToast('Network error. Please check your connection.', 'error');
        } else {
            showToast(error.message || 'An error occurred while generating the blog.', 'error');
        }
    } finally {
        setLoading(false);
    }
});

function resetState() {
    validationMsg.style.display = 'none';
    promptInput.style.borderColor = '#e5e7eb';
    outputCard.style.display = 'none';
}

function setLoading(isLoading) {
    generateBtn.disabled = isLoading;
    if (isLoading) {
        spinner.style.display = 'block';
        btnText.textContent = 'Generating...';
        statusChip.textContent = 'Calling LLM...';
        statusChip.style.background = '#fef3c7';
        statusChip.style.color = '#d97706';
    } else {
        spinner.style.display = 'none';
        btnText.textContent = 'Generate Blog';
    }
}

function renderBlog(markdownText) {
    outputCard.style.display = 'block';
    blogContent.innerHTML = marked.parse(markdownText);

    // Word count
    const words = markdownText.trim().split(/\s+/).length;
    wordCount.textContent = `${words} words`;

    statusChip.textContent = 'Generated';
    statusChip.style.background = '#d1fae5';
    statusChip.style.color = '#059669';
}

function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    document.getElementById('toast-container').appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function copyToClipboard() {
    const text = document.getElementById('blog-content').innerText;
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copied to clipboard!');
    }).catch(() => {
        showToast('Failed to copy to clipboard.', 'error');
    });
}

function downloadMarkdown() {
    // Get the raw markdown content. 
    // Since we are rendering markdown to HTML, we might not have the raw markdown stored globally.
    // However, the user wants to download the blog. 
    // The current implementation renders HTML. `innerText` gives text content, but not markdown formatting.
    // To do this correctly, we should probably store the raw markdown when we receive it.

    // Let's grab the innerText for now as a fallback, or better, let's store the raw markdown in a data attribute or variable.
    // I'll modify renderBlog to store it.

    // Actually, let's just use turndown or similar if we wanted to reverse it, but we have the source in the response.
    // I will add a global variable to store the current markdown.
    if (currentMarkdown) {
        const blob = new Blob([currentMarkdown], { type: 'text/markdown' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'blog_post.md';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        showToast('Blog downloaded successfully!', 'success');
    } else {
        showToast('No blog content to download.', 'error');
    }
}

let currentMarkdown = "";

// Override renderBlog to store markdown
const originalRenderBlog = renderBlog;
renderBlog = function (markdownText) {
    currentMarkdown = markdownText;
    originalRenderBlog(markdownText);
}


function updateCharCounter() {
    const length = promptInput.value.length;
    charCounter.textContent = `${length} / 600 characters`;

    // Update styling based on length
    charCounter.classList.remove('warning', 'error', 'success');
    if (length === 0) {
        charCounter.classList.add('warning');
    } else if (length > 600) {
        charCounter.classList.add('error');
    } else {
        charCounter.classList.add('success');
    }
}

promptInput.addEventListener('input', () => {
    updateCharCounter();

    const length = promptInput.value.length;
    if (length > 0 && length <= 600) {
        validationMsg.style.display = 'none';
        promptInput.style.borderColor = '#e5e7eb';
    }
});

// Initialize character counter
updateCharCounter();
