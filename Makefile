PY=/opt/homebrew/bin/python3.12
.PHONY: record extract cards web demo check export_images
record: ; $(PY) tools/record_from_mcp.py sample/mcp_shots/*.json -o data/shots.jsonl
extract: data/shots.jsonl ; $(PY) features/extract.py data/shots.jsonl -o data/features.jsonl
cards: data/features.jsonl ; $(PY) cli/cards.py --features data/features.jsonl --rules rules/diagnostics.yaml --astro content/astro_map.yaml --out out/cards.md
web: ; $(PY) web/app.py
demo: record extract cards ; @echo "Demo built -> out/cards.md"
demo_user:
	@if [ -z "$(MMDD)" ]; then echo "❌ Please specify MMDD: MMDD=0802 make demo_user"; exit 1; fi
	@echo "🎯 Creating demo deck for birth date $(MMDD)..."
	$(PY) tools/make_demo_deck.py --mmdd $(MMDD) --k 3
	@echo "🎉 Demo deck created -> out/cards.md"
export_images:
	@echo "Checking FastAPI server on 127.0.0.1:8000..."
	@curl -s http://127.0.0.1:8000/cards.json >/dev/null || (echo "❌ FastAPI server not running on 127.0.0.1:8000. Start with: make web"; exit 1)
	@echo "✅ FastAPI server is running"
	@echo "📸 Exporting card images..."
	@npm -C webui run export:images
	@echo "🎉 Images exported to webui/share/"
check:
	@grep -R "getShotData" -n data_sources tools >/dev/null || (echo "Missing MCP path (getShotData)"; exit 1)
	@grep -R "OPENAI_BASE_URL" -n cli >/dev/null || (echo "Missing optional gpt-oss hook"; exit 1)
	@echo "Checks passed"
