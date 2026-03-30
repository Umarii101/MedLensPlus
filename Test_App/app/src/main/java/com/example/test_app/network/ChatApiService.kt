package com.example.test_app.network

import okhttp3.MultipartBody
import okhttp3.RequestBody
import okhttp3.ResponseBody
import retrofit2.Response
import retrofit2.http.Multipart
import retrofit2.http.POST
import retrofit2.http.Part
import retrofit2.http.Url

interface ChatApiService {
    @Multipart
    @POST
    suspend fun sendChatMessage(
        @Url fullUrl: String,
        @Part("message") userMessage: RequestBody,
        @Part("chat_id") chatId: RequestBody?,
        @Part file: MultipartBody.Part?
    ): Response<ResponseBody>
}
