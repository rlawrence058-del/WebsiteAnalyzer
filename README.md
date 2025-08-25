# 5MM Website Analyzer & Site Builder

### 1. Forking & Setup
1. Click "Fork" in the top-right corner of this Replit project.
2. In your fork, click the "Files" tab → create a file named `.env`.
3. Paste your OpenAI API key into `.env` as: OPENAI_API_KEY=sk-…

4. (Optional) If login is enabled, open `authorized_users.py` and add your email to `AUTHORIZED_EMAILS`.

### 2. Running the Analyzer
1. Click "Run" (green ▶️ button).  
2. A "Web View" pane will open on the right (Streamlit interface).
3. (If login is enabled) Enter your authorized email → click "Login."  
4. On the "Enter Your OpenAI API Key" screen, paste your key → click "Continue."  
5. In the main interface:
- Paste any local business website URL (e.g., `exampleplumbing.com`).
- Click **"Analyze Website."**
6. Wait for the analysis spinner. Once finished, you'll see:
- **Score (1–10)** with color (red/yellow/green).  
- **Plain-English Report** listing each deficiency.  
- **"Is This a Good Lead?"** (Yes/No + rationale).  
- **Replit Prompt** (copy-ready to generate a fresh site).  
- **Outreach Email** and **Outreach DM** templates (click "Copy" to copy text).  
7. To export:
- Click **"Copy All"** to copy everything to clipboard.  
- Click **"Download PDF"** to download a PDF of the report (optional).  
- Click **"Reset"** to clear and analyze another site.

### 3. Using the Replit Prompt
1. Copy the **entire contents** of the "Replit Prompt" box.  
2. Create a **new Replit AI Site Builder** or ChatGPT "create a site" session.  
3. Paste the prompt exactly.  
4. The AI will generate:
- **index.html** (homepage demo)  
- **blog.html** (blog index page)  
- An empty `/posts/` folder  
- A shared `styles.css` file  
5. Review, edit any content if needed (e.g., phone # or service wording).  
6. Click **Deploy → Static Site** in Replit to go live at `clientname.replit.app`.

### 4. Folder Structure After Site Build
