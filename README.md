# TelegramBot

Homework setup for local Ollama, ChromaDB, Hermes Agent, and a Telegram gateway.

## Verified Results (2026-10-11)

- Ollama 0.35.0: `hermes-small` uses the approximately 2.5 GB `qwen3:4b-instruct` fallback and reports tool capability.
- Direct Ollama API: returned `get_weather` with `location: Vienna`.
- ChromaDB: the Austria/Vienna document was the top result.
- Python HTTPS: returned HTTP 200 after clearing `SSLKEYLOGFILE`.
- Hermes v0.21.6: returned exactly `Hermes small local model works.` and successfully executed `ls -1` through the terminal tool.
- Saved reasoning override: a local `Hello Hermes` request also succeeded using the Telegram toolset without a CLI reasoning override.
- Telegram: the restarted gateway connected; after `/new`, `Hello Hermes` received a successful model reply. The user confirmed receipt, and gateway/agent logs confirmed the turn used `hermes-small`.
- No model larger than 5 GB was downloaded. No credentials were added to the repository.

## Homework Scope

- Verify Ollama is installed and serving a local model.
- Use the small, tool-capable `hermes-small` model made from `Modelfile.hermes-small`.
- Create and query a ChromaDB collection from Python.
- Configure Hermes Agent to use local Ollama through `http://localhost:11434/v1`.
- Run the configured Telegram gateway without committing secrets.

## Ollama Verification

Use PowerShell:

```powershell
ollama --version
ollama list
Invoke-RestMethod http://localhost:11434/api/tags
ollama show hermes-small
ollama run hermes-small
```

If `ollama` is not on PATH in an existing terminal, either open a new PowerShell window or run:

```powershell
& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" --version
& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" list
```

The base model is the requested fallback `qwen3:4b-instruct`, listed as approximately 2.5 GB with tool support by [Ollama](https://ollama.com/library/qwen3:4b-instruct). The preferred `llama3.2:3b` (2.0 GB) was tried first: its direct tool test passed, but it repeatedly used inappropriate tool calls instead of returning the requested text in Hermes. The custom model reuses the base model's downloaded weights.

An 8192-token context passed the initial direct Ollama tool test, but installed Hermes v0.21.6 refuses Ollama agent sessions below 64000 tokens. `Modelfile.hermes-small` therefore uses the minimum required 64000-token context; this does not download a larger model, but increases runtime memory use.

```powershell
ollama pull qwen3:4b-instruct
ollama create hermes-small -f .\Modelfile.hermes-small
ollama stop hermes-small
ollama show hermes-small
powershell -NoProfile -ExecutionPolicy Bypass -File .\test_ollama_tools.ps1
```

The API test supplies a fake `get_weather(location)` function. It passes only when Ollama returns an actual `get_weather` tool call; it does not fetch real weather. It uses the model's configured context instead of overriding it. No model larger than 5 GB is required. The original `Modelfile` and `hermes-local` model are retained as earlier work, but are not used by the gateway.

## ChromaDB Instructions

Create and activate the local virtual environment:

```powershell
& "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe" -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install chromadb
.\.venv\Scripts\python.exe .\chromadb_tutorial.py
```

The script creates an in-memory collection named `homework_collection`, adds three short capital-city documents, and queries the top two matches for:

```text
What is the capital of Austria?
```

## Hermes Local Ollama Setup Summary

Official Hermes Windows install:

```powershell
iex (irm https://hermes-agent.nousresearch.com/install.ps1)
```

Then open a new PowerShell window and verify:

```powershell
Get-Command hermes
hermes --version
hermes --help
```

Configure the model using the Hermes setup/model command shown by your installed help:

```powershell
hermes model
```

Use these values, or set them directly with `hermes config set`:

- Provider: custom endpoint
- Base URL: `http://localhost:11434/v1`
- Model: `hermes-small`
- API key: `ollama` as a harmless local placeholder if Hermes requires one
- Context length: `64000` (required by this installed Hermes version)

```powershell
hermes config set model.default hermes-small
hermes config set model.provider custom
hermes config set model.base_url http://localhost:11434/v1
hermes config set model.api_key ollama
hermes config set model.context_length 64000
hermes config set model.ollama_num_ctx 64000
hermes config set agent.reasoning_overrides '{hermes-small: none, hermes-small:latest: none}'
```

Then test:

```powershell
hermes chat -q "Reply with exactly: Hermes small local model works." --oneshot --provider custom -m hermes-small --reasoning none -t terminal --max-turns 2 --run-budget 120
hermes chat -q "List the files in the current directory. Call the terminal tool once with the read-only command ls -1, then show its output. Do not modify files." --oneshot --provider custom -m hermes-small --reasoning none -t terminal --max-turns 3 --run-budget 120
```

Verified command syntax on this install:

```powershell
hermes setup gateway
hermes gateway setup
hermes gateway run
```

The per-model reasoning override disables reasoning for both spellings of `hermes-small`. It uses a setting supported by this installation; the one-shot tests also use the documented `--reasoning none` option. The terminal-only tests keep the proof focused and do not disable tool calling.

## Telegram Setup Summary

The bot credentials and Windows gateway startup entry are already configured locally. Follow [TELEGRAM_SETUP.md](TELEGRAM_SETUP.md) for initial setup on another machine. Restart this installation with:

```powershell
hermes gateway stop
Remove-Item Env:SSLKEYLOGFILE -ErrorAction SilentlyContinue
hermes gateway start
hermes gateway status
```

In the bot conversation, send `/new`, then `Hello Hermes`. If `/model` still reports the old model, send `/model hermes-small --provider custom`, then `/new` and `Hello Hermes` again. A connected adapter alone does not prove a model reply: capture the actual bot response.

## Issues Encountered

1. `SSLKEYLOGFILE` pointed to an invalid Windows volume path and blocked Python HTTPS/setup. Clearing it in the launching process restored HTTPS; no persistent User or Machine value was found during setup.
2. The original `hermes-local` model used plain Llama 3 and supported chat but not the tool-calling interface required by Hermes Gateway. Llama 3.2 was tried first but did not follow Hermes' simple text-reply instructions reliably, so the replacement uses the approximately 2.5 GB Qwen fallback.
3. The requested 8192-token context works in Ollama, but installed Hermes refuses to start below 64000 tokens. The final configuration uses Hermes' minimum required context instead of changing or bypassing Hermes code.

Hermes was initially configured with a plain Llama 3 model, which supported chat but not the tool-calling interface required by Hermes Gateway. I replaced it with a smaller tool-capable Ollama model and verified local Hermes and Telegram operation.

## Suggested Short Writeups

Ollama:
"I ran Ollama locally with hermes-small, based on the approximately 2.5 GB qwen3:4b-instruct model, and tested its tool-calling API. The original Llama 3 model lacked tool support, and the first Llama 3.2 attempt did not reliably follow Hermes' reply instructions."

ChromaDB:
"I created a ChromaDB collection, added three documents, and successfully queried the top two matching results. The main issue was ensuring the Python environment had the correct package installed."

Hermes:
"I configured Hermes to use hermes-small through the local Ollama endpoint with reasoning disabled. SSLKEYLOGFILE blocked the initial installer, the original model lacked tools, and this Hermes version required a 64000-token context."

Telegram:
"I restarted Hermes Gateway, reset the Telegram session with /new, and received a reply to Hello Hermes. Replacing the original model resolved the tool-support error."

## What to Submit

For each tutorial:

- one short note explaining what I ran
- one screenshot or terminal paste
- one sentence about what broke or almost broke

For Telegram:

- screenshot of the bot reply
- token redacted
