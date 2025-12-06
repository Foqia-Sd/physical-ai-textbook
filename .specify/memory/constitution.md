<!--
Sync Impact Report:
Version change: 0.0.0 (template) -> 0.0.1
Modified principles:
  - PROJECT_NAME -> AI-Native Physical AI Textbook
  - PRINCIPLE_1_NAME -> Modularity & Reusability
  - PRINCIPLE_2_NAME -> API-First Design
  - PRINCIPLE_3_NAME -> AI-Driven Content
  - PRINCIPLE_4_NAME -> User Experience Focus
  - PRINCIPLE_5_NAME -> Deployment & Scalability
  - PRINCIPLE_6_NAME -> Quality Assurance
  - SECTION_2_NAME -> Non-Goals
  - SECTION_3_NAME -> Development Workflow
  - GOVERNANCE_RULES -> Standard Governance
Added sections: None
Removed sections: None
Templates requiring updates:
  - .specify/templates/plan-template.md (⚠ pending)
  - .specify/templates/spec-template.md (⚠ pending)
  - .specify/templates/tasks-template.md (⚠ pending)
  - .specify/templates/commands/sp.constitution.md (⚠ pending)
  - .specify/templates/commands/sp.phr.md (⚠ pending)
Follow-up TODOs: None
-->
# AI-Native Physical AI Textbook Constitution

## Core Principles

### I. Modularity & Reusability
The textbook content MUST be structured into multiple independent Markdown chapters to facilitate easy organization, reusability, and future expansion.

### II. API-First Design
The RAG chatbot backend MUST expose its functionality via a FastAPI interface with clearly defined `/ingest` and `/query` endpoints, ensuring a standardized and extensible communication protocol.

### III. AI-Driven Content
The RAG chatbot MUST leverage Gemini for both embedding text and generating answers, utilizing Gemini Flash for cost-effective and efficient responses. Qdrant MUST be used as the vector database for efficient retrieval of relevant information. Highlight-based answers MUST be supported to provide precise context from the textbook.

### IV. User Experience Focus
A ChatWidget MUST be seamlessly integrated into the Docusaurus frontend to provide an intuitive and interactive user experience for the RAG chatbot.

### V. Deployment & Scalability
The frontend (Docusaurus) MUST be deployable on GitHub Pages or Vercel, and the backend (FastAPI) MUST be deployable on Railway or Render, utilizing free-tier services where possible to ensure accessibility and minimize operational costs.

### VI. Quality Assurance
The project MUST ensure the textbook is complete, the RAG chatbot functions reliably without hallucinations, and highlight-based answers work accurately. Both frontend and backend deployments MUST be live and fully operational.

## Non-Goals

Authentication, large datasets, heavy compute, and paid APIs are explicitly out of scope for this project to maintain a free-tier focus and streamline development.

## Development Workflow

The project MUST adhere to the Spec-Kit Plus and Claude Code workflows for specification, planning, task management, and implementation.

## Governance

This constitution supersedes all other practices. Amendments require thorough documentation, approval by the project lead, and a clear migration plan for any affected components. All pull requests and code reviews MUST verify compliance with these principles. Complexity MUST always be justified and aligned with project goals.

**Version**: 0.0.1 | **Ratified**: 2025-12-04 | **Last Amended**: 2025-12-04
