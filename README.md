# ☕ Espresso Horoscope MCP

A local-first MCP server that reads real espresso shot metrics and a birth date, then generates a personalised "cosmic" reading — running fully offline using a local GPT-OSS model via LM Studio.

Demo: Watch the 3-minute demo (Sep 2025)

Why This Exists
Built for the OpenAI Open Model Hackathon (Aug–Sep 2025), co-hosted by Hugging Face, NVIDIA, Ollama, LM Studio, and vLLM. The challenge: apply gpt-oss-20b or gpt-oss-120b in creative, unexpected ways.

My entry was in the Best Local Agent category — the most useful agentic application of gpt-oss with no internet access.

The honest learning goal: I wanted to get my hands dirty with local model inference under real constraints. The best way I know to learn something properly is to put myself under pressure with a time-bound deliverable. A six-week hackathon with a real submission deadline does that better than any tutorial. The horoscope framing is deliberately playful — but the architecture underneath it is serious.

The goal is not fortune-telling. It's to demonstrate a reproducible, offline-first local agent pattern that combines real sensor data with local LLM inference through MCP.

What It Does
Espresso Horoscope MCP connects shot data from an espresso machine to a local LLM, which generates a short personalised "cosmic" reading based on:

Extraction metrics: pressure, temperature, flow rate, extraction time

Birth date input from the user

Historical shot tracking — readings accumulate per user, with the latest on top

The system runs with Wi-Fi completely off. No API calls. No cloud. Everything happens on-device.

## Architecture
flowchart TD
    A(["☕ Espresso Machine\nPressure · Temperature · Flow Rate · Time"])

    A --> B

    subgraph MCP ["🔧 Espresso Horoscope MCP Server"]
        direction TB
        B["📥 Shot Data Ingestor\nParses and normalises extraction metrics"]
        B --> C
        C["🎂 Birth Date Parser\nUser input → astrological context"]
        C --> D
        D["📜 Prompt Builder\nCombines shot metrics + birth date\ninto horoscope-style prompt"]
        D --> E
        E["🗂️ History Tracker\nLongitudinal reading storage\nLatest card on top"]
    end

    E --> F

    F[("🧠 GPT-OSS (Local)\nRunning via LM Studio\nFully offline — no internet")]

    F --> G

    G(["🔮 Cosmic Reading Card\nPersonalised to your shot + birthday\nTimestamped · Accumulates over time"])

    style MCP fill:#1a1a2e,stroke:#c8a96e,stroke-width:2px,color:#ffffff
    style A fill:#2a1a0e,stroke:#c8a96e,stroke-width:2px,color:#ffffff
    style F fill:#16213e,stroke:#c8a96e,stroke-width:2px,color:#ffffff
    style G fill:#2a1a0e,stroke:#c8a96e,stroke-width:2px,color:#ffffff
    style B fill:#1a1a2e,stroke:#8b6914,stroke-width:1.5px,color:#ffffff
    style C fill:#1a1a2e,stroke:#8b6914,stroke-width:1.5px,color:#ffffff
    style D fill:#1a1a2e,stroke:#8b6914,stroke-width:1.5px,color:#ffffff
    style E fill:#1a1a2e,stroke:#8b6914,stroke-width:1.5px,color:#ffffff

Technical Highlights
Local-first inference via LM Studio
GPT-OSS runs entirely on-device through LM Studio. The MCP server communicates with the local model endpoint — no OpenAI API key, no cloud dependency, no data leaving the machine.

Real sensor data as LLM context
The input to the model is not freeform text — it's structured extraction metrics (pressure curve, temperature, flow rate, yield time) translated into a semantically rich prompt. This demonstrates the MCP pattern for domain-specific, structured-data-to-LLM pipelines.

Longitudinal memory
The system tracks readings per user (keyed by birth date). Each new shot generates a new card. Cards accumulate with the latest on top — building a personal "coffee journey" over time. This is a minimal implementation of longitudinal agent memory without a vector store.

Dynamic horoscope style generation
GPT-OSS handles stylistic variation — the same birth date + different shot metrics produces a different reading. The model is prompted to write in distinct horoscope archetypes, so the output never feels templated.

What I Learned
LM Studio as a local inference server is genuinely usable for rapid prototyping. The OpenAI-compatible endpoint makes swapping between cloud and local trivial — the MCP server doesn't know which it's talking to.

Structured sensor data → LLM prompt requires more normalisation than expected. Raw espresso metrics (e.g., 9.1 bar, 93°C, 28s) need semantic framing before they're useful in a prompt. A "good shot" and a "bad shot" look very similar to a model without domain context.

MCP as an offline agent framework works well when the tool contract is strict. No hallucinated API calls, reliable schema enforcement, clean separation between data ingestion and model interaction.

Scope under time pressure is a skill. Six weeks, a full-time job, and a hard submission deadline. The history tracker and dynamic style system were scoped in during week four when the core was stable. Knowing what to cut — and what to add — under real constraints is different from planning in the abstract.

Limitations
Shot data in the demo is simulated. A real hardware integration (e.g., Decent DE1, La Marzocco with API access) would make this production-grade.

Birth date as a user key is a proxy for identity. A real multi-user system would need proper session management.

Horoscope style archetypes are hardcoded in the prompt template. A fine-tuned model would produce more consistent stylistic variation.

Tech Stack
Layer	Tool
Agent protocol	Model Context Protocol (MCP)
Local inference	GPT-OSS-20B via LM Studio
Runtime	Node.js
Data input	Simulated espresso shot metrics
Memory	In-process longitudinal store
Hackathon Context
Event: OpenAI Open Model Hackathon, Aug–Sep 2025
Category entered: Best Local Agent
Co-sponsors: Hugging Face · NVIDIA · Ollama · LM Studio · vLLM
Submission requirement: Fully offline, no internet access during execution

License
MIT

Built by Vivid Savitri-Hampton
