# Mock Server Connectivity Test Report

## Purpose
Validate that the Android Test_App can send requests to a self-hosted server endpoint and receive responses successfully over a shared network.

## Test Setup
- Client: Android Test_App installed on phone
- Server: Local mock server running on PC (`FastAPI + Uvicorn`)
- Network: Phone and PC connected via phone tethering/hotspot
- Endpoint tested: `http://10.39.49.6:8000/api/chat/`
- Request type: `multipart/form-data`

## Request Payload Used
1. `user_message` (required)
2. `chat_id` (optional, left empty in this test)
3. `image` (optional, not used in this specific successful text test)

## Result
- Status in app: `Response received`
- Debug log: success recorded
- Sample message sent: `hi`
- Sample response received:
  - `Your message has been received. Echo: hi`

## Observation
Initial timeout occurred when an outdated IP (`172.20.10.2`) was used. After updating to the active PC IP (`10.39.49.6`), connectivity succeeded.

## Conclusion
The Android client-server communication pipeline is functional for text requests. This validates core networking, endpoint compatibility, and response handling. The next test phase should include optional image upload and `chat_id` validation against the actual friend-hosted server.
