from llama_cpp import convert_hf_to_gguf

convert_hf_to_gguf(
    model_dir="qwen-world-history",
    output_file="qwen-world-history.gguf"
)


print("Model converted successfully!")