PY=/opt/homebrew/bin/python3.12
.PHONY: record extract cards web demo check
record: ; $(PY) tools/record_from_mcp.py sample/mcp_shots/*.json -o data/shots.jsonl
extract: data/shots.jsonl ; $(PY) features/extract.py data/shots.jsonl -o data/features.jsonl
cards: data/features.jsonl ; $(PY) cli/cards.py --features data/features.jsonl --rules rules/diagnostics.yaml --astro content/astro_map.yaml --out out/cards.md
web: ; $(PY) web/app.py
demo: record extract cards ; @echo "Demo built -> out/cards.md"
check:
	@grep -R "getShotData" -n data_sources tools >/dev/null || (echo "Missing MCP path (getShotData)"; exit 1)
	@grep -R "OPENAI_BASE_URL" -n cli >/dev/null || (echo "Missing optional gpt-oss hook"; exit 1)
	@echo "Checks passed"
