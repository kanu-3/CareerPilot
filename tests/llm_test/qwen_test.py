from backend.llm.qwen import qwen_model


response = qwen_model.generate(
    prompt=(
        "Explain in 3 short points what an AI career agent "
        "could do for a software engineer."
    )
)

print("\nQwen response:\n")
print(response)