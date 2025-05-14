.PHONY: zip zip-list clean-last

VENV_BIN=.venv/bin
PYTHON=$(shell \
	if [ -x "$(VENV_BIN)/python" ]; then \
		echo "$(VENV_BIN)/python"; \
	elif command -v python3 > /dev/null; then \
		echo "python3"; \
	elif command -v python > /dev/null; then \
		echo "python"; \
	else \
		echo ""; \
	fi)

LAST_ZIP=$(shell cat .last_zipignore 2>/dev/null || echo "no_zip_found")

zip:
	clear
ifeq ($(PYTHON),)
	@echo "❌ Python not found"
	@exit 1
else
	@echo "🐍 Using Python: $(PYTHON)"
	@$(PYTHON) zipignore.py
endif

zip-list:
	clear
	@echo "📦 Contents of: $(LAST_ZIP)"
	@unzip -l $(LAST_ZIP)

clean-last:
	@if [ -f .last_zipignore ]; then \
		rm -f "$$(cat .last_zipignore)"; \
		rm -f .last_zipignore; \
		echo "🧹 Last zip removed."; \
	else \
		echo "ℹ️  No last zip found."; \
	fi


test:
	clear
	uv run pytest -v --capture=tee-sys --cov=. --cov-report=term-missing tests/