#!/bin/bash

# Push the rental_lookup_tool.json to Vapi with API key from .env

API_KEY=$(grep vapi_api_key .env | cut -d'=' -f2 | xargs)
TOOL_PATH="DEV_MAN/rental_lookup_tool.json"

if [ -z "$API_KEY" ]; then
  echo "[ERROR] vapi_api_key not found in .env. Aborting."
  exit 1
fi

if [ ! -f "$TOOL_PATH" ]; then
  echo "[ERROR] Tool definition $TOOL_PATH not found. Aborting."
  exit 1
fi

echo "[INFO] Pushing $TOOL_PATH to Vapi..."
vapi tool push $TOOL_PATH --api-key $API_KEY

if [ $? -eq 0 ]; then
  echo "[SUCCESS] Tool pushed successfully. Run 'vapi tool list --api-key $API_KEY' to verify."
else
  echo "[ERROR] Failed to push tool. Check your tool definition and API key."
  exit 1
fi 