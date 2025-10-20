# 🗓️ AI Calendar Assistant

> Personal calendar management powered by **local LLM** (Ollama), **Google Calendar API**, and **Model Context Protocol (MCP)**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ollama](https://img.shields.io/badge/Ollama-llama3.2-green.svg)](https://ollama.com/)
[![MCP](https://img.shields.io/badge/MCP-Compatible-purple.svg)](https://modelcontextprotocol.io/)

A lightweight, privacy-first AI calendar assistant that runs entirely on your local machine. Chat with your calendar using natural language, powered by **Llama 3.2** running locally via **Ollama** - completely free, no API costs.

![Demo](https://img.shields.io/badge/Status-Working-brightgreen)

---

## ✨ Features

- 🤖 **Local AI** - Uses Ollama (llama3.2:3b) running on your machine
- 📅 **Google Calendar Integration** - Full read/write access via OAuth2
- 💬 **Natural Language** - Ask questions in plain English
- ⚡ **Fast** - Responses in 1-2 seconds
- 🔒 **Privacy-First** - LLM runs locally, only calendar sync requires internet
- 🆓 **100% Free** - No API costs, no subscriptions
- 🔌 **MCP Compatible** - Integrates with Claude Desktop and other MCP clients
- 🎨 **Beautiful CLI** - Rich terminal interface with color and formatting

---

## 🏗️ Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                     MCP Client for Ollama (ollmcp)             │
│               Terminal UI - Natural Language Interface          │
└─────────────────┬──────────────────────┬───────────────────────┘
                  │                      │
                  │ (MCP Protocol)       │ (Ollama API)
                  │                      │
                  ▼                      ▼
┌──────────────────────────────┐  ┌────────────────────────────┐
│   Calendar MCP Server        │  │   Ollama                   │
│   (calendar_server.py)       │  │   Llama 3.2 3B             │
│                              │  │   (Local LLM)              │
│   Exposes 7 Calendar Tools:  │  │                            │
│   • list_events              │  │   Handles:                 │
│   • get_today_events         │  │   • Intent parsing         │
│   • create_event             │  │   • Natural language       │
│   • search_events            │  │   • Response generation    │
│   • update_event             │  │   • Tool orchestration     │
│   • delete_event             │  │                            │
│   • check_availability       │  │                            │
└─────────────┬────────────────┘  └────────────────────────────┘
              │
              │ (Google Calendar API)
              │
              ▼
┌──────────────────────────────┐
│   GoogleCalendarClient       │
│   • OAuth2 Authentication    │
│   • Event CRUD Operations    │
└─────────────┬────────────────┘
              │
              ▼
┌──────────────────────────────┐
│      Google Calendar         │
│      (Cloud Storage)         │
└──────────────────────────────┘
```

**Flow:**
1. You type natural language → MCP Client (ollmcp)
2. Ollama (Llama 3.2) understands intent and determines which MCP tools to call
3. MCP Client calls appropriate calendar tools via MCP protocol
4. Calendar MCP Server executes Google Calendar operations
5. Response flows back through MCP → Ollama → formatted natural language response

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- macOS, Linux, or Windows
- Google account
- 4GB RAM (for local LLM)

### Installation

1. **Install Ollama**
   ```bash
   # macOS
   brew install ollama

   # Start Ollama service
   ollama serve

   # Pull the model (in a new terminal)
   ollama pull llama3.2:3b
   ```

2. **Clone & Setup**
   ```bash
   git clone https://github.com/othmane-zizi-pro/ai-calendar-assistant.git
   cd ai-calendar-assistant
   pip install -r requirements.txt
   ```

3. **Get Google Calendar Credentials**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable "Google Calendar API"
   - Create OAuth 2.0 credentials (Desktop app)
   - Download JSON and save as `credentials.json`
   - See [detailed setup guide](SETUP.md)

4. **Install MCP Client for Ollama**
   ```bash
   pip install mcp-client-for-ollama
   ```

5. **Run - Start Natural Language Calendar Chat**
   ```bash
   # First run - authenticate with Google (this will open browser)
   python run_calendar_server.py  # Test server once, then Ctrl+C

   # Start interactive MCP chat with Ollama
   ollmcp --servers-json ollmcp_config.json --model llama3.2:3b
   ```

---

## 💡 Usage

### Interactive MCP-Powered Chat

```bash
# Start the MCP client with Ollama
ollmcp --servers-json ollmcp_config.json --model llama3.2:3b
```

**Example conversation:**
```
You: What's on my calendar today?
AI: Let me check your calendar for today...
    [Calls get_today_events tool via MCP]

    You have 3 events scheduled today:
    1. Team Standup at 9:00 AM
    2. Client Meeting at 2:00 PM
    3. Gym Session at 6:00 PM

You: Create a meeting tomorrow at 3pm for 1 hour called "Project Review"
AI: I'll create that event for you...
    [Calls create_event tool via MCP]

    ✅ Done! Event "Project Review" scheduled for tomorrow 3:00 PM - 4:00 PM

You: Am I free on Friday afternoon?
AI: Let me check your availability...
    [Calls check_availability tool via MCP]

    Yes, you're free after 2:00 PM on Friday!
```

### Available MCP Tools

The calendar MCP server exposes these tools (automatically used by Ollama through the MCP client):

- **list_events** - Get upcoming calendar events
- **get_today_events** - Retrieve today's schedule
- **create_event** - Create new calendar event
- **search_events** - Search events by keyword
- **update_event** - Modify existing event
- **delete_event** - Remove event from calendar
- **check_availability** - Check if time slot is free

### Alternative: Use with Claude Desktop

If you prefer using Claude Desktop instead of the local Ollama setup:

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "calendar": {
      "command": "python3",
      "args": ["run_calendar_server.py"],
      "cwd": "/path/to/ai-calendar-assistant"
    }
  }
}
```

Restart Claude Desktop - now Claude can access your calendar via MCP!

---

## 🛠️ Technical Stack

### Core Technologies

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **MCP Client** | mcp-client-for-ollama (ollmcp) | Bridges Ollama with MCP servers, terminal UI |
| **Local LLM** | Ollama (Llama 3.2 3B) | Natural language understanding, intent parsing, tool orchestration |
| **MCP Server** | Model Context Protocol SDK | Exposes calendar tools via MCP protocol |
| **Calendar API** | Google Calendar API v3 | Event management, OAuth2 authentication |
| **NLP** | LangChain | Prompt engineering, chain-of-thought |

### Key Features Implementation

#### 1. **MCP Server - Tool Exposure**
```python
# Expose calendar tools via MCP protocol
@app.list_tools()
async def list_tools():
    return [
        Tool(name="list_events", description="List upcoming calendar events", ...),
        Tool(name="create_event", description="Create a new calendar event", ...),
        Tool(name="search_events", description="Search events by keyword", ...),
        Tool(name="get_today_events", ...),
        Tool(name="update_event", ...),
        Tool(name="delete_event", ...),
        Tool(name="check_availability", ...)
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Any):
    client = get_calendar_client()
    if name == "list_events":
        events = client.list_events(...)
        return [TextContent(type="text", text=formatted_output)]
```

#### 2. **OAuth2 Authentication**
```python
# Google Calendar OAuth2 flow
flow = InstalledAppFlow.from_client_secrets_file(
    'credentials.json',
    SCOPES=['https://www.googleapis.com/auth/calendar']
)
creds = flow.run_local_server(port=0)
```

#### 3. **MCP + Ollama Integration**
```bash
# ollmcp connects Ollama to MCP servers
ollmcp --servers-json ollmcp_config.json --model llama3.2:3b

# User types: "What's on my calendar today?"
# → Ollama (Llama 3.2) understands intent
# → Calls get_today_events tool via MCP protocol
# → Calendar server executes Google Calendar API call
# → Response formatted and returned via MCP
# → Ollama generates natural language response
```

---

## 📊 Performance

| Metric | Value |
|--------|-------|
| **Response Time** | 1-2 seconds (local LLM) |
| **Memory Usage** | ~4GB RAM (Llama 3.2 3B) |
| **API Calls** | Only for calendar sync (free tier: 1M requests/day) |
| **Offline Capability** | LLM works offline, calendar requires internet |
| **Cost** | $0/month (100% free) |

### Model Comparison

| Model | Size | RAM | Speed | Quality | Use Case |
|-------|------|-----|-------|---------|----------|
| llama3.2:3b | 2GB | 4GB | ⚡⚡⚡ | ⭐⭐⭐⭐ | **Recommended** |
| gemma:2b | 1.4GB | 3GB | ⚡⚡⚡⚡ | ⭐⭐⭐ | Faster, lower RAM |
| phi3:mini | 2.3GB | 4GB | ⚡⚡⚡ | ⭐⭐⭐⭐ | Better code understanding |
| mistral:7b | 4.1GB | 8GB | ⚡⚡ | ⭐⭐⭐⭐⭐ | Highest quality |

---

## 🔧 Project Structure

```
ai-calendar-assistant/
├── calendar_assistant/
│   ├── mcp_server/
│   │   ├── __init__.py
│   │   └── calendar_server.py      # MCP server implementation
│   ├── llm/
│   │   ├── __init__.py
│   │   └── local_assistant.py      # Ollama integration
│   ├── utils/
│   │   ├── __init__.py
│   │   └── google_calendar.py      # Google Calendar API wrapper
│   ├── __init__.py
│   └── cli.py                      # CLI interface
├── calendar_assistant.py            # Main entry point
├── requirements.txt                 # Dependencies
├── verify_setup.py                  # Setup verification script
├── .env.example                     # Environment configuration template
├── .gitignore                       # Git ignore rules
├── README.md                        # This file
├── QUICKSTART.md                    # 5-minute setup guide
├── SETUP.md                         # Detailed setup instructions
└── LOCAL_LLM_SETUP.md              # Ollama installation guide
```

---

## 🎯 MCP Tools Available

When integrated with Claude Desktop, the following tools are exposed:

| Tool | Description | Parameters |
|------|-------------|------------|
| `list_events` | Get upcoming calendar events | `max_results`, `days_ahead` |
| `get_today_events` | Retrieve today's schedule | None |
| `create_event` | Create a new calendar event | `summary`, `start_time`, `end_time`, `description`, `location` |
| `search_events` | Search events by keyword | `query`, `max_results` |
| `update_event` | Modify existing event | `event_id`, `summary`, `start_time`, `end_time` |
| `delete_event` | Remove event from calendar | `event_id` |
| `check_availability` | Check if time slot is free | `start_time`, `end_time` |

---

## 🔐 Privacy & Security

- ✅ **Local LLM** - All AI processing happens on your machine
- ✅ **OAuth2** - Secure Google authentication
- ✅ **No Cloud LLM APIs** - No data sent to OpenAI/Anthropic
- ✅ **Credentials Protected** - `credentials.json` and `token.pickle` in `.gitignore`
- ✅ **Open Source** - Full transparency, audit the code yourself

**Data Flow:**
1. Your query → Local LLM (Ollama) → Intent extracted
2. Calendar operation → Google Calendar API (OAuth2)
3. Response → Local LLM → Natural language response

---

## 📚 Documentation

- [Quick Start Guide](QUICKSTART.md) - Get running in 5 minutes
- [Setup Guide](SETUP.md) - Detailed installation instructions
- [Local LLM Setup](LOCAL_LLM_SETUP.md) - Ollama configuration

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Ollama](https://ollama.com/) - Local LLM runtime
- [Model Context Protocol](https://modelcontextprotocol.io/) - AI integration framework
- [Google Calendar API](https://developers.google.com/calendar) - Calendar integration
- [LangChain](https://www.langchain.com/) - LLM orchestration
- [Rich](https://github.com/Textualize/rich) - Beautiful terminal output

---

## 📧 Contact

**Othmane Zizi** - [othmane.zizi.pro@gmail.com](mailto:othmane.zizi.pro@gmail.com)

Project Link: [https://github.com/othmane-zizi-pro/ai-calendar-assistant](https://github.com/othmane-zizi-pro/ai-calendar-assistant)

---

**⭐ Star this repo if you found it helpful!**
