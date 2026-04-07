import os
import logging
from llama_cpp import Llama

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "Models", "medgemma-27b-it-UD-IQ2_XXS.gguf")

_llm_instance = None

SYSTEM_PROMPT = (
    "You are MedLens AI, a professional medical assistant embedded in a clinical "
    "decision-support application. Provide concise, accurate, and structured clinical "
    "guidance. Use bullet points for clarity where appropriate. Never state absolute "
    "diagnoses — always recommend professional consultation for confirmation. "
    "If an image context is provided, incorporate it into your assessment."
)


def get_llm():
    global _llm_instance
    if _llm_instance is None:
        if not os.path.exists(MODEL_PATH):
            logger.error(f"Model file not found at: {MODEL_PATH}")
            raise FileNotFoundError(f"Model not found at {MODEL_PATH}")

        logger.info("Loading MedGemma-27B (IQ2_XXS) onto RTX 3080...")

        try:
            _llm_instance = Llama(
                model_path=MODEL_PATH,
                n_gpu_layers=-1,        # Push all layers to RTX 3080
                n_ctx=2048,             # Keep low — protects VRAM on 10GB card
                n_threads=4,            # Match i5-7500 physical core count exactly
                n_batch=512,            # Prompt processing batch size
                flash_attn=True,        # Reduces VRAM usage during prompt processing
                type_k="q8_0",          # KV cache quantization (replaces deprecated f16_kv)
                type_v="q8_0",          # Saves ~1GB VRAM vs full precision
                verbose=False,
            )
            logger.info("Model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize Llama: {e}")
            raise

    return _llm_instance


def _build_prompt(messages: list) -> str:
    """
    Builds a Gemma 3 instruction-tuned prompt.

    Gemma 3 does not have a dedicated system turn.
    The system prompt is prepended to the first user message content.

    Format:
        <bos><start_of_turn>user
        {system_prompt} {user_message}<end_of_turn>
        <start_of_turn>model
        {assistant_response}<end_of_turn>
        ...
        <start_of_turn>model
    """
    prompt = "<bos>"
    first_user_seen = False

    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")

        # Flatten list-based content (image + text dicts from views.py)
        if isinstance(content, list):
            text_parts = [
                item["text"] for item in content
                if isinstance(item, dict) and item.get("type") == "text"
            ]
            content = " ".join(text_parts) if text_parts else "Medical image context provided."

        content = content.strip()

        if role == "user":
            # Prepend system prompt to first user turn only
            if not first_user_seen:
                content = f"{SYSTEM_PROMPT}\n\n{content}"
                first_user_seen = True
            prompt += f"<start_of_turn>user\n{content}<end_of_turn>\n"

        elif role in ("assistant", "model"):
            prompt += f"<start_of_turn>model\n{content}<end_of_turn>\n"

    # Trigger model generation
    prompt += "<start_of_turn>model\n"
    return prompt


def llm_call(messages: list) -> str:
    """
    Blocking (non-streaming) inference.
    Returns the complete response as a string.
    Use this if your view does not support SSE.
    """
    try:
        llm = get_llm()
        prompt = _build_prompt(messages)

        response = llm(
            prompt,
            max_tokens=800,
            temperature=0.2,
            repeat_penalty=1.1,
            stop=["<end_of_turn>", "<start_of_turn>"],   # Removed bare "user" — caused mid-sentence stops
        )

        return response["choices"][0]["text"].strip()

    except Exception as e:
        logger.exception("Inference error in llm_call")
        return "System Error: Local inference engine failed to respond."


def llm_stream(messages: list):
    """
    Streaming inference — yields text chunks as they are generated.
    Use this with Django StreamingHttpResponse or FastAPI StreamingResponse.

    Usage in Django view:
        def chat_view(request):
            ...
            def event_stream():
                for chunk in llm_stream(messages):
                    yield f"data: {chunk}\\n\\n"
            return StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    """
    try:
        llm = get_llm()
        prompt = _build_prompt(messages)

        stream = llm(
            prompt,
            max_tokens=800,
            temperature=0.2,
            repeat_penalty=1.1,
            stop=["<end_of_turn>", "<start_of_turn>"],
            stream=True,
        )

        for chunk in stream:
            token = chunk["choices"][0].get("text", "")
            if token:
                yield token

    except Exception as e:
        logger.exception("Inference error in llm_stream")
        yield "System Error: Local inference engine failed to respond."
