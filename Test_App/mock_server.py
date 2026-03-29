from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI(title="MedLens Mock Server")


@app.get("/health")
def health():
    return {"status": "ok", "message": "Mock server is running"}


@app.post("/api/chat/")
async def chat(
    user_message: str = Form(...),
    chat_id: str | None = Form(default=None),
    image: UploadFile | None = File(default=None),
):
    image_info = None
    if image is not None:
        content = await image.read()
        image_info = {
            "filename": image.filename,
            "content_type": image.content_type,
            "size_bytes": len(content),
        }

    response_text = (
        "Your message has been received. "
        f"Echo: {user_message[:200]}"
    )

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
    uvicorn.run("mock_server:app", host="0.0.0.0", port=8000, reload=False)
