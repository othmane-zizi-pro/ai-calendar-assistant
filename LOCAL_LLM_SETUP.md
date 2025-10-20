# Local LLM Setup Guide

## Install Ollama (Recommended - Easiest)

### macOS
```bash
# Download and install from official site
curl -fsSL https://ollama.com/install.sh | sh

# Or use Homebrew
brew install ollama
```

### Verify Installation
```bash
ollama --version
```

### Install a Lightweight Model

We'll use **Llama 3.2 (3B)** - perfect balance of speed and capability:

```bash
# Start Ollama service (run in background)
ollama serve

# In a new terminal, pull the model
ollama pull llama3.2:3b

# Test it
ollama run llama3.2:3b "Hello, how are you?"
```

### Other Good Lightweight Options

```bash
# Phi-3 Mini (3.8B) - Microsoft's efficient model
ollama pull phi3:mini

# Mistral 7B - More powerful but still fast
ollama pull mistral:7b

# Gemma 2B - Google's tiny but capable model
ollama pull gemma:2b
```

### Model Comparison

| Model | Size | RAM Needed | Speed | Quality | Best For |
|-------|------|------------|-------|---------|----------|
| **llama3.2:3b** | 2GB | 4GB | ⚡⚡⚡ | ⭐⭐⭐⭐ | **Recommended - Best balance** |
| gemma:2b | 1.4GB | 3GB | ⚡⚡⚡⚡ | ⭐⭐⭐ | Fastest, low memory |
| phi3:mini | 2.3GB | 4GB | ⚡⚡⚡ | ⭐⭐⭐⭐ | Code-focused |
| mistral:7b | 4.1GB | 8GB | ⚡⚡ | ⭐⭐⭐⭐⭐ | More accuracy |

## Verify Ollama is Running

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Should return list of installed models
```

## Alternative: LM Studio (GUI Option)

If you prefer a graphical interface:

1. Download LM Studio: https://lmstudio.ai/
2. Browse and download models through UI
3. Start local server
4. Use same API endpoint pattern

## Using Ollama API

Ollama provides an OpenAI-compatible API:

```python
import requests

response = requests.post('http://localhost:11434/api/generate', json={
    'model': 'llama3.2:3b',
    'prompt': 'What is the capital of France?',
    'stream': False
})

print(response.json()['response'])
```

## Performance Tips

### Speed up inference:
```bash
# Use GPU if available (automatic on M1/M2 Macs)
# Reduce context window for faster responses
ollama run llama3.2:3b --num-ctx 2048
```

### Check GPU usage (Mac):
```bash
# Monitor GPU activity
sudo powermetrics --samplers gpu_power -i 1000
```

## Troubleshooting

### Ollama won't start
```bash
# Kill existing process
pkill ollama

# Restart
ollama serve
```

### Model too slow
- Use a smaller model (gemma:2b)
- Reduce context window
- Close other applications

### Out of memory
- Use gemma:2b instead
- Restart Ollama
- Close browser tabs

## Next Steps

Once Ollama is running, proceed to set up the Google Calendar assistant!
