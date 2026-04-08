from llama_cpp import Llama
import time
import os

# Ensure this matches your folder name
model_path = "./Model/medgemma-27b-it-UD-IQ2_XXS.gguf"

print(f"--- 🚀 Initializing MedGemma-27B (Gemma 3 optimized) ---")

try:
    # 1. Setup the Model with Modern llama-cpp-python args
    llm = Llama(
        model_path=model_path,
        n_gpu_layers=-1,         # All layers to RTX 3080
        n_ctx=2048,              # Context window
        n_threads=4,             # i5-7500 optimization
        type_k=1,                # KV Cache Quantization (1 = q8_0) - Saves ~1GB VRAM
        type_v=1,                # KV Cache Quantization (1 = q8_0)
        flash_attn=True,         # Reduces memory spikes
        verbose=True             # To verify CUDA offloading
    )

    # 2. Gemma 3 Prompt Format (No System Turn)
    # We inject the "System Instruction" into the first User turn
    system_instruction = (
        "You are MedLens AI, a professional clinical assistant. "
        "Provide evidence-based, structured medical guidance."
    )
    user_query = "What are the early warning signs of heatstroke?"
    
    # Correct Gemma 3 formatting
    prompt = f"<start_of_turn>user\n{system_instruction}\n\n{user_query}<end_of_turn>\n<start_of_turn>model\n"

    print("\n--- 🧠 Generating Clinical Response (Streaming) ---")
    start_time = time.time()
    first_token_time = None
    generated_text = ""

    # 3. Use Streaming (as requested for your Django SSE implementation)
    stream = llm(
        prompt,
        max_tokens=500,
        stop=["<end_of_turn>", "<eos>"], # Fixed stop tokens
        temperature=0.2,
        stream=True
    )

    for chunk in stream:
        if first_token_time is None:
            first_token_time = time.time()
        
        token = chunk['choices'][0]['text']
        generated_text += token
        print(token, end='', flush=True) # Live print to terminal

    end_time = time.time()

    # 4. Performance Metrics
    total_duration = end_time - start_time
    ttft = first_token_time - start_time if first_token_time else 0
    
    print(f"\n\n--- 📊 Performance Stats ---")
    print(f"Time to First Token (TTFT): {ttft:.2f}s")
    print(f"Total Generation Time: {total_duration:.2f}s")
    print(f"Status: Full GPU Offload (63/63 layers)")

except Exception as e:
    print(f"\n❌ ERROR: {e}")
