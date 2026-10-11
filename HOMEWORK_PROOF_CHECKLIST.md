# Homework Proof Checklist

## Verified Setup (2026-10-11)

- [x] `hermes-small` created from the 2.5 GB `qwen3:4b-instruct` fallback; tool capability confirmed.
- [x] Ollama returned an actual `get_weather(location: Vienna)` tool call.
- [x] ChromaDB returned Vienna as the top match.
- [x] Hermes returned the exact requested local sentence and successfully executed `ls -1`.
- [x] Gateway restarted cleanly with `SSLKEYLOGFILE` cleared and Telegram polling connected.
- [x] User sent `/new`, then `Hello Hermes`, and confirmed a successful bot reply; logs confirmed `hermes-small` handled the turn.
- [x] No tool-support, thinking-support, or dependency error occurred on the successful Telegram turn.
- [ ] Capture and attach the proof screenshots below before submitting.

## SSLKEYLOGFILE

- Show that `SSLKEYLOGFILE` was not stored in User or Machine environment variables.
- Show Python HTTPS test returning status `200` for `https://pypi.org`.

## Ollama

- Screenshot or paste `ollama --version`.
- Screenshot or paste `ollama list` showing `qwen3:4b-instruct` and `hermes-small`.
- Screenshot or paste local API output from `http://localhost:11434/api/tags`.
- Screenshot or paste `ollama show hermes-small` showing `tools` capability and `num_ctx 64000` (the minimum accepted by this Hermes version).
- Screenshot or paste `powershell -NoProfile -ExecutionPolicy Bypass -File .\test_ollama_tools.ps1` showing a `get_weather` tool call.

## ChromaDB

- Screenshot or paste `.venv\Scripts\python.exe chromadb_tutorial.py`.
- Confirm the top result is the Austria/Vienna document.

## Hermes

- Screenshot or paste `Get-Command hermes`.
- Screenshot or paste `hermes --version`.
- Screenshot or paste `hermes --help`.
- Screenshot the one-shot local reply: `Hermes small local model works.`
- Screenshot a Hermes directory-listing request showing the terminal tool executed successfully.
- Confirm the provider is `custom`, the endpoint is `http://localhost:11434/v1`, the model is `hermes-small`, and context is `64000`.

## Telegram

- Run `hermes gateway status` and confirm it is running.
- Send `/new`, then `Hello Hermes` to the configured bot.
- If needed, switch with `/model hermes-small --provider custom`, then reset and test again.
- Screenshot the actual successful bot reply, including the test message. Adapter connection alone is not reply proof.
- Redact the bot token anywhere it appears.
- Do not include private Telegram user IDs unless your instructor specifically requires them.

## Short Notes to Include

- Ollama: `hermes-small` uses the small `qwen3:4b-instruct` base model (approximately 2.5 GB); no model larger than 5 GB is needed.
- Model choice: `llama3.2:3b` was tried first and accepted tools, but its Hermes text-reply tests were unreliable, so the requested Qwen fallback was used.
- Context: the direct API tool test passed at 8192 tokens, but Hermes refused that window and required 64000 tokens for agent sessions.
- ChromaDB: three documents were added and Vienna was returned as the top result.
- Hermes: the original plain Llama 3 model accepted chat but lacked tools; the replacement successfully executed a terminal directory listing.
- Setup: clearing the bad `SSLKEYLOGFILE` process variable restored Python HTTPS.
- Telegram: a fresh message received a successful model reply after the session reset; capture that exchange.

