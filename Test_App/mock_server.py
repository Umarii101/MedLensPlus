from fastapi import FastAPI, Form, File, UploadFile, Request
from fastapi.responses import JSONResponse
import uvicorn
import socket
from datetime import datetime

app = FastAPI(title="MedLens Mock Server")

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
    """Status page"""
    local_ip = get_local_ip()
    return JSONResponse({
        "status": "Server is running",
        "server_ip": local_ip,
        "port": 8000,
        "url": f"http://{local_ip}:8000",
        "api_endpoint": f"http://{local_ip}:8000/api/chat/"
    })

@app.get("/health")
def health():
    return {"status": "ok", "message": "Mock server is running"}

@app.post("/api/chat/")
async def chat(
    request: Request,
    user_message: str = Form(...),
    chat_id: str | None = Form(default=None),
    image: UploadFile | None = File(default=None),
):
    timestamp = datetime.now().isoformat()
    client_ip = request.client.host if request.client else "unknown"
    
    print(f"\n{'='*60}")
    print(f"[{timestamp}] REQUEST FROM {client_ip}")
    print(f"Message: {user_message[:100]}")
    print(f"Chat ID: {chat_id}")
    print(f"Image: {image.filename if image else 'None'}")
    print(f"{'='*60}")
    
    image_info = None
    if image is not None:
        content = await image.read()
        image_info = {
            "filename": image.filename,
            "content_type": image.content_type,
            "size_bytes": len(content),
        }

    response_text = user_message

    return JSONResponse(
        {
            "response": response_text,
            "received": {
                "chat_id": chat_id,
                "has_image": image is not None,
                "image_info": image_info,
            },
        }
    )


if __name__ == "__main__":
    local_ip = get_local_ip()
    print("\n" + "="*60)
    print("MEDLENS MOCK SERVER")
    print("="*60)
    print(f"Server IP: {local_ip}")
    print(f"Port: 8000")
    print(f"Base URL: http://{local_ip}:8000")
    print(f"Endpoint: /api/chat/")
    print("="*60 + "\n")
    
    uvicorn.run("mock_server:app", host="0.0.0.0", port=8000, reload=False)
