# Test_App (Android API Chat Tester)

A small Android app to test POST requests to your self-hosted LLM endpoint.

## Request Payload

This app sends a multipart POST request with:

1. `user_message` (required)
2. `chat_id` (optional)
3. `image` (optional file upload)

## UI Features

1. Chat interface with user and assistant bubbles
2. Optional image picker and preview
3. Configurable server URL and endpoint path
4. Displays raw/parsed response text from API

## Default Config in App

- Base URL: `http://172.20.10.2:8000`
- Endpoint path: `api/chat/`

Change these in the app to match your friend's laptop server.

## Expected Server Behavior

For best compatibility, the server should accept `multipart/form-data` with fields:

- `user_message` as string
- `chat_id` as optional string
- `image` as optional file

Recommended response format:

```json
{
  "response": "Your model output here"
}
```

The app also tries `message`, `answer`, `output`, and `text` keys, or falls back to plain text.

## Android Studio Build Steps

1. Open Android Studio.
2. Click Open and select the `Test_App` folder.
3. Wait for Gradle sync to finish.
4. Open `MainActivity` and confirm no red errors.
5. Connect your Android device (same LAN as server laptop).
6. Make sure server is reachable from phone using browser or curl-style app.
7. Click Run and choose your device.

## First Test Checklist

1. App base URL is your friend's LAN IP, not localhost.
2. Port is open in Windows Firewall on server laptop.
3. Server binds to `0.0.0.0`, not `127.0.0.1`.
4. Endpoint path in app matches server route exactly.
5. Send text-only message first, then test with image.

## Common Issues

- `CLEARTEXT communication not permitted`: already handled with `usesCleartextTraffic=true`.
- Timeout: verify IP/port/firewall and Wi-Fi network.
- HTTP 404: endpoint path mismatch.
- HTTP 415/422: server expects JSON instead of multipart. Update server parser or app contract.

## Local Simulation Test (No APK Changes)

You can test now by using this PC as a mock server and your phone app as client.

### Files added for simulation

- [mock_server.py](mock_server.py)
- [mock_server_requirements.txt](mock_server_requirements.txt)
- [run_mock_server.ps1](run_mock_server.ps1)

### What this mock server does

1. Accepts `POST /api/chat/` with multipart form fields:
   - `user_message` (required)
   - `chat_id` (optional)
   - `image` (optional)
2. Returns JSON like:

```json
{
  "response": "Your message has been received. Echo: ...",
  "received": {
    "chat_id": "23",
    "has_image": true,
    "image_info": {
      "filename": "photo.jpg",
      "content_type": "image/jpeg",
      "size_bytes": 12345
    }
  }
}
```

### Run the mock server

From PowerShell in this folder:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\run_mock_server.ps1
```

Or manually:

```powershell
py -m pip install -r .\mock_server_requirements.txt
py .\mock_server.py
```

### Hotspot test plan

1. Turn on mobile hotspot on your phone.
2. Connect this PC to that hotspot.
3. Find this PC local IP (for example `172.20.10.2`) using `ipconfig`.
4. In app settings use:
   - Base URL: `http://<PC_IP>:8000`
   - Endpoint path: `api/chat/`
5. Keep the mock server running and send test messages from app.

### Firewall note

If app cannot connect, allow inbound TCP port 8000 in Windows Defender Firewall.
