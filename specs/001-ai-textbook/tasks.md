# Feature Tasks: AI-Native Physical AI Textbook

This document outlines the tasks for implementing the AI-Native Physical AI Textbook, following the plan detailed in `specs/001-ai-textbook/plan.md`.

## Task 1: Write Docusaurus Chapters

**Description**: Write two initial chapters for the Docusaurus textbook.

### Sub-tasks:

1.  **Module 1: ROS 2 Basics**
    *   Create `docs/module1-ros2-basics.md`.
    *   Cover ROS 2 concepts: nodes, topics, services.
    *   Include `rclpy` examples for Python.
    *   Explain URDF (Unified Robot Description Format) for robot modeling.
    *   Refer to Context-7 MCP documentation for accuracy.

2.  **Module 2: Digital Twin Fundamentals**
    *   Create `docs/module2-digital-twin-fundamentals.md`.
    *   Cover Gazebo for physics simulation.
    *   Explain Unity for Human-Robot Interaction (HRI).
    *   Discuss common sensor types: LiDAR, Depth, IMU.
    *   Refer to Context-7 MCP documentation for accuracy.

## Module 3: The AI-Robot Brain (NVIDIA Isaac™)

- **Focus:** Advanced perception and training  
- **NVIDIA Isaac Sim:** Photorealistic simulation and synthetic data generation  
- **Isaac ROS:** Hardware-accelerated VSLAM (Visual SLAM) and navigation  
- **Nav2:** Path planning for bipedal humanoid movement  

---

## Module 4: Vision-Language-Action (VLA)

- **Focus:** The convergence of LLMs and Robotics  
- **Voice-to-Action:** Using OpenAI Whisper for voice commands  
- **Cognitive Planning:** Using LLMs to translate natural language (e.g., “Clean the room”) into a sequence of ROS 2 actions  
- **Capstone Project: The Autonomous Humanoid**  
  - A simulated robot receives a voice command  
  - Plans a path  
  - Navigates obstacles  
  - Identifies an object with computer vision  
  - Manipulates it  

---

## Task 2: Scaffold FastAPI Backend

**Description**: Set up the core FastAPI backend with ingest and query capabilities, integrated with Qdrant and Neon Postgres.

### Sub-tasks:

1.  **FastAPI Project Initialization**
    *   Create a new FastAPI project structure.
    *   Implement basic `/health` endpoint.

2.  **Qdrant Cloud Integration**
    *   Set up Qdrant client and connection.
    *   Define vector collection for embeddings.

3.  **Neon Postgres Integration**
    *   Set up SQLAlchemy/Alembic for database migrations.
    *   Define schema for storing document metadata and highlights.

4.  **Ingest Endpoint Scaffold**
    *   Create `/ingest` endpoint handler (initial empty function).
    *   Outline steps for Markdown processing, embedding generation, and storage.

5.  **Query Endpoint Scaffold**
    *   Create `/query` endpoint handler (initial empty function).
    *   Outline steps for question embedding, retrieval, and answer generation.

## Task 3: Scaffold ChatWidget + ChatKit/Agents RAG Integration

**Description**: Integrate the ChatWidget into Docusaurus and connect it to the RAG agent and backend.

### Sub-tasks:

1.  **Docusaurus ChatWidget Integration**
    *   Identify appropriate Docusaurus component for ChatWidget placement.
    *   Add ChatWidget component to the Docusaurus frontend.

2.  **ChatKit SDK Setup**
    *   Initialize ChatKit SDK in the Docusaurus frontend.
    *   Configure ChatKit to connect to the RAG agent runtime.

3.  **RAG Agent Stub**
    *   Create a placeholder RAG Agent using OpenAI Agents framework.
    *   Define `retriever` and `highlight_extractor` tool stubs.
    *   Connect agent tools to the FastAPI backend (initially placeholder calls).

## Acceptance Criteria for all tasks:

- All specified files and directories are created.
- Placeholder code structures are in place for all endpoints, components, and tools.
- No functional implementation beyond scaffolding is required at this stage.
