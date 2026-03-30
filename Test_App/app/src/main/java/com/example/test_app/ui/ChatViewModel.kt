package com.example.test_app.ui

import android.app.Application
import android.net.Uri
import android.util.Log
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.example.test_app.network.ChatRepository
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import kotlinx.coroutines.launch

class ChatViewModel(application: Application) : AndroidViewModel(application) {

    companion object {
        private const val TAG = "ChatViewModel"
        private const val MAX_DEBUG_LOGS = 60
    }

    data class UiMessage(
        val fromUser: Boolean,
        val text: String,
        val imageUri: Uri? = null
    )

    private val repository = ChatRepository(application)

    val messages = mutableStateListOf<UiMessage>()
    val debugLogs = mutableStateListOf<String>()

    var baseUrl by mutableStateOf("http://192.168.1.100:8000")
    var endpointPath by mutableStateOf("api/chat/")
    var chatId by mutableStateOf("")
    var inputMessage by mutableStateOf("")
    var selectedImageUri by mutableStateOf<Uri?>(null)
    var isLoading by mutableStateOf(false)
    var statusText by mutableStateOf("Ready")

    fun setSelectedImage(uri: Uri?) {
        selectedImageUri = uri
        addDebugLog("Image selected: ${uri != null}")
    }

    fun clearImage() {
        selectedImageUri = null
        addDebugLog("Image cleared")
    }

    fun sendMessage() {
        val userText = inputMessage.trim()
        if (userText.isBlank() && selectedImageUri == null) return
        if (isLoading) return

        addDebugLog(
            "→ POST $baseUrl$endpointPath (chatId=${chatId.takeIf { it.isNotBlank() } ?: "none"}, photo=${selectedImageUri != null})"
        )

        messages.add(UiMessage(fromUser = true, text = userText.ifBlank { "[Image only]" }, imageUri = selectedImageUri))

        val imageToSend = selectedImageUri
        inputMessage = ""
        selectedImageUri = null
        isLoading = true
        statusText = "Sending request..."

        viewModelScope.launch(Dispatchers.IO) {
            val result = repository.sendMessage(
                baseUrl = baseUrl,
                endpointPath = endpointPath,
                userMessage = userText.ifBlank { "Please analyze this image." },
                chatId = chatId,
                imageUri = imageToSend
            )

            withContext(Dispatchers.Main) {
                result.onSuccess { responseText ->
                    messages.add(UiMessage(fromUser = false, text = responseText))
                    statusText = "Response received"
                    addDebugLog("Success: responseLength=${responseText.length}")
                    Log.d(TAG, "Request succeeded")
                }.onFailure { throwable ->
                    val errorMsg = when {
                        throwable.message?.contains("connect") == true -> 
                            "Connection failed. Check: 1) Server is running, 2) Correct IP entered, 3) Phone and PC on same network"
                        throwable.message?.contains("timeout") == true -> 
                            "Timeout. Server not responding. Check if running and IP is correct."
                        throwable.message?.contains("refused") == true -> 
                            "Connection refused. Server may not be running on this IP."
                        else -> "Error: ${throwable.message}"
                    }
                    messages.add(UiMessage(fromUser = false, text = errorMsg))
                    statusText = "Connection Error"
                    addDebugLog("Failed: ${throwable::class.simpleName} - ${throwable.message}")
                    Log.e(TAG, "Request failed", throwable)
                }

                isLoading = false
            }
        }
    }

    private fun addDebugLog(message: String) {
        Log.d(TAG, message)
        debugLogs.add("${System.currentTimeMillis()}: $message")
        if (debugLogs.size > MAX_DEBUG_LOGS) {
            debugLogs.removeAt(0)
        }
    }
}
