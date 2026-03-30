from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from datetime import datetime
import logging

from .models import Chat
from .utils import llm_call

logger = logging.getLogger(__name__)


class ChatAPIView(APIView):

    def post(self, request):
        try:
            message_text = request.data.get("message", "").strip()
            chat_id = request.data.get("chat_id")
            file = request.FILES.get("file")


            # 1. CHAT FETCH / CREATE

            chat = None
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


            # 2. FILE HANDLING (STANDARDIZED)

            file_url = None
            message_type = "text"

            if file:
                message_type = "file"

                try:
                    file_path = default_storage.save(
                        f"uploads/{file.name}",
                        ContentFile(file.read())
                    )
                    file_url = default_storage.url(file_path)

                except Exception as file_error:
                    logger.exception("File upload failed")
                    return Response({
                        "status": "error",
                        "details": "File upload failed",
                        "error": str(file_error)
                    }, status=500)


            # 3. BUILD LLM HISTORY

            history = []

            for msg in chat.details:
                role = "user" if msg.get("sender_type") == "User" else "assistant"

                if msg.get("message_type") == "file":
                    content = f"[File: {msg.get('file_url')}]"
                else:
                    content = msg.get("message", "")

                history.append({
                    "role": role,
                    "content": content
                })

            # current message
            if message_text:
                history.append({
                    "role": "user",
                    "content": message_text
                })

            if file_url:
                history.append({
                    "role": "user",
                    "content": f"[User uploaded file: {file_url}]"
                })

            # 4. LLM CALL
            try:
                bot_response = llm_call(history)
            except Exception as llm_error:
                logger.exception("LLM call failed")
                return Response({
                    "status": "error",
                    "details": "LLM processing failed",
                    "error": str(llm_error)
                }, status=500)

            # 5. SAVE USER MESSAGE
            chat.details.append({
                "sender_type": "User",
                "message_type": message_type,
                "message": message_text,
                "file_url": file_url,
                "timestamp_at": current_time
            })


            # 6. SAVE BOT RESPONSE

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