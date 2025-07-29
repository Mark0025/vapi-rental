# Vapi Rental Lookup Tool

## Overview

This project enables automated extraction of rental property data from public rental websites using a modern Python stack:

- **FastAPI** backend for secure, API-driven access
- **LangChain** agent for web data extraction and structured output
- **OpenRouter** API for LLM-powered web search and extraction
- **Vapi** integration for voice/chat assistant workflows

## Architecture

- **User/Agent** → **Vapi API Tool** → **FastAPI `/rental-lookup` endpoint** → **LangChain Agent** → **OpenRouter**
- End-to-end flow: User asks for rentals → Vapi agent triggers API tool → FastAPI backend fetches/extracts data → Agent relays results

## Setup

1. **Clone the repo and install dependencies:**
   ```sh
   uv add -r requirements.txt
   uv add langchain_community langchain_openai fastapi uvicorn httpx python-dotenv wikipedia
   ```
2. **Configure environment variables in `.env`:**
   - `VAPI_API_KEY` (your Vapi private key)
   - `OPENROUTER_API_KEY` (your OpenRouter key)
3. **Run the FastAPI proxy:**
   ```sh
   uv run -m uvicorn rental_lookup_proxy:app --host 0.0.0.0 --port 4242 --reload
   ```
4. **Expose your local server with ngrok:**
   ```sh
   ngrok http 4242
   ```
5. **Configure your Vapi API tool:**
   - Method: POST
   - URL: `https://<ngrok-url>/rental-lookup`
   - Body: `{ "website": "<target-rental-site>" }`
   - Header: `Content-Type: application/json`

## Usage

- Use the Vapi dashboard or API to trigger the rental lookup tool.
- The FastAPI backend will extract and return structured rental data as JSON.
- Example curl test:
  ```sh
  curl -X POST https://<ngrok-url>/rental-lookup \
    -H "Content-Type: application/json" \
    -d '{"website": "https://nolenpropertiesllc.managebuilding.com/Resident/public/home"}'
  ```

## Project Files

- `main.py`: LangChain agent and extraction logic
- `tools.py`: Custom tools for the agent
- `rental_lookup_proxy.py`: FastAPI server and endpoint
- `rental_lookup_tool.json`: Vapi tool definition
- `.env`: API keys and config
- `requirements.txt`: Python dependencies

## Best Practices

- Use POST for structured input
- Never expose secrets in tool definitions
- Use ngrok for local dev, update URLs for production
- See `.cursor/rules/vapi-tool-best-practices.mdc` for more

## License

MIT
# vapi-rental
