# AtlasQAX.ai - Makefile
# Minimal targets: install, start, stop (+ a couple of helpers).

MODULE   := atlasqaxai
RUN      := pipenv run python -m $(MODULE)
APP_PID  := .atlasqaxai.pid
APP_LOG  := .atlasqaxai.log

.DEFAULT_GOAL := help

.PHONY: help install start stop cli ingest status

help: ## Show this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage: make <target>\n\nTargets:\n"} \
	     /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

install: ## Install dependencies with pipenv
	pipenv install

start: ## Start Ollama (docker) and the Streamlit app
	docker compose up -d
	@echo "Waiting for Ollama to be ready..."
	@until docker exec ollama ollama list >/dev/null 2>&1; do sleep 1; done
	@if [ -f $(APP_PID) ] && kill -0 `cat $(APP_PID)` 2>/dev/null; then \
	    echo "App already running (pid `cat $(APP_PID)`)"; \
	else \
	    nohup $(RUN) app > $(APP_LOG) 2>&1 & echo $$! > $(APP_PID); \
	    echo "App started (pid `cat $(APP_PID)`) — logs: $(APP_LOG)"; \
	    echo "Open http://localhost:8501"; \
	fi

stop: ## Stop the Streamlit app and Ollama
	@if [ -f $(APP_PID) ]; then \
	    kill `cat $(APP_PID)` 2>/dev/null || true; \
	    rm -f $(APP_PID); \
	    echo "App stopped"; \
	else \
	    echo "App not running"; \
	fi
	docker compose down

cli: ## Run the interactive CLI (Ctrl+C to exit)
	$(RUN)

ingest: ## Index documents from data/files
	$(RUN) ingest

status: ## Show app and Ollama status
	@if [ -f $(APP_PID) ] && kill -0 `cat $(APP_PID)` 2>/dev/null; then \
	    echo "App: running (pid `cat $(APP_PID)`)"; \
	else \
	    echo "App: stopped"; \
	fi
	@docker compose ps 2>/dev/null || true
