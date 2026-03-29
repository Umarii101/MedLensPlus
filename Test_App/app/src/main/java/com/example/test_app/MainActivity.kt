package com.example.test_app

import android.net.Uri
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.viewModels
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.VerticalDivider
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil.compose.AsyncImage
import com.example.test_app.ui.ChatViewModel

class MainActivity : ComponentActivity() {
    private val viewModel: ChatViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()

        setContent {
            MaterialTheme {
                ChatScreen(viewModel)
            }
        }
    }
}

@Composable
private fun ChatScreen(viewModel: ChatViewModel) {
    var pickerTrigger by remember { mutableStateOf(false) }

    val imagePicker = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.GetContent()
    ) { uri: Uri? ->
        viewModel.setSelectedImage(uri)
    }

    if (pickerTrigger) {
        pickerTrigger = false
        imagePicker.launch("image/*")
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(12.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Text(
            text = "MedLens API Test Client",
            fontSize = 20.sp,
            color = MaterialTheme.colorScheme.primary
        )

        ServerConfigPanel(viewModel)

        Text(
            text = "Status: ${viewModel.statusText}",
            fontSize = 13.sp,
            color = Color.Gray
        )

        DebugLogPanel(logs = viewModel.debugLogs)

        LazyColumn(
            modifier = Modifier
                .weight(1f)
                .fillMaxWidth(),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            itemsIndexed(viewModel.messages) { _, message ->
                MessageBubble(
                    text = message.text,
                    imageUri = message.imageUri,
                    fromUser = message.fromUser
                )
            }
        }

        SelectedImagePreview(
            imageUri = viewModel.selectedImageUri,
            onClear = { viewModel.clearImage() }
        )

        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(8.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            OutlinedTextField(
                value = viewModel.inputMessage,
                onValueChange = { viewModel.inputMessage = it },
                modifier = Modifier.weight(1f),
                placeholder = { Text("Type message") }
            )

            Button(onClick = { pickerTrigger = true }) {
                Text("Image")
            }
        }

        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.End,
            verticalAlignment = Alignment.CenterVertically
        ) {
            if (viewModel.isLoading) {
                CircularProgressIndicator(modifier = Modifier.size(20.dp), strokeWidth = 2.dp)
                Spacer(modifier = Modifier.size(8.dp))
            }
            Button(
                onClick = { viewModel.sendMessage() },
                enabled = !viewModel.isLoading
            ) {
                Text("Send")
            }
        }
    }
}

@Composable
private fun DebugLogPanel(logs: List<String>) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .background(Color(0xFFF0F3F7), RoundedCornerShape(10.dp))
            .padding(8.dp),
        verticalArrangement = Arrangement.spacedBy(4.dp)
    ) {
        Text("Debug Logs", fontSize = 13.sp, color = Color(0xFF1D3557))

        if (logs.isEmpty()) {
            Text("No logs yet", fontSize = 12.sp, color = Color.Gray)
            return
        }

        val recentLogs = logs.takeLast(5).reversed()
        recentLogs.forEach { log ->
            Text(
                text = log,
                fontSize = 11.sp,
                color = Color(0xFF3A3A3A),
                modifier = Modifier.fillMaxWidth()
            )
        }
    }
}

@Composable
private fun ServerConfigPanel(viewModel: ChatViewModel) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .background(Color(0xFFF3F5F8), RoundedCornerShape(10.dp))
            .padding(10.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Text("Server Config", color = Color(0xFF204A87), fontSize = 14.sp)

        OutlinedTextField(
            value = viewModel.baseUrl,
            onValueChange = { viewModel.baseUrl = it },
            label = { Text("Base URL") },
            placeholder = { Text("http://192.168.1.100:8000") },
            modifier = Modifier.fillMaxWidth(),
            singleLine = true
        )

        OutlinedTextField(
            value = viewModel.endpointPath,
            onValueChange = { viewModel.endpointPath = it },
            label = { Text("Endpoint Path") },
            placeholder = { Text("chat") },
            modifier = Modifier.fillMaxWidth(),
            singleLine = true
        )

        OutlinedTextField(
            value = viewModel.chatId,
            onValueChange = { viewModel.chatId = it },
            label = { Text("Chat ID (optional)") },
            placeholder = { Text("23") },
            modifier = Modifier.fillMaxWidth(),
            singleLine = true
        )
    }
}

@Composable
private fun MessageBubble(text: String, imageUri: Uri?, fromUser: Boolean) {
    val bg = if (fromUser) Color(0xFFD4EDDA) else Color(0xFFE9ECEF)
    val align = if (fromUser) Alignment.CenterEnd else Alignment.CenterStart

    Box(
        modifier = Modifier.fillMaxWidth(),
        contentAlignment = align
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth(0.85f)
                .background(bg, RoundedCornerShape(12.dp))
                .padding(10.dp)
        ) {
            if (imageUri != null) {
                AsyncImage(
                    model = imageUri,
                    contentDescription = "uploaded image",
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(140.dp),
                    contentScale = ContentScale.Crop
                )
                Spacer(modifier = Modifier.height(6.dp))
            }
            Text(text = text, textAlign = TextAlign.Start)
        }
    }
}

@Composable
private fun SelectedImagePreview(imageUri: Uri?, onClear: () -> Unit) {
    if (imageUri == null) return

    Column(
        modifier = Modifier
            .fillMaxWidth()
            .background(Color(0xFFF9F0D5), RoundedCornerShape(10.dp))
            .padding(8.dp),
        verticalArrangement = Arrangement.spacedBy(6.dp)
    ) {
        Text("Selected image to upload", fontSize = 13.sp)
        AsyncImage(
            model = imageUri,
            contentDescription = "selected image",
            modifier = Modifier
                .fillMaxWidth()
                .height(120.dp),
            contentScale = ContentScale.Crop
        )
        TextButton(onClick = onClear, modifier = Modifier.align(Alignment.End)) {
            Text("Remove")
        }
    }
}
