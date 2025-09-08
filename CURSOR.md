
# Espresso Horoscope (Cursor Charter)

## Purpose

Ship an offline MVP that consumes **Gaggiuino MCP** shot data (recorded/replayed) and applies **gpt-oss:20b** locally for optional phrasing. Default run is deterministic with no network.

## Non-negotiables

- Data source: recorded outputs from **Gaggiuino MCP** tools (`getShotData`).
- Normalisation: `data_sources/gaggiuino_loader.py` converts MCP JSON → our schema.
- Offline default: no HTTP calls in runtime.
- gpt-oss use: add `--style gptoss` path that calls a local **`gpt-oss:20b`** via Ollama.
- Deliverable: `make demo` builds `out/cards.md` from `sample/mcp_shots/*.json` (or simulator fallback).

## Repo layout

features/extract.py
rules/diagnostics.yaml
content/astro_map.yaml
content/cosmic_lexicon.yaml
data_sources/gaggiuino_loader.py
tools/record_from_mcp.py
tools/simulate_shots.py
cli/cards.py
web/app.py
sample/mcp_shots/*.json

markdown
Copy code

## Acceptance tests

1) **Normalize MCP**`python tools/record_from_mcp.py sample/mcp_shots/*.json -o data/shots.jsonl`Output JSONL lines include:`timestamp,target_mass_g,pressure_bar[],flow_ml_s[],temp_c[],pump_pct[],preinfusion_ms,first_drip_s,shot_end_s`
2) **Extract**`python features/extract.py data/shots.jsonl -o data/features.jsonl`Each line has:`brew_ratio,peak_pressure_bar,shot_end_s,temp_avg_c,flow_avg_ml_s,channeling_score_0_1`
3) **Render**`python cli/cards.py --features data/features.jsonl --rules rules/diagnostics.yaml --astro content/astro_map.yaml --out out/cards.md`Produces at least one Markdown card.
4) **Hooks present**
   `grep -R "getShotData" -n data_sources tools` finds an MCP path.
   `grep -R "OPENAI_BASE_URL" -n cli` finds the gpt-oss hook.

## Tasks for Cursor

- Implement `data_sources/gaggiuino_loader.py` to map raw MCP JSON → our schema.
- Implement `tools/record_from_mcp.py` to read `sample/mcp_shots/*.json` and write `data/shots.jsonl`.
- Fill `features/extract.py`, `rules/diagnostics.yaml`, `content/astro_map.yaml`, `cli/cards.py`, `web/app.py` so that:
  - `make demo` runs end-to-end.
  - `make web` serves `out/cards.md` at `/`.
- Add `--style gptoss` in `cli/cards.py` that calls local **`gpt-oss:20b`** via Ollama while preserving numbers and units.

## Links

- Gaggiuino MCP server directory: https://glama.ai/mcp/servers/@AndrewKlement/gaggiuino-mcp
- Tools used: `getStatus`, `getLatestShotId`, `getShotData(id)`
