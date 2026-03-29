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

    suspend fun sendMessage(
        baseUrl: String,
        endpointPath: String,
        userMessage: String,
        chatId: String?,
        imageUri: Uri?
    ): Result<String> {
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
                image = imagePart
            )

            val responseBody = response.body()?.string().orEmpty()
            if (response.isSuccessful) {
                val parsed = extractTextResponse(responseBody)
                Log.d(
                    TAG,
                    "Request success code=${response.code()} rawLength=${responseBody.length} parsedLength=${parsed.length}"
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
        return MultipartBody.Part.createFormData("image", tempFile.name, requestBody)
    }

    private fun extractTextResponse(raw: String): String {
        if (raw.isBlank()) return "(Empty response from server)"

        return try {
            val element = JsonParser.parseString(raw)
            if (!element.isJsonObject) return raw
            val obj = element.asJsonObject

            val keys = listOf("response", "message", "answer", "output", "text")
            for (key in keys) {
                if (obj.has(key) && !obj.get(key).isJsonNull) {
                    return obj.get(key).asString
                }
            }

            if (obj.has("data") && obj.get("data").isJsonObject) {
                val dataObj = obj.getAsJsonObject("data")
                for (key in keys) {
                    if (dataObj.has(key) && !dataObj.get(key).isJsonNull) {
                        return dataObj.get(key).asString
                    }
                }
            }

            raw
        } catch (_: Exception) {
            raw
        }
    }
}
