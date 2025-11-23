import os
import markdown
from flask import Flask, render_template_string, request, jsonify
from openai import OpenAI
import re

app = Flask(__name__)

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ.get("HUGGINGFACE_API_KEY")
)

html_template = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Blog Generator</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
        :root {
            --primary-gradient: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
            --bg-gradient: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            --glass-bg: rgba(255, 255, 255, 0.95);
            --glass-border: 1px solid rgba(255, 255, 255, 0.2);
            --text-primary: #1f2937;
            --text-secondary: #4b5563;
            --error-color: #ef4444;
            --success-color: #10b981;
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        }

        body {
            font-family: 'Inter', sans-serif;
            background: var(--bg-gradient);
            min-height: 100vh;
            margin: 0;
            padding: 0;
            color: var(--text-primary);
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .main-container {
            width: 100%;
            max-width: 900px;
            padding: 2rem;
            box-sizing: border-box;
        }

        /* Hero Section */
        header {
            text-align: center;
            margin-bottom: 3rem;
            animation: fadeIn 0.8s ease-out;
        }

        header h1 {
            font-size: 3rem;
            font-weight: 800;
            background: var(--primary-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
            letter-spacing: -0.02em;
        }

        header p {
            font-size: 1.25rem;
            color: var(--text-secondary);
            max-width: 600px;
            margin: 0 auto;
            line-height: 1.6;
        }

        /* Card Styles */
        .card {
            background: var(--glass-bg);
            backdrop-filter: blur(10px);
            border-radius: 1.5rem;
            border: var(--glass-border);
            box-shadow: var(--shadow-lg);
            padding: 2.5rem;
            margin-bottom: 2rem;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .card:hover {
            transform: translateY(-2px);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        }

        /* Form Elements */
        .input-group {
            position: relative;
            margin-bottom: 1.5rem;
        }

        textarea {
            width: 100%;
            height: 180px;
            padding: 1.25rem;
            font-family: inherit;
            font-size: 1.1rem;
            border: 2px solid #e5e7eb;
            border-radius: 1rem;
            background: #fff;
            resize: none;
            transition: all 0.3s ease;
            box-sizing: border-box;
        }

        textarea:focus {
            outline: none;
            border-color: #8b5cf6;
            box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.1);
        }

        .error-msg {
            color: var(--error-color);
            font-size: 0.9rem;
            margin-top: 0.5rem;
            display: none;
            align-items: center;
            gap: 0.5rem;
        }

        .char-counter {
            font-size: 0.875rem;
            color: var(--text-secondary);
            text-align: right;
            margin-top: 0.5rem;
            transition: color 0.3s;
        }

        .char-counter.warning {
            color: #f59e0b;
        }

        .char-counter.error {
            color: var(--error-color);
        }

        .char-counter.success {
            color: var(--success-color);
        }

        .btn-primary {
            width: 100%;
            padding: 1rem;
            font-size: 1.1rem;
            font-weight: 600;
            color: white;
            background: var(--primary-gradient);
            border: none;
            border-radius: 1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 0.75rem;
        }

        .btn-primary:hover:not(:disabled) {
            opacity: 0.95;
            transform: translateY(-1px);
        }

        .btn-primary:disabled {
            opacity: 0.7;
            cursor: not-allowed;
        }

        /* Loading Spinner */
        .spinner {
            width: 24px;
            height: 24px;
            border: 3px solid rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            border-top-color: white;
            animation: spin 1s linear infinite;
            display: none;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        /* Output Section */
        #output-card {
            display: none;
            animation: slideUp 0.5s ease-out;
        }

        .output-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid #e5e7eb;
        }

        .status-chip {
            padding: 0.5rem 1rem;
            border-radius: 2rem;
            font-size: 0.875rem;
            font-weight: 500;
            background: #e0e7ff;
            color: #4338ca;
            transition: all 0.3s ease;
        }

        .meta-info {
            display: flex;
            gap: 1.5rem;
            align-items: center;
            color: var(--text-secondary);
            font-size: 0.9rem;
        }

        .copy-btn {
            background: none;
            border: 1px solid #e5e7eb;
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            color: var(--text-secondary);
            cursor: pointer;
            font-size: 0.9rem;
            transition: all 0.2s;
        }

        .copy-btn:hover {
            background: #f3f4f6;
            color: var(--text-primary);
        }

        .blog-content {
            line-height: 1.8;
            font-size: 1.1rem;
            color: #374151;
        }
        
        .blog-content h1 {
            color: #111827;
            font-size: 2rem;
            font-weight: 700;
            margin-top: 2.5rem;
            margin-bottom: 1rem;
            line-height: 1.3;
        }

        .blog-content h2 {
            color: #111827;
            font-size: 1.5rem;
            font-weight: 600;
            margin-top: 2rem;
            margin-bottom: 0.75rem;
            line-height: 1.4;
        }

        .blog-content h3 {
            color: #1f2937;
            font-size: 1.25rem;
            font-weight: 600;
            margin-top: 1.5rem;
            margin-bottom: 0.5rem;
        }
        
        .blog-content p {
            margin-bottom: 1.5rem;
            text-align: justify;
        }

        .blog-content ul, .blog-content ol {
            margin-bottom: 1.5rem;
            padding-left: 2rem;
        }

        .blog-content li {
            margin-bottom: 0.5rem;
        }

        .blog-content strong {
            color: #111827;
            font-weight: 600;
        }

        .blog-content em {
            font-style: italic;
        }

        .blog-content code {
            background: #f3f4f6;
            padding: 0.2rem 0.4rem;
            border-radius: 0.25rem;
            font-size: 0.9em;
            font-family: 'Courier New', monospace;
        }

        .blog-content pre {
            background: #1f2937;
            color: #f9fafb;
            padding: 1rem;
            border-radius: 0.5rem;
            overflow-x: auto;
            margin-bottom: 1.5rem;
        }

        .blog-content blockquote {
            border-left: 4px solid #8b5cf6;
            padding-left: 1rem;
            margin: 1.5rem 0;
            color: #4b5563;
            font-style: italic;
        }

        /* Toast Notification */
        .toast-container {
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            z-index: 1000;
        }

        .toast {
            background: white;
            padding: 1rem 1.5rem;
            border-radius: 0.75rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            margin-top: 1rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            animation: slideIn 0.3s ease-out;
            border-left: 4px solid var(--primary-gradient);
        }

        .toast.error { border-left-color: var(--error-color); }
        .toast.success { border-left-color: var(--success-color); }

        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        @keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes slideIn { from { opacity: 0; transform: translateX(100%); } to { opacity: 1; transform: translateX(0); } }

        /* Responsive */
        @media (max-width: 640px) {
            header h1 { font-size: 2rem; }
            .card { padding: 1.5rem; }
        }
    </style>
</head>
<body>
    <div class="main-container">
        <header>
            <h1>AI Blog Generator</h1>
            <p>Transform your ideas into fully-fledged, 1000-word blogs with the power of AI. Just enter a topic and let the magic happen.</p>
        </header>

        <div class="card">
            <form id="blog-form">
                <div class="input-group">
                    <textarea id="prompt" placeholder="Enter your blog topic (e.g., 'The Future of Renewable Energy', 'Digital Marketing Trends in 2025')..." spellcheck="false"></textarea>
                    <div class="char-counter" id="char-counter">0 / 600 characters</div>
                    <div id="validation-msg" class="error-msg">⚠ Please enter a prompt between 20 and 600 characters.</div>
                </div>
                <button type="submit" id="generate-btn" class="btn-primary">
                    <div class="spinner"></div>
                    <span class="btn-text">Generate Blog</span>
                </button>
            </form>
        </div>

        <div id="output-card" class="card">
            <div class="output-header">
                <div class="status-chip" id="status-chip">Generated</div>
                <div class="meta-info">
                    <span id="word-count">0 words</span>
                    <button class="copy-btn" onclick="copyToClipboard()">Copy Blog</button>
                </div>
            </div>
            <div id="blog-content" class="blog-content"></div>
        </div>
    </div>

    <div class="toast-container" id="toast-container"></div>

    <script>
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
            if (prompt.length < 20 || prompt.length > 600) {
                validationMsg.style.display = 'flex';
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

        function updateCharCounter() {
            const length = promptInput.value.length;
            charCounter.textContent = `${length} / 600 characters`;
            
            // Update styling based on length
            charCounter.classList.remove('warning', 'error', 'success');
            if (length < 20) {
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
            if (length >= 20 && length <= 600) {
                validationMsg.style.display = 'none';
                promptInput.style.borderColor = '#e5e7eb';
            }
        });

        // Initialize character counter
        updateCharCounter();
    </script>
</body>
</html>
"""

def is_incomplete(text: str) -> bool:
    text = text.strip()

    if not text.endswith(('.', '!', '?')):
        return True

    last_line = text.split("\n")[-1].lower()
    if last_line.startswith(("##", "###", "1.", "2.", "3.", "4.", "5.", "-", "|")):
        return True

    if text.count("|") % 2 != 0:  # odd number of pipes → broken table
        return True

    if len(text.split()) > 900:  # approaching 1000
        return True

    return False

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Handle JSON request
        if request.is_json:
            data = request.get_json()
            prompt = data.get("prompt", "")
        else:
            # Fallback for standard form submit if needed (though UI uses JSON)
            prompt = request.form.get("prompt", "")

        if not prompt or len(prompt) < 20:
            return jsonify({"error": "Prompt must be at least 20 characters."}), 400

        try:
            completion = client.chat.completions.create(
                model="openai/gpt-oss-120b:together",
                messages=[{"role": "user", "content": f"Write a detailed, engaging blog of ~1000 words on: {prompt}"}],
                max_tokens=1500
            )
            blog = completion.choices[0].message.content
            blog = re.sub(r"By .?\n+Published: .?\n+", "", blog)

            if is_incomplete(blog):
                continuation = client.chat.completions.create(
                    model="openai/gpt-oss-120b:together",
                    messages=[
                        {"role": "system", "content": "You are a blog continuation assistant."},
                        {"role": "user", "content": f"Continue this blog without repeating, and finish it properly:\n\n{blog}"}
                    ],
                    max_tokens=500
                )
                blog += "\n" + continuation.choices[0].message.content

            # Return raw markdown for client-side rendering
            return jsonify({"blog": blog})

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return render_template_string(html_template)

if __name__ == "__main__":
    app.run(debug=True)