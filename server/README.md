# AI-HR Recruitment Simulator Backend

A zero-dependency Node.js REST API for the AI-HR-Recruitment-Simulator frontend.

## Run

From the project root:

```bash
npm install
npm run server
```

The API runs on `http://localhost:8000`.

In another terminal:

```bash
npm run dev
```

The Vite frontend runs on its normal development port.

## Demo accounts

- Candidate: `candidate@demo.com` / `Demo1234`
- Recruiter: `recruiter@demo.com` / `Demo1234`

## Implemented API

- Authentication: register, login, forgot-password request, change password
- Candidate profile and applications
- Jobs and job details
- Job application submission with match-score calculation
- PDF resume upload and basic text/skill extraction
- Recruiter candidate ranking
- Natural-language HR Copilot candidate filtering
- Interview answer submission and evaluation scoring
- Notifications and notification preferences
- Persistent JSON data store under `server/data/database.json`

## Resume parsing

If the machine has `pdftotext` installed, uploaded PDF text is extracted and scanned for common skills, contact information, education, and experience. If it is unavailable, the API still accepts the PDF but only has limited information to infer.

For production, replace the development token secret with the `JWT_SECRET` environment variable and move the JSON store to a real database.
