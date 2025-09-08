# Espresso Horoscope — Cursor Charter

## Purpose
Ship an offline MVP that consumes **Gaggiuino MCP** shot data (replayed) and applies **gpt-oss** locally for optional phrasing.

## Hard requirements
- Data source: **Gaggiuino MCP** tool outputs (`getShotData`) recorded to JSON and replayed.
- Normalization: write `data_sources/gaggiuino_loader.py` to convert MCP JSON → our schema.
- Offline default: no network calls in runtime. Optional local **gpt-oss** via `--style gptoss`.
- Deliverables: `make demo` builds `out/cards.md` from `sample/mcp_shots/*.json`.

## Acceptance tests (Cursor must satisfy)
- `python tools/record_from_mcp.py sample/mcp_shots/*.json -o data/shots.jsonl` creates a JSONL file with keys:
  `timestamp, target_mass_g, pressure_bar[], flow_ml_s[], temp_c[], pump_pct[], preinfusion_ms, first_drip_s, shot_end_s`.
- `python features/extract.py data/shots.jsonl -o data/features.jsonl` writes N lines, one per shot.
- `python cli/cards.py --features data/features.jsonl --rules rules/diagnostics.yaml --astro content/astro_map.yaml --out out/cards.md` produces a markdown with at least 1 card.
- `grep -R "getShotData" -n data_sources tools` finds usage (proves MCP path exists).
- README shows **how to enable** local gpt-oss via Ollama and a `--style gptoss` flag.

## Links
- Gaggiuino MCP directory page (tools list & usage): https://glama.ai/mcp/servers/@AndrewKlement/gaggiuino-mcp


