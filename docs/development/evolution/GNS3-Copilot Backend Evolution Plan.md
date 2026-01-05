

# 🏗️ GNS3-Copilot Backend Evolution Plan

## 1. Architectural Vision

Transition from a standalone Streamlit script to a **"Dual-Engine"** architecture.

* **Engine A (Legacy):** Streamlit `app.py` for rapid internal prototyping and debugging.
* **Engine B (Modern):** FastAPI `server.py` acting as a **BFF (Backend for Frontend)** to serve a modern React UI and mobile voice interaction.

---

## 2. Core Technical Strategy

* **Concurrency:** Use FastAPI's standard `def` routes to leverage the internal thread pool for handling synchronous GNS3 API calls and LangGraph execution.
* **Configuration:** Maintain `.env` driven settings (Local-First). Credentials (LLM Keys, GNS3 URL) are loaded via environment variables; no complex Auth required for local MVP.
* **Communication:** Implement **SSE (Server-Sent Events)** for real-time AI "typing" effects and tool-calling status updates.
* **Voice Integration:** Implement a "Relay" pattern: `Browser Mic -> FastAPI -> Commercial STT (Whisper) -> LangGraph -> Commercial TTS -> Browser Speaker`.

---

## 3. Implementation Roadmap

### Phase 1: API Infrastructure (Foundation)

* **Goal:** Establish the FastAPI project structure and enable cross-origin communication.
* **Tasks:**
1. Install `fastapi` and `uvicorn`.
2. Create `api/main.py` with **CORS** middleware (essential for React).
3. Set up the router directory structure for scalability.



### Phase 2: LangGraph Integration (The "Brain")

* **Goal:** Expose the LangGraph agent as a unified, streaming API.
* **Tasks:**
1. Develop the `POST /agent/stream` endpoint.
2. Wrap the synchronous `graph.stream` using `asyncio.to_thread` or an event-pumping queue.
3. Define a standard SSE message schema (e.g., `type: text` for content, `type: tool` for action status).



### Phase 3: Voice Interaction Pipeline

* **Goal:** Enable voice-to-command capabilities using commercial APIs.
* **Tasks:**
1. Create `POST /agent/voice-chat` to receive audio files (`.webm`/`.wav`).
2. Integrate **OpenAI Whisper API** for STT (Speech-to-Text).
3. Connect transcribed text to the existing LangGraph logic and optionally return audio via TTS.



### Phase 4: Project & Topology Services

* **Goal:** Provide the frontend with GNS3 project metadata.
* **Tasks:**
1. Implement `GET /projects` to list available GNS3 topologies.
2. Implement `GET /projects/{id}/topology` for React Flow visualization data.



---

## 4. Recommended Project Structure

```text
src/gns3_copilot/
├── api/
│   ├── __init__.py
│   ├── main.py              # Entry point & Middleware config
│   ├── dependencies.py      # Shared logic (Context/Config)
│   └── routers/
│       ├── __init__.py
│       ├── agent.py         # Chat, Streaming, and Voice endpoints
│       └── projects.py      # Project & Topology management
├── tools/                   # Existing Sync GNS3 Tools (Unchanged)
├── agent/                   # Existing LangGraph Logic (Unchanged)
└── .env                     # Local API Keys & GNS3 Server config

```

---

## 5. Current Sprint Checklist

* [ ] **Setup**: Run `pip install fastapi uvicorn pydantic-settings`.
* [ ] **Scaffolding**: Create the `api/` directory and initialize `main.py`.
* [ ] **Core API**: Implement the `/agent/stream` endpoint and verify via Swagger UI (`/docs`).
* [ ] **Testing**: Ensure the API correctly reads `.env` variables without manual injection.

