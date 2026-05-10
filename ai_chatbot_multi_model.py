#!/usr/bin/env python3
"""
Multi-Model AI Chatbot - Supporting Claude, Gemini, GPT-4, and more
"""

import os
import sys
from typing import Optional, List, Dict
from abc import ABC, abstractmethod
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Google Gemini API Configuration
GOOGLE_API_KEY = "AIzaSyC9JEuLjmwm_K3Tc-V9ln9wVUC90bMhtNY"

# Import API clients
try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None

try:
    import openai
except ImportError:
    openai = None

try:
    import requests
except ImportError:
    requests = None


class ModelProvider(ABC):
    """Abstract base class for AI model providers"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.conversation_history = []
    
    @abstractmethod
    def get_response(self, user_message: str) -> str:
        """Get response from the model"""
        pass
    
    @abstractmethod
    def clear_history(self):
        """Clear conversation history"""
        pass
    
    def add_to_history(self, role: str, content: str):
        """Add message to conversation history"""
        self.conversation_history.append({"role": role, "content": content})


class ClaudeProvider(ModelProvider):
    """Anthropic Claude API provider"""
    
    MODELS = {
        "Claude Opus 4.7": "claude-opus-4-7",
        "Claude 3.5 Sonnet": "claude-3-5-sonnet-20241022",
        "Claude 3 Opus": "claude-3-opus-20240229",
        "Claude 3 Haiku": "claude-3-haiku-20240307",
    }
    
    def __init__(self, api_key: str, model: str = "claude-opus-4-7"):
        super().__init__(api_key)
        if not Anthropic:
            raise ImportError("Anthropic library not installed. Run: pip install anthropic")
        self.client = Anthropic(api_key=api_key)
        self.model = model
    
    def get_response(self, user_message: str) -> str:
        """Get response from Claude"""
        self.add_to_history("user", user_message)
        
        # Check if using Claude Opus 4.7 with extended thinking
        if "opus-4-7" in self.model:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=20000,
                thinking={
                    "type": "adaptive"
                },
                system="You are a helpful, intelligent AI assistant. Provide accurate and thoughtful responses.",
                messages=self.conversation_history
            )
        else:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system="You are a helpful, intelligent AI assistant. Provide accurate and thoughtful responses.",
                messages=self.conversation_history
            )
        
        assistant_message = response.content[0].text
        self.add_to_history("assistant", assistant_message)
        return assistant_message
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []


class GeminiProvider(ModelProvider):
    """Google Gemini API provider"""
    
    MODELS = {
        "Gemini 3.0 Pro": "gemini-3.0-pro",
        "Gemini 2.0 Flash": "gemini-2.0-flash",
        "Gemini 1.5 Pro": "gemini-1.5-pro",
        "Gemini 1.5 Flash": "gemini-1.5-flash",
    }
    
    def __init__(self, api_key: str, model: str = "gemini-1.5-pro"):
        super().__init__(api_key)
        if not genai:
            raise ImportError("Google Generative AI library not installed. Run: pip install google-generativeai")
        
        # Configure Google Gemini API with the provided API key
        genai.configure(api_key=api_key)
        print(f"✓ Google Gemini API configured successfully with API Key: {api_key[:20]}...")
        
        self.model = genai.GenerativeModel(model)
        self.chat = self.model.start_chat(history=[])
    
    def get_response(self, user_message: str) -> str:
        """Get response from Gemini"""
        self.add_to_history("user", user_message)
        
        try:
            response = self.chat.send_message(user_message)
            assistant_message = response.text
            
            self.add_to_history("assistant", assistant_message)
            return assistant_message
        except Exception as e:
            error_message = f"Error getting response from Gemini: {str(e)}"
            print(f"❌ {error_message}")
            return error_message
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        self.chat = self.model.start_chat(history=[])


class GPT4Provider(ModelProvider):
    """OpenAI GPT-4 API provider"""
    
    MODELS = {
        "GPT-4o": "gpt-4o",
        "GPT-4 Turbo": "gpt-4-turbo",
        "GPT-4": "gpt-4",
        "GPT-3.5 Turbo": "gpt-3.5-turbo",
    }
    
    def __init__(self, api_key: str, model: str = "gpt-4o"):
        super().__init__(api_key)
        if not openai:
            raise ImportError("OpenAI library not installed. Run: pip install openai")
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
    
    def get_response(self, user_message: str) -> str:
        """Get response from GPT-4"""
        self.add_to_history("user", user_message)
        
        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=1024,
            messages=self.conversation_history,
            system="You are a helpful, intelligent AI assistant. Provide accurate and thoughtful responses."
        )
        
        assistant_message = response.choices[0].message.content
        self.add_to_history("assistant", assistant_message)
        return assistant_message
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []


class NanoBananaProvider(ModelProvider):
    """Banana.dev Nano LLM provider"""
    
    MODELS = {
        "Nano Banana": "nano-banana",
        "Falcon 7B": "falcon-7b",
    }
    
    def __init__(self, api_key: str, model: str = "nano-banana"):
        super().__init__(api_key)
        if not requests:
            raise ImportError("Requests library not installed. Run: pip install requests")
        self.model = model
        self.endpoint = "https://api.banana.dev/analyze"
    
    def get_response(self, user_message: str) -> str:
        """Get response from Nano Banana"""
        self.add_to_history("user", user_message)
        
        payload = {
            "messages": self.conversation_history,
            "model": self.model
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(self.endpoint, json=payload, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        assistant_message = result.get("output", "No response received")
        
        self.add_to_history("assistant", assistant_message)
        return assistant_message
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []


class MistralProvider(ModelProvider):
    """Mistral AI provider"""
    
    MODELS = {
        "Mistral Large": "mistral-large-latest",
        "Mistral Medium": "mistral-medium-latest",
        "Mistral Small": "mistral-small-latest",
    }
    
    def __init__(self, api_key: str, model: str = "mistral-large-latest"):
        super().__init__(api_key)
        if not openai:
            raise ImportError("OpenAI library not installed. Run: pip install openai")
        self.client = openai.OpenAI(api_key=api_key, base_url="https://api.mistral.ai/v1")
        self.model = model
    
    def get_response(self, user_message: str) -> str:
        """Get response from Mistral"""
        self.add_to_history("user", user_message)
        
        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=1024,
            messages=self.conversation_history
        )
        
        assistant_message = response.choices[0].message.content
        self.add_to_history("assistant", assistant_message)
        return assistant_message
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []


class ChatbotManager:
    """Manage chatbot with multiple model support"""
    
    PROVIDERS = {
        "claude": (ClaudeProvider, "ANTHROPIC_API_KEY"),
        "gemini": (GeminiProvider, "GOOGLE_API_KEY"),
        "gpt-4": (GPT4Provider, "OPENAI_API_KEY"),
        "banana": (NanoBananaProvider, "BANANA_API_KEY"),
        "mistral": (MistralProvider, "MISTRAL_API_KEY"),
    }
    
    def __init__(self):
        self.current_provider: Optional[ModelProvider] = None
        self.current_provider_name: str = ""
    
    def list_available_providers(self) -> List[str]:
        """List providers with available API keys"""
        available = []
        for provider_name, (_, env_key) in self.PROVIDERS.items():
            api_key = None
            
            # Special handling for Gemini - use hardcoded API key as fallback
            if provider_name == "gemini":
                api_key = os.environ.get(env_key) or GOOGLE_API_KEY
            else:
                api_key = os.environ.get(env_key)
            
            if api_key:
                available.append(provider_name)
        
        return available
    
    def list_models(self, provider_name: str) -> Dict[str, str]:
        """List models for a provider"""
        if provider_name not in self.PROVIDERS:
            return {}
        
        provider_class, _ = self.PROVIDERS[provider_name]
        return provider_class.MODELS
    
    def set_provider(self, provider_name: str, model_name: str = None) -> bool:
        """Set the current provider and model"""
        if provider_name not in self.PROVIDERS:
            print(f"Unknown provider: {provider_name}")
            return False
        
        provider_class, env_key = self.PROVIDERS[provider_name]
        
        # Special handling for Gemini - use hardcoded API key as fallback
        if provider_name == "gemini":
            api_key = os.environ.get(env_key) or GOOGLE_API_KEY
        else:
            api_key = os.environ.get(env_key)
        
        if not api_key:
            print(f"Error: {env_key} environment variable not set.")
            return False
        
        try:
            models = provider_class.MODELS
            
            if model_name is None:
                model_name = list(models.values())[0]
            elif model_name in models:
                model_name = models[model_name]
            
            self.current_provider = provider_class(api_key, model_name)
            self.current_provider_name = provider_name
            print(f"✓ Switched to {provider_name} - {model_name}")
            return True
        
        except Exception as e:
            print(f"Error initializing {provider_name}: {str(e)}")
            return False
    
    def get_response(self, user_message: str) -> str:
        """Get response from current provider"""
        if not self.current_provider:
            return "No provider selected. Use 'provider' command to select one."
        return self.current_provider.get_response(user_message)
    
    def clear_history(self):
        """Clear conversation history"""
        if self.current_provider:
            self.current_provider.clear_history()


def display_help():
    """Display help message"""
    print("""
