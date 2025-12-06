---
id: "001"
title: "Initialize AI-Native Physical AI Textbook Constitution"
stage: "constitution"
date_iso: "2025-12-04"
surface: "agent"
model: "claude-opus-4-5-20251101"
feature: "AI-Native Physical AI Textbook"
branch: "1-cli-calculator"
user: "null"
command: "/sp.constitution"
labels: ["constitution", "project-setup"]
links:
  spec: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files_yaml:
  - .specify/memory/constitution.md
tests_yaml: []
---

## Prompt

```text
AI-Native Physical AI Textbook Short Constitution
Goal:
Create a Physical AI & Humanoid Robotics textbook in Docusaurus with a free-tier RAG chatbot using FastAPI, Gemini Embeddings + Gemini Flash, and Qdrant. Follow Spec-Kit Plus + Claude Code workflow.
Objectives:
•    Multi-chapter textbook (Markdown).
•    FastAPI backend for /ingest + /query.
•    Gemini for embeddings + answers.
•    Qdrant for retrieval.
•    Highlight-based answers.
•    ChatWidget integrated into Docusaurus.
•    Deploy: GitHub Pages/Vercel (frontend), Railway/Render (backend).
Success Criteria:
Book complete, RAG works reliably, highlight answers work, both deployments live, zero hallucinations.
Non-Goals:
Authentication, large datasets, heavy compute, paid APIs.
```

## Response

The project constitution at `.specify/memory/constitution.md` has been updated to version `0.0.1`. This is the initial version of the constitution for the "AI-Native Physical AI Textbook" project.

### Version Bump Rationale

This is the first version of the constitution, hence a `0.0.1` version.

### Files Flagged for Manual Follow-up

- `.specify/templates/plan-template.md`: Review "Constitution Check" section for alignment.
- `.specify/templates/spec-template.md`: Review for scope/requirements alignment.
- `.specify/templates/tasks-template.md`: Review for task categorization alignment.
- All command files under `.specify/templates/commands/` (e.g., `sp.constitution.md`, `sp.phr.md`, `sp.plan.md`, `sp.specify.md`, `sp.tasks.md`, `sp.analyze.md`, `sp.adr.md`, `sp.git.commit_pr.md`, `sp.implement.md`, `sp.checklist.md`, `sp.clarify.md`): These files were not found, so their alignment could not be verified. It's recommended to ensure any custom commands align with the new constitution.

