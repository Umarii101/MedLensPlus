"""
Diagnostic Mock Server - Debug networking issues easily
Logs all requests with full details
"""
from fastapi import FastAPI, Form, File, UploadFile, Request
from fastapi.responses import JSONResponse, PlainTextResponse
import uvicorn
import socket
import json
from datetime import datetime

app = FastAPI(title="MedLens Diagnostic Server")

def get_local_ip():
    """Get the actual IP address this server is listening on"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

@app.get("/")
def root():
    """Simple health check"""
    local_ip = get_local_ip()
    return JSONResponse({
        "status": "Server is running",
        "server_ip": local_ip,
        "port": 8000,
        "url": f"http://{local_ip}:8000",
        "api_endpoint": f"http://{local_ip}:8000/api/chat/",
        "test_ping": f"http://{local_ip}:8000/ping"
    })

@app.get("/ping")
def ping():
    """Simple ping test"""
    return PlainTextResponse("PONG - Server is reachable!")

@app.get("/health")
def health():
    return {"status": "ok", "message": "Server is running"}

@app.post("/api/chat/")
async def chat(
    request: Request,
    message: str = Form(...),
    chat_id: str | None = Form(default=None),
    file: UploadFile | None = File(default=None),
):
    """
    Chat endpoint - echoes back the user message
    """
    timestamp = datetime.now().isoformat()
    client_ip = request.client.host if request.client else "unknown"
    
    print(f"\n{'='*60}")
    print(f"[{timestamp}] REQUEST RECEIVED")
    print(f"{'='*60}")
    print(f"Client IP: {client_ip}")
    print(f"User Message: {message[:200]}")
    print(f"Chat ID: {chat_id}")
    print(f"File Present: {file is not None}")
    
    file_info = None
    if file is not None:
        content = await file.read()
        file_info = {
            "filename": file.filename,
            "content_type": file.content_type,
            "size_bytes": len(content),
        }
        print(f"File Details: {file_info}")

    response_text = message  # Echo back the exact message
    
    response_payload = {
        "status": "success",
        "response": response_text,
        "chat_id": chat_id or "9999",
        "received": {
            "has_file": file is not None,
            "file_info": file_info,
            "timestamp": timestamp,
            "client_ip": client_ip,
        },
    }
    
    print(f"\nResponse: {json.dumps(response_payload, indent=2)}")
    print(f"{'='*60}\n")
    
    return JSONResponse(response_payload)


if __name__ == "__main__":
    local_ip = get_local_ip()
    print("\n" + "="*60)
    print("MEDLENS DIAGNOSTIC SERVER")
    print("="*60)
    print(f"Server IP: {local_ip}")
    print(f"Port: 8000")
    print(f"\nAndroid App Configuration:")
    print(f"  Base URL: http://{local_ip}:8000")
    print(f"  Endpoint: /api/chat/")
    print(f"\nServer running on: http://0.0.0.0:8000")
    print(f"Test endpoint: http://{local_ip}:8000/ping")
    print("="*60 + "\n")
    
    uvicorn.run("diagnostic_server:app", host="0.0.0.0", port=8000, reload=False)
