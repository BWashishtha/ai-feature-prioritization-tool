# 🛠️ AI Feature Prioritization Tool

A full-stack AI-powered web app that helps early-stage startups, product managers, and founders prioritize user feature requests.  
It uses LLMs (via OpenRouter API) to automatically categorize features based on **Impact** and **Effort**, saving valuable time in product decision-making.

---

## ✨ Key Features

- 📋 Submit multiple user feature requests
- 🚀 AI categorizes features into:
  - High Impact / Low Effort
  - High Impact / High Effort
  - Low Impact / Low Effort
  - Low Impact / High Effort
- ♻️ Reset all fields with one click
- ⬇️ Download prioritized results as a `.txt` file
- 📱 Fully mobile-responsive design
- 🔥 Fast, smooth user experience with React + TailwindCSS

---

## 🛠️ Tech Stack

- **Frontend:** React.js, Vite, TailwindCSS, React Toastify, React Spinners
- **Backend:** Flask (Python), OpenRouter AI API
- **Deployment:** 
  - Backend hosted on Render.com
  - Frontend hosted on Vercel.com

---

## 🛎️ How to Run Locally

### 1. Clone the Repo

```bash
git clone https://github.com/BWashishtha/ai-feature-prioritization-tool.git
cd ai-feature-prioritization-tool
cd backend
pip install -r requirements.txt
python app.py
cd frontend
npm install
npm run dev
```
🌍 Live Deployment
🔗 Frontend: Vercel Live Link - Coming Soon

🔗 Backend: Render Live Link - Coming Soon

🚀 Future Improvements
Export prioritized features to .csv format
Weight features based on user votes or impact scores
Visualize feature prioritization in a 2x2 Impact vs Effort quadrant chart
Add basic user authentication for saving prioritization sessions

