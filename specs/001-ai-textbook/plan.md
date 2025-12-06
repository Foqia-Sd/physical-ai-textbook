# Implementation Plan: AI-Native Physical AI Textbook

## 1. Technical Context

This plan outlines the implementation strategy for the AI-Native Physical AI Textbook, leveraging the provided constitution and user requirements. The project will involve developing a Docusaurus-based textbook, a FastAPI RAG backend, an OpenAI Agents RAG agent, and a Docusaurus ChatWidget frontend, with deployment to GitHub Pages and Railway/Render.

### System Overview
The system comprises a Docusaurus frontend for the textbook and chat widget, a FastAPI backend for RAG functionalities, and an OpenAI-based RAG agent. Qdrant Cloud and Neon Postgres will be used for data storage.

### Key Technologies
- **Frontend**: Docusaurus, ChatKit SDK
- **Backend**: FastAPI, Qdrant Cloud, Neon Postgres
- **AI/RAG**: OpenAI Agents, Gemini (for embeddings and answers - clarified in Constitution III. AI-Driven Content)
- **Deployment**: GitHub Pages (frontend), Railway/Render (backend)

## 2. Constitution Check

The plan adheres to the following core principles from the constitution:

- **I. Modularity & Reusability**: The plan outlines distinct components (Book, Backend, Agents, Frontend), promoting modularity.
- **II. API-First Design**: The backend explicitly defines `/ingest` and `/query` FastAPI endpoints.
- **III. AI-Driven Content**: Utilizes Gemini for embeddings and answers, Qdrant for vector database, and supports highlight-based answers.
- **IV. User Experience Focus**: Integrates a ChatWidget into the Docusaurus frontend.
- **V. Deployment & Scalability**: Specifies deployment to GitHub Pages and Railway/Render, prioritizing free-tier services.
- **VI. Quality Assurance**: Implicitly covered by the structured plan and the need for functional components.

Non-goals (Authentication, large datasets, heavy compute, paid APIs) are respected by the specified technologies and deployment targets.

## 3. Implementation Phases

### Phase 0: Setup and Core Infrastructure

1.  **Book Setup**:
    *   Scaffold Docusaurus documentation site using Spec-Kit.
    *   Initialize Git repository and link to GitHub.

2.  **Backend Setup**:
    *   Set up a FastAPI project.
    *   Configure Qdrant Cloud instance.
    *   Configure Neon Postgres instance.
    *   Implement basic `/health` endpoint for testing.

3.  **Agent Setup**:
    *   Set up OpenAI Agents environment.
    *   Integrate ChatKit SDK.

### Phase 1: Book Content & Backend Ingestion

1.  **Book Content Creation**:
    *   Define chapter structure for the Docusaurus book.
    *   Use Claude Code to write initial chapters in Markdown format.
    *   Set up GitHub Pages deployment for Docusaurus.

2.  **Backend Ingest Endpoint**:
    *   Develop `/ingest` endpoint in FastAPI.
    *   Process Markdown content into chunks.
    *   Generate embeddings using Gemini.
    *   Store chunks and embeddings in Qdrant.
    *   Store metadata (original MD, highlights) in Neon Postgres.

### Phase 2: Backend Query & RAG Agent Development

1.  **Backend Query Endpoint**:
    *   Develop `/query` endpoint in FastAPI.
    *   Receive user questions.
    *   Generate embeddings for questions using Gemini.
    *   Retrieve relevant chunks from Qdrant.
    *   Retrieve original content/highlights from Neon Postgres based on chunks.
    *   Generate answers using Gemini, incorporating highlight-based answers.

2.  **RAG Agent Implementation**:
    *   Create a RAG Agent with OpenAI Agents + ChatKit SDK.
    *   Implement `retriever` tool to call the FastAPI `/query` endpoint.
    *   Implement `highlight_extractor` tool for precise answer highlighting.
    *   Implement `personalize` tool (optional, for future enhancements).
    *   Connect agent tools to the FastAPI backend.

### Phase 3: Frontend Integration & Deployment

1.  **Frontend ChatWidget Integration**:
    *   Integrate ChatWidget into the Docusaurus site.
    *   Connect ChatWidget to the backend `/query` endpoint via the ChatKit runtime.
    *   Implement UI for displaying highlight-based answers.

2.  **Deployment Finalization**:
    *   Deploy FastAPI backend to Railway or Render.
    *   Finalize GitHub Pages deployment for Docusaurus frontend.
    *   Verify end-to-end functionality across deployed components.

## 4. Risks and Mitigation

1.  **Gemini API Rate Limits/Cost**:
    *   Risk: Exceeding free-tier limits during development/testing.
    *   Mitigation: Implement caching for embeddings and answers where appropriate; monitor API usage closely.

2.  **Qdrant/Neon Postgres Integration Complexity**:
    *   Risk: Difficulties in connecting and managing data across vector and relational databases.
    *   Mitigation: Use clear ORM/client libraries; thoroughly test data flow between components early.

3.  **ChatKit SDK/OpenAI Agents Compatibility**:
    *   Risk: Integration challenges between different AI SDKs.
    *   Mitigation: Follow documentation closely, create minimal reproducible examples for testing integrations.

## 5. Follow-ups

- Detailed API contract definitions for `/ingest` and `/query` endpoints.
- Specific environment variable management strategy for API keys and database credentials.
- Comprehensive testing strategy for each component and end-to-end RAG functionality.
