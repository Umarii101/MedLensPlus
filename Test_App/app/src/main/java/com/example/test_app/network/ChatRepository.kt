package com.example.test_app.network

import android.content.Context
import android.net.Uri
import android.util.Log
import android.webkit.MimeTypeMap
import com.google.gson.JsonParser
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.RequestBody
import okhttp3.RequestBody.Companion.asRequestBody
import okhttp3.RequestBody.Companion.toRequestBody
import java.io.File

class ChatRepository(
    private val context: Context,
    private val api: ChatApiService = NetworkProvider.chatApiService
) {
    companion object {
        private const val TAG = "ChatRepository"
    }

    data class ChatResult(val message: String, val chatId: String?)

    suspend fun sendMessage(
        baseUrl: String,
        endpointPath: String,
        userMessage: String,
        chatId: String?,
        imageUri: Uri?
    ): Result<ChatResult> {
        return try {
            val fullUrl = buildUrl(baseUrl, endpointPath)
            Log.d(
                TAG,
                "Preparing request url=$fullUrl, messageLength=${userMessage.length}, chatIdPresent=${!chatId.isNullOrBlank()}, imagePresent=${imageUri != null}"
            )

            val userBody = userMessage.toRequestBody("text/plain".toMediaTypeOrNull())
            val chatIdBody = chatId
                ?.takeIf { it.isNotBlank() }
                ?.toRequestBody("text/plain".toMediaTypeOrNull())

            val imagePart = imageUri?.let { createImagePart(it) }

            val response = api.sendChatMessage(
                fullUrl = fullUrl,
                userMessage = userBody,
                chatId = chatIdBody,
                file = imagePart
            )

            val responseBody = response.body()?.string().orEmpty()
            if (response.isSuccessful) {
                val parsed = extractTextResponse(responseBody)
                Log.d(
                    TAG,
                    "Request success code=${response.code()} rawLength=${responseBody.length} parsedLength=${parsed.message.length}"
                )
                Result.success(parsed)
            } else {
                val errorBody = response.errorBody()?.string().orEmpty()
                Log.e(
                    TAG,
                    "Request failed code=${response.code()} errorBody=$errorBody"
                )
                Result.failure(
                    IllegalStateException(
                        "HTTP ${response.code()}: $errorBody"
                    )
                )
            }
        } catch (e: Exception) {
            Log.e(TAG, "Request exception: ${e.message}", e)
            Result.failure(e)
        }
    }

    private fun buildUrl(baseUrl: String, endpointPath: String): String {
        val normalizedBase = if (baseUrl.endsWith("/")) baseUrl else "$baseUrl/"
        val normalizedPath = endpointPath.trimStart('/')
        return normalizedBase + normalizedPath
    }

    private fun createImagePart(uri: Uri): MultipartBody.Part {
        val resolver = context.contentResolver
        val mimeType = resolver.getType(uri) ?: "image/jpeg"
        val extension = MimeTypeMap.getSingleton().getExtensionFromMimeType(mimeType) ?: "jpg"
        val tempFile = File.createTempFile("upload_", ".$extension", context.cacheDir)

        resolver.openInputStream(uri).use { input ->
            requireNotNull(input) { "Unable to open image URI" }
            tempFile.outputStream().use { output -> input.copyTo(output) }
        }

        Log.d(
            TAG,
            "Prepared image upload mime=$mimeType sizeBytes=${tempFile.length()} file=${tempFile.name}"
        )

        val requestBody: RequestBody = tempFile.asRequestBody(mimeType.toMediaTypeOrNull())
        return MultipartBody.Part.createFormData("file", tempFile.name, requestBody)
    }

    private fun extractTextResponse(raw: String): ChatResult {
        if (raw.isBlank()) return ChatResult("(Empty response from server)", null)

        return try {
            val element = JsonParser.parseString(raw)
            if (!element.isJsonObject) return ChatResult(raw, null)
            val obj = element.asJsonObject

            var parsedChatId: String? = null
            if (obj.has("chat_id") && !obj.get("chat_id").isJsonNull) {
                parsedChatId = obj.get("chat_id").asString
            }

            val keys = listOf("response", "message", "answer", "output", "text")
            for (key in keys) {
                if (obj.has(key) && !obj.get(key).isJsonNull) {
                    return ChatResult(obj.get(key).asString, parsedChatId)
                }
            }

            if (obj.has("data") && obj.get("data").isJsonObject) {
                val dataObj = obj.getAsJsonObject("data")
                if (dataObj.has("chat_id") && !dataObj.get("chat_id").isJsonNull) {
                    parsedChatId = dataObj.get("chat_id").asString
                }
                for (key in keys) {
                    if (dataObj.has(key) && !dataObj.get(key).isJsonNull) {
                        return ChatResult(dataObj.get(key).asString, parsedChatId)
                    }
                }
            }

            ChatResult(raw, parsedChatId)
        } catch (_: Exception) {
            ChatResult(raw, null)
        }
    }
}
