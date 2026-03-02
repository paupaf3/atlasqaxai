#!/usr/bin/env bash
set -eu
set -o pipefail

# Start the Ollama server in the background
ollama serve >/tmp/ollama.log 2>&1 &
pid=$!

# Ensure we forward signals to the server
trap 'kill -TERM "$pid" 2>/dev/null || true' SIGINT SIGTERM

# Wait until the server is ready
until ollama list >/dev/null 2>&1; do
  echo "Waiting for Ollama to be ready..."
  sleep 1
done

echo "🔴 Pulling llama3.1:8b ..."
ollama list | grep -q '^llama3\.1:8b' || ollama pull llama3.1:8b
echo "🟢 Done!"

# echo "🔴 Pulling nomic-embed-text ..."
# ollama list | grep -q '^nomic-embed-text' || ollama pull nomic-embed-text
# echo "🟢 Done!"

echo "🔴 Pulling bge-m3 ..."
ollama list | grep -q '^bge-m3' || ollama pull bge-m3
echo "🟢 Done!"

# Keep the server in the foreground of the container
wait "$pid"