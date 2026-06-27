# 🛍️ Smart Shop Assistant

A lightweight, serverless conversational AI shopping assistant powered by **Groq Cloud (LLaMA 3.3 70B)** and **Gradio**. This project showcases native **Function Calling (Tool Use)** with an LLM, allowing the model to dynamically look up real-time product pricing from an internal inventory system when required, while falling back to natural conversation for general inquiries.

---

## 🚀 Architecture & Technical Overview

The assistant leverages an agentic design pattern utilizing deterministic tool invocation loops:

1. **User Request Assessment:** The user's query is intercepted and passed alongside structural JSON Schemas defining available tools to the `llama-3.3-70b-versatile` engine.
2. **Deterministic Tool Use:** If the model requires external state information (e.g., product pricing), it pauses textual completion and generates a structured `tool_calls` payload containing arguments conforming to the function specifications.
3. **Local State Invocation:** The execution layer unpacks the arguments via standard parsing routines, executes the local Python dictionary search algorithm, and attaches the resulting system evaluation payload using a dedicated `tool` execution role.
4. **Context Consolidation:** The final consolidated context window is fed back into Groq to emit a contextual, human-readable response.

---

## 📂 Project Repository Directory Layout

```text
Smart Shop Assistant/
├── .env                  # Local workspace secrets management (API Keys)
├── .gitignore            # Git exclusion directory management
├── agent.py              # LLM client logic, system instructions, and tool schemas
└── app.py                # Gradio UI presentation layer & state mapping
