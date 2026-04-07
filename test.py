from llama_cpp import Llama
import os

# Path to your 13GB MedGemma file
model_path = "./Model/medgemma-27b-it-UD-Q3_K_XL.gguf"

print("--- Initializing MedGemma on RTX 3080 ---")
try:
    llm = Llama(
        model_path=model_path,
        n_gpu_layers=28,  # Offload ~85% of the model to VRAM
        n_ctx=1024,       # Context window
        n_threads=4,      # Matches your i5-7500 physical cores
        verbose=True      # CRITICAL: This shows us the CUDA load logs
    )
    
    prompt = "<start_of_turn>user\nExplain why offline AI is important for clinical settings.<end_of_turn>\n<start_of_turn>model\n"
    
    print("\n--- Generating Response ---")
    output = llm(prompt, max_tokens=100, stop=["<end_of_turn>"])
    print("\nAI Response:", output['choices'][0]['text'])
    
except Exception as e:
    print(f"\n[ERROR]: {e}")
