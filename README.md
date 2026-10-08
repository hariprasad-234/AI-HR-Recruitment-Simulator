# AI HR Recruitment Simulator 🤖📄

An AI-powered hiring platform designed to transform recruitment into a smarter, faster, and more data-driven process. This project helps HR teams review resumes, evaluate candidates, match them to job roles, and interact with an intelligent recruiter assistant.

## 🌟 Overview

AI HR Recruitment Simulator brings together resume analysis, candidate evaluation, and recruiter assistance in a single modern platform. It helps hiring teams make informed decisions with less manual effort and better speed.

## ✨ Key Features

- Resume-based candidate evaluation 📄
- AI-driven job matching and ranking 🎯
- Recruiter dashboard for hiring insights 📊
- HR Copilot assistant for natural-language queries 💬
- Candidate filtering by skills, score, and location 🧠
- Modern and responsive user interface for HR teams 🖥️
- Integrated Node.js REST API for authentication, jobs, applications, resume uploads, notifications, and interviews 🔧

## 🏗️ Tech Stack

- React.js ⚛️
- Vite ⚡
- React Router DOM 🧭
- Node.js REST API 💚
- JavaScript / JSX 💻
- CSS styling 🎨
- JSON-file persistence for local development 🔌

## 🚀 Project Goals

- Reduce manual screening time ⏱️
- Improve recruitment accuracy with AI-assisted evaluation 🧠
- Build a recruiter-friendly user experience 👩‍💼
- Provide a working local backend for recruitment workflows 🤝

## 🧩 Core Modules

- Authentication and user access 🔐
- Candidate dashboard and evaluation 📋
- Job matching and ranking 🧾
- HR Copilot assistant 🤖
- Recruiter filtering and shortlist workflow 🧑‍💼

## 📁 Project Structure

```bash
src/
├── App.jsx
├── main.jsx
├── Routes/
├── pages/
├── components/
├── Hooks/
├── Services/
├── context/
├── data/
└── assets/
server/
├── index.js
└── README.md
```

## 🛠️ Getting Started

### Install dependencies

```bash
npm install
```

### Run the backend

```bash
npm run server
```

The API runs at `http://localhost:8000`. In a second terminal, start the frontend:

```bash
npm run dev
```

Then open:

```text
http://localhost:5173
```

The backend uses a local JSON database in `server/data/`; this runtime data is ignored by Git. Demo accounts for local development are documented in [server/README.md](./server/README.md). Set a private `JWT_SECRET` environment variable before using the server outside local development.

## 🤖 HR Copilot Feature

The HR Copilot interface allows recruiters to ask natural-language questions such as:

- Show me top Python candidates 🐍
- Who are the best React developers? ⚛️
- Candidates with score above 85 📈
- Top candidates in Chennai 📍

This feature helps recruiters quickly explore candidate matches and shortlist suitable applicants using conversational prompts.

## 📌 Future Enhancements

- Integration with a production AI model for resume analysis and copiloting 🤖
- Resume parsing using NLP and ML 🧠
- Interview scheduling automation 📅
- Candidate analytics dashboard 📈
- Enhanced recruiter insights and reporting 📊

## Task 10 API integration

The settings and notification screens use the API base URL from `VITE_API_BASE_URL` (defaults to `http://localhost:8000`) and send a bearer token from `localStorage` under `token` when present. The backend must provide:

- `GET /api/notifications` returning an array or `{ "notifications": [] }` with `id`, `title` or `message`, optional `created_at`, and `read` or `is_read`.
- `PATCH /api/notifications/{id}/read` to mark a notification read.
- `GET /api/settings` returning notification preferences.
- `PATCH /api/settings/notifications` accepting `{ "email": boolean, "in_app": boolean, "interview_updates": boolean }`.
- `POST /api/auth/change-password` accepting `{ "current_password": string, "new_password": string }`.
- `POST /api/copilot/query` accepting the query, filters, and history described in `src/Services/copilotService.js`.

Copy `.env.example` to `.env` for local configuration. Set `VITE_API_BASE_URL` to the backend URL when it is not running at `http://localhost:8000`. Copilot uses the API by default; set `VITE_USE_MOCK=true` only to opt into its local sample data. The included local backend implements the application API; live API behavior should also be verified against the deployed service.

## 🤝 Team Contribution

This project is built as a collaborative effort across frontend, backend, and AI modules to create a complete digital hiring ecosystem.

## ⭐ Mission

To make hiring smarter, faster, and more efficient through the power of AI and intuitive design.
