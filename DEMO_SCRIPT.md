# 2-Minute Video Demo Script

**Goal:** Explain the tech stack, design decisions, and demonstrate the "Text Prompt to Blog" platform.
**Time:** ~2 Minutes

---

## Part 1: Introduction & Tech Stack (0:00 - 0:45)

**(Camera on you or Screen showing the Code/Architecture)**

"Hi, I'm [Your Name], and this is my submission for the Fullstack Developer assessment at FlocCare. I've built a **Text-to-Blog Generator** that turns simple prompts into comprehensive, 1000-word articles.

For the **Tech Stack**, I chose:
*   **Backend:** Python Flask. It's lightweight and perfect for handling API requests and serving our application.
*   **Frontend:** Vanilla HTML, CSS, and JavaScript. I wanted to demonstrate that we can build a premium, responsive UI without the overhead of heavy frameworks like React for this specific use case.
*   **AI Model:** I'm using the **GPT-OSS-120B** model via the Hugging Face Inference API. I chose a 120-billion parameter model because generating a coherent, long-form blog requires deep reasoning capabilities that smaller models just don't have. It's also open-source and free to use, meeting the assessment criteria."

---

## Part 2: UX/UI & Features (0:45 - 1:15)

**(Screen recording of the Web Page)**

"Let's look at the User Experience. I focused on a clean, **Glassmorphism design** that feels modern and professional.

*   **Dynamic Input:** We have a rotating placeholder here to inspire users with topic ideas.
*   **Tone Selector:** This is a key feature. Users can choose a tone—like 'Professional', 'Casual', or 'Humorous'. This dynamically adjusts the system prompt sent to the AI, ensuring the output matches the user's intent.
*   **Theme Toggle:** We have a fully functional Dark Mode because developer experience matters!"

---

## Part 3: Live Demonstration (1:15 - 1:50)

**(Action: Type a prompt and click Generate)**

"Let's generate a blog about **'The Future of Remote Work'** with a **'Professional'** tone.

**(Action: Point to the loading state)**
While it generates, notice the **Dynamic Loading State**. Instead of a boring spinner, we cycle through phases like 'Brainstorming', 'Structuring', and 'Drafting'. This keeps the user engaged and provides transparency into the process.

**(Action: Wait for generation to finish)**
And here is our result.
*   **Typewriter Effect:** The content reveals itself smoothly, mimicking the writing process.
*   **Quality Check:** The system ensures the blog is approximately 1000 words. If the model stops early, my backend logic detects it and automatically triggers a continuation to complete the article seamlessly.
*   **Markdown Rendering:** It's fully formatted with headers and bullet points."

---

## Part 4: Conclusion (1:50 - 2:00)

**(Action: Show Copy/Download buttons and History)**

"Finally, users can **Copy to Clipboard**, **Download as Markdown**, or revisit previous generations in the **History Section** below.

This platform delivers a robust, user-friendly experience for generating high-quality content. Thank you for watching!"
