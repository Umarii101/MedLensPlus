package com.example.test_app.network

import okhttp3.Interceptor
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.util.concurrent.TimeUnit

object NetworkProvider {
    private val loggingInterceptor = HttpLoggingInterceptor().apply {
        level = HttpLoggingInterceptor.Level.BODY
    }

    // Interceptor to bypass anti-phishing interstitial pages on Dev Tunnels, Ngrok, etc.
    private val tunnelBypassInterceptor = Interceptor { chain ->
        val original = chain.request()
        val request = original.newBuilder()
            .header("User-Agent", "MedLens-Test-Client") // Bypasses browser-gate pages
            .header("Bypass-Tunnel-Reminder", "true") // LocalTunnel bypass
            .header("ngrok-skip-browser-warning", "true") // Ngrok bypass
            .header("X-Tunnel-Skip-AntiPhishing-Page", "true") // Microsoft Dev Tunnels bypass
            .method(original.method, original.body)
            .build()
        chain.proceed(request)
    }

    private val okHttpClient = OkHttpClient.Builder()
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(60, TimeUnit.SECONDS)
        .writeTimeout(60, TimeUnit.SECONDS)
        .addInterceptor(tunnelBypassInterceptor)
        .addInterceptor(loggingInterceptor)
        .build()

    private val retrofit = Retrofit.Builder()
        .baseUrl("http://localhost/")
        .addConverterFactory(GsonConverterFactory.create())
        .client(okHttpClient)
        .build()

    val chatApiService: ChatApiService = retrofit.create(ChatApiService::class.java)
}
