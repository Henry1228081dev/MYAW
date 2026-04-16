# Agentic Workflows (MYAW)

This repository contains a powerful Agentic Workflow system built on a 3-layer architecture. It is designed to bridge the gap between probabilistic LLM decision-making and deterministic business logic execution.

## 🏗️ The 3-Layer Architecture (DO Framework)

### Layer 1: Directive (The "SOP" Layer)
Located in `directives/`. This layer contains standard operating procedures (SOPs) written in Markdown. They define goals, inputs, tools, and outputs—much like instructions for a human employee.

### Layer 2: Orchestration (The "Decision" Layer)
This is the AI Orchestrator (Antigravity). Its job is to read directives, call execution tools in the correct order, handle errors, and learn from mistakes. If no directive exists, the Orchestrator acts as a **Directive Architect** to build one.

### Layer 3: Execution (The "Action" Layer)
Located in `execution/`. This layer contains deterministic Python scripts that perform the actual work (scraping, API calls, file processing, etc.). This ensures reliability and speed.

## 🚀 Getting Started

1.  **Configuration**: Copy `.env.example` to `.env` and fill in your API keys and environment variables.
2.  **Directives**: Explore the `directives/` folder to see available workflows (Lead Gen, Upwork Automation, etc.).
3.  **Execution**: Scripts in `execution/` can be run directly or through the Orchestrator.

## 📂 Project Structure

-   `.agents/skills/`: Custom capabilities and skills for the agent.
-   `directives/`: SOPs for various workflows.
-   `execution/`: Python scripts for task execution.
-   `tmp/`: Temporary processing directory (ignored by Git).
-   `docs/`: Project documentation and reference guides.

## 🛠️ Key Skills
-   **Lead Generation**: Google Maps and SERP scraping.
-   **Job Automation**: Upwork scraping and application management.
-   **Content Analysis**: Video and transcript processing.
-   **System Audits**: Pre-push codebase audits and performance optimization.

---
*Built with ❤️ by the Advanced Agentic Coding team.*
