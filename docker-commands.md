```bash
curl http://localhost:12434/engines/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "ai/deepseek-r1-distill-llama",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role":"user",
                "content":"Please write 500 words about the fall of Rome."
            }
        ]
    }'
```

_From within a container_
```bash
curl http://model-runner.docker.internal/engines/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "ai/deepseek-r1-distill-llama",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role":"user",
                "content":"Please write 500 words about the fall of Rome."
            }
        ]
    }'
```