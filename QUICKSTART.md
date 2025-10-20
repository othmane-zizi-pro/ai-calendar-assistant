# 🚀 Quick Start - AI Calendar Assistant with MCP + Ollama

Get your AI calendar assistant with **local LLM** and **MCP protocol** running in under 10 minutes!

---

## Step 1: Install Ollama (2 minutes)

```bash
# macOS
brew install ollama

# Start Ollama service (keep this terminal open)
ollama serve

# In a NEW terminal, pull Llama 3.2 model (2GB download)
ollama pull llama3.2:3b

# Test it works
ollama run llama3.2:3b "Hello!"
# Press Ctrl+D to exit
```

---

## Step 2: Install Dependencies (1 minute)

```bash
cd syntra-ai
pip install -r requirements.txt
```

This installs:
- `mcp` - Model Context Protocol SDK
- `mcp-client-for-ollama` - Bridges Ollama to MCP servers
- `google-api-python-client` - Google Calendar API
- All other dependencies

---

## Step 3: Get Google Calendar Credentials (3 minutes)

### Quick Steps:
1. Go to https://console.cloud.google.com/
2. Create new project → "Calendar Assistant"
3. Enable "Google Calendar API"
4. Create OAuth 2.0 credentials (Desktop app)
5. Download JSON → save as `credentials.json` in project root
6. Add your email as test user in OAuth consent screen

**Detailed guide:** See [SETUP.md](SETUP.md) for step-by-step with screenshots

---

## Step 4: Authenticate with Google (1 minute)

```bash
# Run the calendar server once to authenticate
python3 run_calendar_server.py
```

**What happens:**
1. Browser opens automatically
2. Sign in to Google
3. Click "Continue" (ignore "unverified app" warning)
4. Grant calendar permissions
5. See "The authentication flow has completed" in browser
6. Press `Ctrl+C` in terminal to stop server

**Created:** `token.pickle` (your auth token, auto-renewed)

---

## Step 5: Start Your AI Calendar Assistant! (30 seconds)

```bash
# Launch MCP client with Ollama
ollmcp --servers-json ollmcp_config.json --model llama3.2:3b
```

**You should see:**
```
╭──────────────────────────────────────────────────────────────╮
│        Welcome to the MCP Client for Ollama 🦙               │
╰──────────────────────────────────────────────────────────────╯

Connected to calendar server with 7 tools
🧠 Current model: llama3.2:3b
```

---

## 🎉 Try It Out!

### Check Today's Schedule
```
You: What's on my calendar today?

AI: [Calls get_today_events via MCP]
    You have 3 events today:
    1. Team Standup at 9:00 AM
    2. Client Meeting at 2:00 PM
    3. Gym at 6:00 PM
```

### Create a Meeting
```
You: Create a meeting tomorrow at 3pm called "Project Review"

AI: [Calls create_event via MCP]
    ✅ Event created!
    Title: Project Review
    Time: Tomorrow 3:00 PM - 4:00 PM
```

### Check Availability
```
You: Am I free Friday afternoon?

AI: [Calls check_availability via MCP]
    Yes! You're completely free after 2 PM on Friday.
```

### Search Events
```
You: Find all my coffee chats this week

AI: [Calls search_events via MCP]
    Found 2 events matching 'coffee':
    1. Coffee with Sarah - Mon 10 AM
    2. Team Coffee - Wed 3 PM
```

---

## 🔧 Available MCP Tools

Your AI automatically uses these calendar tools:

- **list_events** - Get upcoming events
- **get_today_events** - Show today's schedule
- **create_event** - Create new events
- **search_events** - Search by keyword
- **update_event** - Modify events
- **delete_event** - Remove events
- **check_availability** - Check if times are free

---

## 💡 ollmcp Commands

While chatting, type these commands:

| Command | What it does |
|---------|-------------|
| `model` or `m` | Switch Ollama models |
| `tools` or `t` | View available MCP tools |
| `help` or `h` | Show help |
| `quit` or `q` | Exit |

---

## 🎯 What Makes This Special?

✅ **100% Local LLM** - Llama 3.2 runs on your machine, zero API costs
✅ **MCP Protocol** - Proper tool integration like Claude Desktop
✅ **Privacy-First** - Only calendar sync requires internet
✅ **Fast** - 1-2 second responses
✅ **Free Forever** - No subscriptions, no cloud costs

---

## 🐛 Troubleshooting

### "Connection refused"
**Fix:** Make sure Ollama is running:
```bash
ollama serve
```

### "Could not connect to calendar server"
**Fix:** Test server standalone:
```bash
python3 run_calendar_server.py
# Should start without errors, Ctrl+C to stop
```

### "Authentication failed"
**Fix:** Re-authenticate:
```bash
rm token.pickle
python3 run_calendar_server.py
```

### Model is slow?
**Fix:** Try a smaller model:
```bash
ollama pull gemma:2b
ollmcp --servers-json ollmcp_config.json --model gemma:2b
```

---

## 🔄 Try Different Models

```bash
# Faster, less RAM (1.4GB)
ollama pull gemma:2b
ollmcp --servers-json ollmcp_config.json --model gemma:2b

# Higher quality (4GB)
ollama pull mistral:7b
ollmcp --servers-json ollmcp_config.json --model mistral:7b
```

---

## 📚 Next Steps

- **Full setup guide:** [SETUP.md](SETUP.md)
- **Architecture details:** [README.md](README.md)
- **Model comparison:** [LOCAL_LLM_SETUP.md](LOCAL_LLM_SETUP.md)
- **GitHub publishing:** [GITHUB_SETUP.md](GITHUB_SETUP.md)

---

**You're all set!** Enjoy your privacy-first, cost-free AI calendar assistant! 🚀
