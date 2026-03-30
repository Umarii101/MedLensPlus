# Android Test Client - Complete Setup Guide

## Quick Start (5 minutes)

### Step 1: Find Your PC's IP Address
**Windows (Command Prompt):**
```bash
ipconfig
```
Look for **"IPv4 Address"** under your network adapter. Likely values:
- `192.168.1.x` (home WiFi)
- `192.168.0.x` (home WiFi) 
- `10.x.x.x` (phone hotspot)

**Screenshot example:**
```
Ethernet adapter Ethernet:
   IPv4 Address . . . . . . . . . . : 192.168.1.100
```
**Remember this IP - you'll need it in 2 minutes.**

---

### Step 2: Start the Server

**Easy Way (Recommended):**
1. Open `Test_App/start_server.bat` (double-click it)
2. It will show you your IP address and server URL
3. Server will start on port 8000

**Manual Way:**
```bash
cd Test_App
python diagnostic_server.py
```

**Expected output:**
```
======================================
  MedLens Diagnostic Server
======================================
Server IP: 192.168.1.100
Port: 8000

Android App Configuration:
  Base URL: http://192.168.1.100:8000
  Endpoint: api/chat/
======================================
```

**⚠️ Keep this terminal window open while testing!**

---

### Step 3: Build and Install Android App
```bash
# From project root
./gradlew build
./gradlew installDebug  # requires phone connected via USB
```

---

### Step 4: Network Setup (Choose One)

**Option A: USB Hotspot (Most Reliable)**
1. Enable USB Tethering on your phone
2. PC automatically connects to phone's network
3. Phone can reach PC via hotspot IP

**Option B: Shared WiFi**
1. Connect both PC and phone to the same WiFi router
2. Phone can reach PC via WiFi IP (192.168.x.x)
3. May be faster than hotspot

**Option C: Direct USB (Dev Only)**
```bash
# Forward port via ADB
adb forward tcp:8000 tcp:8000
# Then use localhost in app  
```

---

### Step 5: Configure Android App

1. **Open the Test App on your phone**
2. **Enter Server Configuration:**
   
   | Field | Example | Notes |
   |-------|---------|-------|
   | Base URL | `http://192.168.1.100:8000` | Your PC's IP from Step 1 |
   | Endpoint Path | `api/chat/` | Don't change this |
   | Chat ID | (leave empty) | Optional for testing |

3. **Click Send with a message**
4. **Watch the Debug Log panel** - it will show:
   - `→ POST http://192.168.1.100:8000/api/chat/`
   - `Success: responseLength=45`

---

## Troubleshooting

### ❌ "Connection failed" / "timeout"

**Check these in order:**

1. **Is Python server running?**
   - Look at the terminal where you started `diagnostic_server.py`
   - Should see: `Uvicorn running on http://0.0.0.0:8000`

2. **Is the IP correct?**
   - Run `ipconfig` again to double-check
   - Make sure it's not `127.0.0.1` or `localhost`
   - Example: `http://192.168.1.100:8000` ✓

3. **Are they on the same network?**
   - Phone and PC must be on same WiFi/hotspot
   - Can you ping? `ping <IP>` from PC terminal
   - Expected: "Reply from X.X.X.X: bytes=32..."

4. **Firewall blocking?**
   - Windows Defender Firewall → Allow an app
   - Add Python and port 8000
   - Or temporarily disable firewall for testing

5. **Try the ping endpoint:**
   - In browser: `http://192.168.1.100:8000/ping`
   - Should show: `PONG - Server is reachable!`

### ❌ "Connection refused"

Usually means server isn't listening on that port.

```bash
# Check what's listening on port 8000
netstat -an | find "8000"  # Windows

# Kill any process on 8000 and restart
python diagnostic_server.py
```

### ❌ App sees error messages but no server logs

Server isn't actually receiving requests. This means:
- Network route is blocked
- Firewall is dropping packets  
- IP address was typed wrong
- Phone not on same network

**Debug:** Try from browser:
```
http://192.168.1.100:8000/
```
Should show JSON with status and endpoint info.

---

## Testing Checklist

- [ ] Server running (see "Server IP" message)
- [ ] Correct IP in app (matches ipconfig output)  
- [ ] Phone and PC on same network (hotspot or WiFi)
- [ ] Can reach `http://IP:8000/ping` from browser
- [ ] First message shows in debug log with `→ POST`
- [ ] Server terminal shows `REQUEST RECEIVED`
- [ ] Message appears back in app chat

---

## Technical Details

### Request Format

This app sends a multipart POST request with:
- `user_message` (required, text)
- `chat_id` (optional, text)
- `image` (optional, file)

### Response Parsing

Server should respond with JSON:
```json
{
  "response": "Your response text here"
}
```

The app also accepts: `message`, `answer`, `output`, `text` keys, or plain text fallback.

### Server Features

| Endpoint | Purpose |
|----------|---------|
| `GET /` | Show server IP and configuration |
| `GET /ping` | Simple connectivity test |
| `GET /health` | Health check |
| `POST /api/chat/` | Main endpoint (text + optional image) |

---

## Files Included

- `diagnostic_server.py` - Enhanced test server with full request logging
- `mock_server.py` - Simple echo server
- `start_server.bat` - Windows helper (shows IP + starts server)
- `app/` - Android Studio project folder

---

## After It Works

Once you get a successful message:
1. Test with images - try uploading a picture
2. Test chat ID - confirm it echoes back
3. Test error cases - stop server and see error handling
4. Integration - swap `diagnostic_server.py` for your real API

Good luck! 🚀
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
