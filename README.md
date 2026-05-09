# AI Chatbot 🤖

A powerful and user-friendly AI chatbot built with Python and the Anthropic Claude API. Have intelligent conversations with an AI assistant that understands context and provides thoughtful, accurate responses.

## Features ✨

- **Intelligent Conversations**: Powered by Claude AI, one of the most advanced language models
- **Context Awareness**: Maintains conversation history for coherent multi-turn interactions
- **Easy to Use**: Simple command-line interface with intuitive commands
- **Error Handling**: Robust error handling and user-friendly error messages
- **Conversation Management**: Clear history, exit gracefully, and restart anytime
- **Customizable**: Easy to modify system prompts and behaviors

## Prerequisites 📋

Before you begin, ensure you have the following installed:

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **pip** - Python package manager (comes with Python)
- **Anthropic API Key** - Get one free at [console.anthropic.com](https://console.anthropic.com)

## Installation 🚀

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ai-chatbot.git
cd ai-chatbot
```

### 2. Create a Virtual Environment (Recommended)

```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install anthropic
```

### 4. Set Up Your API Key

#### Option A: Environment Variable (Recommended)

```bash
# On macOS/Linux
export ANTHROPIC_API_KEY='your-api-key-here'

# On Windows (Command Prompt)
set ANTHROPIC_API_KEY=your-api-key-here

# On Windows (PowerShell)
$env:ANTHROPIC_API_KEY='your-api-key-here'
```

#### Option B: Create a `.env` file

Create a `.env` file in the project root:

```env
ANTHROPIC_API_KEY=your-api-key-here
```

## Usage 💬

### Run the Chatbot

```bash
python ai_chatbot.py
```

### Commands

Once the chatbot is running, you can:

- **Chat**: Simply type your message and press Enter
- **Clear History**: Type `clear` to reset the conversation
- **Exit**: Type `exit` or `quit` to end the session

### Example Conversation

```
Welcome to AI Chatbot!
Chat with Claude AI. Type 'exit' or 'quit' to end the conversation.
Type 'clear' to reset the conversation history.
============================================================

You: Hello! What can you help me with?
Assistant: Hello! I'm an AI assistant here to help with a wide variety of tasks. I can:
- Answer questions on virtually any topic
- Help with writing, editing, and brainstorming
- Explain complex concepts
- Provide coding help and debugging
- Have thoughtful discussions
- And much more!

Feel free to ask me anything. What would you like help with?

You: Can you explain machine learning in simple terms?
Assistant: Of course! Machine learning is a way to teach computers to learn from examples...
```

## Project Structure 📁

```
ai-chatbot/
├── ai_chatbot.py      # Main chatbot script
├── README.md          # This file
├── requirements.txt   # Python dependencies
└── .gitignore         # Git ignore file
```

## Requirements 📦

- anthropic>=0.7.0
- python>=3.8

See `requirements.txt` for full list:

```
anthropic>=0.7.0
```

## Configuration ⚙️

You can customize the chatbot by editing the `system_prompt` variable in `ai_chatbot.py`:

```python
system_prompt = """You are a helpful AI assistant. 
Customize this prompt to change the chatbot's behavior and personality!"""
```

## Troubleshooting 🔧

### API Key Not Found
- Ensure your ANTHROPIC_API_KEY environment variable is set correctly
- Check that there are no typos in your API key
- Restart your terminal after setting the environment variable

### Module Not Found Error
```bash
# Make sure you've installed the required packages
pip install -r requirements.txt
```

### Connection Issues
- Check your internet connection
- Verify the Anthropic API is accessible
- Check if your API key has valid credits

## API Costs 💰

This chatbot uses the Anthropic Claude API. Note that:
- Free trial credits are available for new accounts
- Pay-as-you-go pricing applies after free credits are used
- Check [Anthropic pricing](https://www.anthropic.com/pricing) for current rates

## Features You Can Add 🚀

- **File I/O**: Save/load conversations to files
- **Multiple Models**: Support for different Claude models
- **Web Interface**: Create a Flask/Django web UI
- **Database**: Store conversation history in a database
- **Voice Input**: Add speech-to-text capabilities
- **Streaming**: Implement streaming responses for faster feedback

## Contributing 🤝

Contributions are welcome! Please feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License 📜

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments 🙏

- [Anthropic](https://www.anthropic.com/) for Claude AI
- [Python](https://www.python.org/) for the programming language
- Contributors and users of this project

## Support 💬

If you have questions or need help:

1. Check the Troubleshooting section above
2. Review [Anthropic Documentation](https://docs.anthropic.com/)
3. Open an issue on GitHub
4. Reach out via email (add your contact info here)

## Roadmap 📈

- [ ] Web UI with Flask
- [ ] Conversation persistence to database
- [ ] Support for different Claude models
- [ ] Streaming responses
- [ ] Voice input/output
- [ ] Multi-language support
- [ ] Docker containerization

---

**Happy chatting! 🎉** If you find this project useful, please consider giving it a star ⭐
