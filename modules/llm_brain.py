"""
LLM Brain Module
Uses Ollama for local language model inference with tool calling.
"""
import ollama
from typing import List, Dict, Optional


class LLMBrain:
    """LLM-based conversational brain using Ollama."""
    
    def __init__(
        self,
        model: str = "llama3.2:3b",
        system_prompt: str = "",
        max_history: int = 10
    ):
        """
        Initialize LLM brain.
        
        Args:
            model: Ollama model name
            system_prompt: System prompt for the model
            max_history: Maximum conversation history to maintain
        """
        self.model = model
        self.system_prompt = system_prompt
        self.max_history = max_history
        self.conversation_history: List[Dict[str, str]] = []
        
        # Verify Ollama is running and model exists
        try:
            ollama.list()
            print(f"Ollama connected. Using model: {model}")
        except Exception as e:
            print(f"Warning: Could not connect to Ollama: {e}")
            print("Make sure Ollama is installed and running.")
    
    def process(self, user_input: str) -> str:
        """
        Process user input and generate response.
        
        Args:
            user_input: User's text input
            
        Returns:
            LLM response (JSON string)
        """
        try:
            # Add user message to history
            self.conversation_history.append({
                "role": "user",
                "content": user_input
            })
            
            # Trim history if too long
            if len(self.conversation_history) > self.max_history * 2:
                # Keep system prompt and recent messages
                self.conversation_history = self.conversation_history[-(self.max_history * 2):]
            
            # Build messages
            messages = []
            
            # Add system prompt
            if self.system_prompt:
                messages.append({
                    "role": "system",
                    "content": self.system_prompt
                })
            
            # Add conversation history
            messages.extend(self.conversation_history)
            
            # Get response from Ollama
            response = ollama.chat(
                model=self.model,
                messages=messages,
                options={
                    "temperature": 0.3,  # Lower for more consistent JSON formatting
                    "top_p": 0.9,
                },
                format="json"  # Force JSON output mode
            )
            
            # Extract response text
            assistant_message = response['message']['content']
            
            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
            
        except Exception as e:
            print(f"LLM Error: {e}")
            # Return error as JSON
            error_response = '{"tool": "none", "response": "I apologize, but I encountered an error processing your request."}'
            return error_response
    
    def reset_conversation(self) -> None:
        """Clear conversation history."""
        self.conversation_history = []
        print("Conversation history cleared.")
    
    def get_history_length(self) -> int:
        """Get number of messages in history."""
        return len(self.conversation_history)
    
    def set_system_prompt(self, prompt: str) -> None:
        """Update system prompt."""
        self.system_prompt = prompt


if __name__ == "__main__":
    # Test LLM brain
    system_prompt = """You are JARVIS. Respond in JSON format:
    {"tool": "none", "response": "Your response here"}"""
    
    brain = LLMBrain(model="llama3.2:3b", system_prompt=system_prompt)
    
    print("Testing LLM Brain...")
    response = brain.process("Hello, who are you?")
    print(f"Response: {response}")

