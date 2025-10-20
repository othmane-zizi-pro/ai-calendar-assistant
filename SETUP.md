# Calendar Assistant Setup Guide

Complete setup guide for your lightweight personal calendar assistant with local LLM.

## Prerequisites

- Python 3.8+
- Ollama (for local LLM)
- Google Cloud Project (for Calendar API)

## Step 1: Install Ollama & Pull Model

### Install Ollama

**macOS:**
```bash
brew install ollama
# OR
curl -fsSL https://ollama.com/install.sh | sh
```

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
Download from https://ollama.com/download

### Start Ollama
```bash
# Start the Ollama service
ollama serve
```

### Pull a Lightweight Model

```bash
# Recommended: Llama 3.2 3B (best balance)
ollama pull llama3.2:3b

# Alternative options:
# ollama pull gemma:2b       # Faster, smaller
# ollama pull phi3:mini      # Good for code
# ollama pull mistral:7b     # More powerful
```

### Verify Installation
```bash
ollama list
ollama run llama3.2:3b "Hello!"
```

## Step 2: Install Python Dependencies

```bash
cd syntra-ai

# Install calendar assistant requirements
pip install -r requirements-calendar.txt

# Or install individually:
pip install mcp google-api-python-client google-auth-httplib2 google-auth-oauthlib ollama langchain rich click python-dotenv pytz
```

## Step 3: Set Up Google Calendar API

### 3.1 Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Name it something like "Personal Calendar Assistant"

### 3.2 Enable Google Calendar API

1. In the Cloud Console, go to **APIs & Services** → **Library**
2. Search for "Google Calendar API"
3. Click **Enable**

### 3.3 Create OAuth 2.0 Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **OAuth client ID**
3. If prompted, configure the OAuth consent screen:
   - User Type: **External**
   - App name: "Personal Calendar Assistant"
   - User support email: your email
   - Developer contact: your email
   - Scopes: Leave default
   - Test users: Add your Gmail address
4. Back to **Create OAuth client ID**:
   - Application type: **Desktop app**
   - Name: "Calendar Assistant"
5. Click **Create**
6. Click **Download JSON**
7. Save it as `credentials.json` in your `syntra-ai` directory

```bash
# Your credentials file should be here:
# /Users/othmanezizi/syntra-ai/credentials.json
```

### 3.4 First-Time Authentication

The first time you run the assistant, it will:
1. Open a browser window
2. Ask you to log in to Google
3. Request calendar permissions
4. Save a token for future use

## Step 4: Test Your Setup

### Test Google Calendar Connection

```bash
python calendar_assistant.py today
```

This will:
- Open browser for first-time auth
- Show today's calendar events
- Create `token.pickle` for future use

### Test Ollama Integration

```bash
# Make sure Ollama is running
curl http://localhost:11434/api/tags

# Should return list of models
```

### Test the Full Assistant

```bash
python calendar_assistant.py chat
```

Try these commands:
- "What's on my calendar today?"
- "Show me upcoming events"
- "Do I have any meetings tomorrow?"

## Step 5: CLI Commands Reference

```bash
# Interactive chat with AI assistant
python calendar_assistant.py chat

# Show today's events
python calendar_assistant.py today

# Show upcoming events
python calendar_assistant.py upcoming --days 7

# Quick daily summary
python calendar_assistant.py summary

# Search for events
python calendar_assistant.py search "dentist"

# Create an event
python calendar_assistant.py create "Team Meeting" \
  --start "2024-01-16T14:00:00" \
  --end "2024-01-16T15:00:00" \
  --location "Conference Room A"
```

## Step 6: MCP Server Setup (Optional - for Claude Desktop)

### Configure MCP Server

Edit Claude Desktop config:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Add:
```json
{
  "mcpServers": {
    "google-calendar": {
      "command": "python",
      "args": ["-m", "calendar_assistant.mcp_server.calendar_server"],
      "cwd": "/Users/othmanezizi/syntra-ai"
    }
  }
}
```

Restart Claude Desktop and it will have access to your calendar!

## Usage Examples

### Morning Routine

```bash
python calendar_assistant.py summary
```

Output:
```
📅 You have 3 event(s) today:

• Team Standup at 09:00
• Client Meeting at 14:00
• Gym Session at 18:00
```

### Interactive Assistant

```bash
python calendar_assistant.py chat
```

**Conversation:**
```
You: What's on my calendar today?
Assistant: You have 3 events scheduled for today:
1. Team Standup at 9:00 AM
2. Client Meeting at 2:00 PM
3. Gym Session at 6:00 PM

You: When is my next dentist appointment?
Assistant: Searching... You have a dentist appointment on January 20th at 10:00 AM.

You: Create a meeting for tomorrow at 3pm called "Project Review" for 1 hour
Assistant: I'll create that for you. Event "Project Review" has been scheduled for tomorrow (January 16th) from 3:00 PM to 4:00 PM.
```

## Troubleshooting

### "Ollama is not running"

```bash
# Start Ollama in a separate terminal
ollama serve

# Or run in background
nohup ollama serve > /dev/null 2>&1 &
```

### "credentials.json not found"

Make sure you've downloaded OAuth credentials from Google Cloud Console and saved them as `credentials.json` in the project root.

### "Permission denied" errors

Re-authenticate:
```bash
rm token.pickle
python calendar_assistant.py today
```

### Slow responses

Try a smaller model:
```bash
ollama pull gemma:2b
python calendar_assistant.py chat --model gemma:2b
```

### Calendar API quota exceeded

Google Calendar API has rate limits:
- 1,000,000 queries/day
- 3,000 queries/minute

For personal use, you'll never hit these limits.

## Advanced Configuration

### Change Default Model

Edit `calendar_assistant/llm/local_assistant.py`:
```python
def __init__(self, model: str = "llama3.2:3b"):  # Change default here
```

### Multiple Calendars

The assistant uses your "primary" calendar by default. To use multiple calendars, modify the functions in `calendar_assistant/utils/google_calendar.py` to accept `calendar_id` parameter.

### Customize System Prompt

Edit `calendar_assistant/llm/local_assistant.py` → `_get_system_prompt()` method to customize the assistant's personality and capabilities.

## Performance Tips

### Speed Optimizations

1. **Use a smaller model**: `gemma:2b` is 2-3x faster than `llama3.2:3b`
2. **Reduce context window**: Edit Ollama settings
3. **Cache responses**: The assistant already caches calendar data between requests

### Memory Usage

| Model | RAM Needed | Speed | Quality |
|-------|-----------|-------|---------|
| gemma:2b | 3GB | ⚡⚡⚡⚡ | ⭐⭐⭐ |
| llama3.2:3b | 4GB | ⚡⚡⚡ | ⭐⭐⭐⭐ |
| phi3:mini | 4GB | ⚡⚡⚡ | ⭐⭐⭐⭐ |
| mistral:7b | 8GB | ⚡⚡ | ⭐⭐⭐⭐⭐ |

## Next Steps

Once you're comfortable:

1. **Add more calendars**: Work, personal, family
2. **Integrate other tools**: Email, tasks, notes
3. **Create automation**: Morning briefings, meeting prep
4. **Build custom commands**: Add your own CLI commands
5. **Extend MCP server**: Add more calendar tools

Enjoy your personal AI calendar assistant! 🚀
