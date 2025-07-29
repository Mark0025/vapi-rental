# Vapi Rental Lookup Tool Planning

## Objective

Create a simplified Vapi tool that allows users to look up rental properties from a specified website using OpenRouter's API, removing all n8n-specific workflow logic.

## Workflow Overview

1. **Input:** User provides a website URL to look up rental properties.
2. **Process:**
   - Send a POST request to OpenRouter's API with a system prompt restricting data usage to the provided website.
   - Use the model `qwen:Qwen1.5-32B-Chat`.
   - Pass the website as context in the prompt.
3. **Output:** Return the list of available rental properties as provided by the model's response.

## Environment Variables

- `vapi_api_key` (from .env)
- `live_server` (ngrok or local server URL)
- `OPENROUTER_API_KEY` (to be added if not present)

## Implementation Steps

1. Remove n8n-specific nodes and connections from the workflow.
2. Create a Vapi tool definition (JSON or YAML) for the rental lookup.
3. Implement a local endpoint (e.g., `/rental-lookup`) to handle requests.
4. Integrate OpenRouter API call logic.
5. Test locally using the ngrok URL for webhook/callbacks.
6. Document usage and testing steps.

## Next Steps

- [ ] Add `OPENROUTER_API_KEY` to `.env` if missing.
- [ ] Draft Vapi tool definition for rental lookup.
- [ ] Implement and test the endpoint locally.
- [ ] Update this README with results and improvements.
