# Quick Start Guide

## 🚀 Get Started in 4 Minutes

### Step 1: Install Dependencies (30 seconds)
```bash
pip install Flask openai markdown
```

### Step 2: Set Up Environment (30 seconds)
```bash
# Copy the example environment file
copy .env.example .env

# Edit .env and add your HuggingFace API key
# Get your key from: https://huggingface.co/settings/tokens
```

Or set it directly:
```bash
# Windows (PowerShell)
$env:HUGGINGFACE_API_KEY="your_key_here"

# Windows (CMD)
set HUGGINGFACE_API_KEY=your_key_here

# Linux/Mac
export HUGGINGFACE_API_KEY=your_key_here
```

### Step 3: Run the App (10 seconds)
```bash
python assessment.py
```

### Step 4: Open Browser (5 seconds)
Visit: **http://127.0.0.1:5000**

---

## 📝 How to Use

### 1. Enter Your Topic
Type a blog topic in the textarea (20-600 characters)

**Examples:**
- "The Future of Artificial Intelligence"
- "Benefits of Remote Work in 2025"
- "Beginner's Guide to Python Programming"

### 2. Watch the Counter
The character counter updates in real-time:
- 🟠 Orange: Less than 20 characters (too short)
- 🟢 Green: 20-600 characters (perfect!)
- 🔴 Red: More than 600 characters (too long)

### 3. Generate Blog
Click the **"Generate Blog"** button

The button will show:
- Spinner animation
- "Generating..." text
- Status chip: "Calling LLM..."

### 4. Read Your Blog
After 10-30 seconds:
- ✅ Blog appears with beautiful formatting
- 📊 Word count displayed (~1000 words)
- 📋 Copy button ready to use

### 5. Copy & Use
Click **"Copy Blog"** to copy the entire blog to your clipboard

---

## 🎨 Features at a Glance

| Feature | What It Does |
|---------|-------------|
| **Character Counter** | Shows how many characters you've typed (0-600) |
| **Validation** | Ensures your prompt is the right length |
| **Loading State** | Shows progress while generating |
| **Markdown Rendering** | Beautiful formatting with headings, lists, bold, italic |
| **Word Counter** | Displays exact word count of generated blog |
| **Copy Button** | One-click copy to clipboard |
| **Toast Notifications** | Success and error messages |
| **Auto-Scroll** | Automatically scrolls to your blog |
| **Rate Limiting** | Prevents spam (3-second cooldown) |

---

## 🎯 Tips for Best Results

### Good Prompts
✅ "The Impact of Climate Change on Agriculture"
✅ "How to Start a Successful Podcast in 2025"
✅ "Understanding Blockchain Technology for Beginners"

### Avoid
❌ "AI" (too short)
❌ Very long prompts with multiple questions
❌ Prompts with special formatting requirements

---

## 🐛 Troubleshooting

### Problem: "Please enter a prompt between 20 and 600 characters"
**Solution**: Your prompt is too short or too long. Check the character counter.

### Problem: "Network error. Please check your connection."
**Solution**: Check your internet connection and try again.

### Problem: "Please wait X seconds before generating again."
**Solution**: Wait for the cooldown period (3 seconds) before submitting again.

### Problem: Blog is less than 1000 words
**Solution**: This is normal. The LLM aims for ~1000 words but may vary. Try a more detailed prompt.

### Problem: Page won't load
**Solution**: 
1. Make sure Flask is running: `python assessment.py`
2. Check the terminal for errors
3. Verify dependencies are installed: `pip install -r requirements.txt`

---

## 🌐 Deploy Online (Optional)

Want to share your blog generator with the world?

### Easiest: Render (Free)
1. Push code to GitHub
2. Go to [render.com](https://render.com)
3. Connect repository
4. Deploy (automatic)
5. Share your URL!

**Full deployment guide**: See `DEPLOYMENT.md`

---

## 📚 Learn More

- **Full Documentation**: `README.md`
- **Testing Guide**: `VERIFICATION.md`
- **Deployment Options**: `DEPLOYMENT.md`
- **Implementation Details**: `IMPLEMENTATION_SUMMARY.md`

---

## 🎉 You're Ready!

Start generating amazing blogs with AI. Enjoy! 🚀

---

**Need Help?** Check the documentation files or review the code comments in `assessment.py`.
