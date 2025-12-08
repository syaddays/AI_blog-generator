# AI Blog Generator - Technical Assessment Documentation

## Overview
This project is a full-stack web application designed to generate high-quality, 1000-word blog posts based on user prompts. It leverages a powerful open-source Large Language Model (LLM) to create structured, engaging content. The application features a modern, responsive user interface with dynamic feedback mechanisms.

## Technical Architecture

### Backend
- **Framework**: Python Flask
  - Chosen for its lightweight nature and ease of integration with Python-based AI libraries.
- **API Integration**: OpenAI Python Client (configured for Hugging Face Inference API)
  - Allows seamless communication with the LLM using a standard, widely-supported interface.
- **Environment Management**: `python-dotenv` for secure API key handling.

### Frontend
- **Technology**: HTML5, CSS3, Vanilla JavaScript (embedded in a single `app.py` for portability).
- **Design System**: Custom CSS with Glassmorphism aesthetics, responsive layout, and dark/light mode support.
- **Markdown Rendering**: `marked.js` for client-side parsing of the generated Markdown content into rich HTML.

## Model Selection

### Model: `openai/gpt-oss-120b:together`
- **Source**: Hugging Face Inference API (`https://router.huggingface.co/v1`)
- **Reasoning**:
  - **Performance**: A 120B parameter model offers superior reasoning and coherence compared to smaller open-source models, essential for generating long-form (1000-word) content without losing context.
  - **Cost**: Accessible via free inference tiers, meeting the assessment requirement for "free ones only".
  - **Compatibility**: Supports the standard OpenAI chat completion format, simplifying integration.

## UX/UI Features

1.  **Dynamic Tone Selection**: Users can choose from 5 distinct tones (Professional, Casual, Enthusiastic, Academic, Humorous) to tailor the output.
2.  **Real-time Feedback**:
    - **Loading Animation**: A cycling text animation ("Brainstorming...", "Structuring...", "Drafting...") keeps the user engaged during the generation process.
    - **Toast Notifications**: Non-intrusive popups for success/error messages (e.g., "Blog generated successfully!", "Copied to clipboard").
3.  **Typewriter Effect**: The generated blog is revealed paragraph-by-paragraph with a smooth fade-in animation, mimicking the writing process.
4.  **History Management**: Recent drafts are saved to the browser's `localStorage`, allowing users to revisit previous generations even after refreshing the page.
5.  **Theme Toggle**: Fully supported Light and Dark modes with persistent preference storage.
6.  **Utility Features**: One-click "Copy to Clipboard" and "Download as Markdown" buttons.

## Dynamic Prompt Handling

To ensure high-quality output that meets the 1000-word requirement, we employ a multi-step prompting strategy:

1.  **System Prompt Engineering**:
    - We define a strict persona: *"You are a top-tier blog writer."*
    - We enforce structural rules: *"Use proper Markdown (H1, H2, H3)", "NO conversational filler", "Aim for ~1000 words".*
2.  **User Prompt Construction**:
    - The user's topic is combined with the selected tone to create a specific instruction: *"Write a blog post about: '{prompt}'. Tone: {tone}."*
3.  **Completeness Check (`is_incomplete`)**:
    - A custom Python function analyzes the generated output.
    - **Logic**: If the text ends abruptly (no punctuation), ends with a header, or is significantly under the word count (< 900 words), it triggers a **continuation loop**.
    - **Continuation**: The model is prompted to *"Continue this blog matching the {tone} tone, without repeating"* to seamlessly extend the content to the desired length.

## Demonstration Guide

1.  **Launch**: Run `python app.py` and open `http://127.0.0.1:5000`.
2.  **Enter Prompt**: Type a topic, e.g., *"The Future of Remote Work"*.
3.  **Select Tone**: Choose *"Professional"* from the dropdown.
4.  **Generate**: Click **Generate Blog**. Watch the loading animation cycle through phases.
5.  **View Result**: The blog will appear with a typewriter effect.
6.  **Interact**:
    - Click the **Copy** icon to copy the text.
    - Click the **Download** icon to save as `.md`.
    - Scroll down to see the "Back to Top" button appear.
    - Refresh the page to see the blog saved in the "Recent Drafts" history section.
