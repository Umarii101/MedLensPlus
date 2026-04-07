from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from datetime import datetime
import logging
import base64

from .models import Chat
from .utils import llm_call

logger = logging.getLogger(__name__)


class ChatAPIView(APIView):

    def post(self, request):
        try:
            message_text = request.data.get("message", "").strip()
            chat_id = request.data.get("chat_id")
            file = request.FILES.get("file")

            print(message_text)
            # =====================================
            # 1. CHAT FETCH / CREATE
            # =====================================
            if chat_id:
                try:
                    chat = Chat.objects.get(id=int(chat_id))
                except (ValueError, Chat.DoesNotExist):
                    return Response({
                        "status": "error",
                        "details": "Invalid chat_id"
                    }, status=400)
            else:
                chat = Chat.objects.create(details=[])

            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # =====================================
            # 2. FILE HANDLING (READ ONCE)
            # =====================================
            file_url = None
            message_type = "text"
            base64_image = None

            if file:
                message_type = "file"

                try:
                    # ✅ read once
                    file_bytes = file.read()

                    # ✅ save file
                    file_path = default_storage.save(
                        f"uploads/{file.name}",
                        ContentFile(file_bytes)
                    )
                    file_url = default_storage.url(file_path)

                    # ✅ encode for LLM
                    base64_image = base64.b64encode(file_bytes).decode("utf-8")

                except Exception as file_error:
                    logger.exception("File handling failed")
                    return Response({
                        "status": "error",
                        "details": "File processing failed",
                        "error": str(file_error)
                    }, status=500)

            # =====================================
            # 3. BUILD HISTORY (STATEFUL MEMORY)
            # =====================================
            history = []

            for msg in chat.details:
                role = "user" if msg.get("sender_type") == "User" else "assistant"

                # ✅ IMAGE MEMORY (use stored description)
                if msg.get("message_type") == "file":
                    description = msg.get("image_description")

                    if description:
                        history.append({
                            "role": role,
                            "content": f"[Previously uploaded image]: {description}"
                        })
                    continue

                # ✅ NORMAL TEXT
                history.append({
                    "role": role,
                    "content": msg.get("message", "")
                })

            # =====================================
            # 4. CURRENT MESSAGE (MULTIMODAL)
            # =====================================
            if base64_image:
                history.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": message_text or "What is in this image?"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{file.content_type};base64,{base64_image}"
                            }
                        }
                    ]
                })
            else:
                history.append({
                    "role": "user",
                    "content": message_text
                })

            # optional: limit history size
            history = history[-6:]

            # =====================================
            # 5. LLM CALL
            # =====================================
            try:
                bot_response = llm_call(history)
            except Exception as llm_error:
                logger.exception("LLM call failed")
                return Response({
                    "status": "error",
                    "details": "LLM processing failed",
                    "error": str(llm_error)
                }, status=500)

            # =====================================
            # 6. IMAGE MEMORY EXTRACTION
            # =====================================
            image_description = None
            if message_type == "file":
                image_description = f"{bot_response}"

            # =====================================
            # 7. SAVE USER MESSAGE
            # =====================================
            chat.details.append({
                "sender_type": "User",
                "message_type": message_type,
                "message": message_text,
                "file_url": file_url,
                "image_description": image_description,  # ✅ NEW
                "timestamp_at": current_time
            })

            # =====================================
            # 8. SAVE Model RESPONSE
            # =====================================
            chat.details.append({
                "sender_type": "Bot",
                "message_type": "text",
                "message": bot_response,
                "file_url": None,
                "timestamp_at": current_time
            })

            chat.save()

            return Response({
                "status": "success",
                "chat_id": chat.id,
                "user_message": message_text,
                "response": bot_response
            }, status=200)

        except Exception as e:
            logger.exception("Unexpected error in ChatAPIView")

            return Response({
                "status": "error",
                "details": "Internal server error",
                "error": str(e)
            }, status=500)