╔════════════════════════════════════════════════════════════╗
║           Multi-Model AI Chatbot Commands                   ║
╠════════════════════════════════════════════════════════════╣
║  provider          - List/switch AI providers              ║
║  models [name]     - List models for a provider            ║
║  clear             - Clear conversation history            ║
║  help              - Show this help message                ║
║  exit/quit         - Exit the chatbot                      ║
╚════════════════════════════════════════════════════════════╝
    """)


def main():
    """Main chatbot function"""
    print("=" * 60)
    print("🤖 Multi-Model AI Chatbot with Google Gemini")
    print("=" * 60)
    
    manager = ChatbotManager()
    
    # Check available providers
    available = manager.list_available_providers()
    
    if not available:
        print("\n❌ Error: No API keys found!")
        print("\nPlease set up your .env file:")
        print("  1. Copy .env.example to .env")
        print("  2. Add your API keys to .env")
        print("\nRequired API keys:")
        print("  - ANTHROPIC_API_KEY (for Claude)")
        print("  - GOOGLE_API_KEY (for Gemini)")
        print("  - OPENAI_API_KEY (for GPT-4)")
        print("  - BANANA_API_KEY (for Nano Banana)")
        print("  - MISTRAL_API_KEY (for Mistral)")
        sys.exit(1)
    
    # Auto-select first available provider
    if not manager.set_provider(available[0]):
        print("Failed to initialize any provider")
        sys.exit(1)
    
    print(f"\n✓ Available providers: {', '.join(available)}")
    print(f"✓ Current provider: {manager.current_provider_name}")
    print("\nType 'help' for commands or start chatting!")
    print("-" * 60 + "\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() == "help":
                display_help()
                continue
            
            if user_input.lower() == "exit" or user_input.lower() == "quit":
                print("\nThank you for chatting! Goodbye! 👋")
                break
            
            if user_input.lower() == "clear":
                manager.clear_history()
                print("✓ Conversation history cleared.\n")
                continue
            
            if user_input.lower().startswith("provider"):
                parts = user_input.split()
                if len(parts) > 1:
                    provider_name = parts[1]
                    model_name = parts[2] if len(parts) > 2 else None
                    manager.set_provider(provider_name, model_name)
                else:
                    print("\nAvailable providers:")
                    for provider in available:
                        mark = "✓" if provider == manager.current_provider_name else " "
                        print(f"  [{mark}] {provider}")
                    print("\nUsage: provider <name> [model]")
                continue
            
            if user_input.lower().startswith("models"):
                parts = user_input.split()
                provider_name = parts[1] if len(parts) > 1 else manager.current_provider_name
                models = manager.list_models(provider_name)
                if models:
                    print(f"\nModels for {provider_name}:")
                    for display_name, model_id in models.items():
                        print(f"  • {display_name} ({model_id})")
                    print()
                else:
                    print(f"No models found for {provider_name}\n")
                continue
            
            # Get response from current provider
            response = manager.get_response(user_input)
            print(f"\nAssistant: {response}\n")
        
        except KeyboardInterrupt:
            print("\n\nChat interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")


if __name__ == "__main__":
    main()
