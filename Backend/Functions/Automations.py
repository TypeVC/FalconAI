import os
import re
import sys
from typing import Optional, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

class FalconAI:
    """
    Falcon AI Assistant - Advanced Task Executor
    A powerful AI assistant that can execute system tasks safely and efficiently.
    """
    
    def __init__(self):
        """Initialize Falcon AI Assistant"""
        self.load_environment()
        self.initialize_client()
        self.setup_conversation_context()
        
    def load_environment(self):
        """Load environment variables safely"""
        try:
            load_dotenv()
            self.api_key = os.getenv("GROQ_API_KEY")
            if not self.api_key:
                raise ValueError("GROQ_API_KEY not found in environment variables")
        except Exception as e:
            print(f"❌ Failed to load environment: {e}")
            sys.exit(1)
            
    def initialize_client(self):
        """Initialize the Groq API client"""
        try:
            self.client = OpenAI(
                base_url="https://api.groq.com/openai/v1",
                api_key=self.api_key
            )
        except Exception as e:
            print(f"❌ Failed to initialize API client: {e}")
            sys.exit(1)
            
    def setup_conversation_context(self):
        """Setup the conversation context for Falcon AI"""
        self.messages = [
            {
                "role": "system", 
                "content": "You are Falcon, an advanced AI assistant created by Utkarsh Rishi. You are designed to be helpful, safe, and efficient."
            },
            {
                "role": "system", 
                "content": """You are a task executor that can perform system operations safely. Always prioritize user safety and system security.

                ### 1. **Automating YouTube Video Search & Google Search**
                **User:** "Write a Python script to search YouTube and Google automatically."

                **Falcon:**
                ```python
                import pywhatkit

                def play_song(song: str) -> None:
                    pywhatkit.playonyt(song)

                def google_search(query: str) -> None:
                    pywhatkit.search(query)

                # Example usage
                play_song("Victory Anthem")
                google_search("Latest AI advancements")

                """
            },
            {
                "role": "system", 
                "content": "Available modules: webbrowser, pyautogui, time, pyperclip, random, datetime, tkinter, os, subprocess (use carefully), psutil for process management."
            },
            {
                "role": "system", 
                "content": "IMPORTANT: Never use input() functions. Always use default paths. Validate all operations before execution."
            },
            {
                "role": "system", 
                "content": "For application control, prefer using psutil for process management over os.system for better cross-platform compatibility."
            },
            # Examples for better context
            {
                "role": "user", 
                "content": "open Google Chrome"
            },
            {
                "role": "assistant", 
                "content": "I'll open Google Chrome for you.\n```python\nimport webbrowser\nimport time\n\n# Open Chrome with Google homepage\nwebbrowser.register('chrome', None, webbrowser.BackgroundBrowser('chrome'))\nwebbrowser.get('chrome').open('https://www.google.com')\ntime.sleep(1)  # Brief pause for application to load\nprint('Google Chrome opened successfully')\n```"
            },
            {
                "role": "user", 
                "content": "close Google Chrome"
            },
            {
                "role": "assistant", 
                "content": "I'll close Google Chrome safely.\n```python\nimport psutil\nimport os\nimport time\n\ntry:\n    # Find and terminate Chrome processes\n    for proc in psutil.process_iter(['pid', 'name']):\n        if 'chrome' in proc.info['name'].lower():\n            proc.terminate()\n    time.sleep(2)\n    print('Google Chrome closed successfully')\nexcept Exception as e:\n    # Fallback method\n    if os.name == 'nt':  # Windows\n        os.system('taskkill /im chrome.exe /f')\n    else:  # Unix/Linux/Mac\n        os.system('pkill -f chrome')\n    print('Chrome closed using fallback method')\n```"
            }
        ]
        
    def execute_task(self, task: str) -> Optional[str]:
        """
        Execute a task using the Groq API
        
        Args:
            task (str): The task to be executed
            
        Returns:
            Optional[str]: The response from the API or None if failed
        """
        try:
            response = self.client.chat.completions.create(
                model="moonshotai/kimi-k2-instruct",
                messages=self.messages + [{"role": "user", "content": task}],
                max_tokens=1500,
                temperature=0.7,
                top_p=0.9
            )
            
            result = response.choices[0].message.content.strip()
            return result
            
        except Exception as e:
            return None
    
    def extract_code_from_response(self, response: str) -> Optional[str]:
        """
        Extract Python code from the API response
        
        Args:
            response (str): The response containing Python code
            
        Returns:
            Optional[str]: Extracted Python code or None if not found
        """
        if not response:
            return None
            
        # Multiple patterns to catch different code block formats
        patterns = [
            r'```python\n(.*?)\n```',
            r'```\n(.*?)\n```',
            r'`([^`]+)`'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, response, re.DOTALL)
            if matches:
                code = matches[0].strip()
                return code
                
        return None
    
    def validate_code_safety(self, code: str) -> bool:
        """
        Basic safety validation for code execution
        
        Args:
            code (str): Python code to validate
            
        Returns:
            bool: True if code appears safe, False otherwise
        """
        dangerous_patterns = [
            r'rm\s+-rf',
            r'del\s+/[fFsS]',
            r'format\s+[cC]:',
            r'__import__\s*\(\s*["\']os["\']',
            r'eval\s*\(',
            r'exec\s*\(',
            r'open\s*\([^)]*["\'][wWaA]'
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                return False
                
        return True
    
    def execute_python_code(self, code: str) -> str:
        """
        Safely execute Python code with error handling
        
        Args:
            code (str): Python code to execute
            
        Returns:
            str: Execution result message
        """
        if not code:
            return ""
            
        if not self.validate_code_safety(code):
            return ""
            
        try:
            # Create a controlled execution environment
            exec_globals = {
                '__builtins__': __builtins__,
                'print': print,
                # Add safe modules
                'os': os,
                'time': __import__('time'),
                'webbrowser': __import__('webbrowser'),
                'psutil': __import__('psutil') if self._module_available('psutil') else None
            }
            
            # Execute the code
            exec(code, exec_globals)
            
            return ""
            
        except ImportError as e:
            return ""
            
        except Exception as e:
            return ""
    
    def _module_available(self, module_name: str) -> bool:
        """Check if a module is available for import"""
        try:
            __import__(module_name)
            return True
        except ImportError:
            return False
    
    def run_task(self, task: str) -> str:
        """
        Complete task execution pipeline
        
        Args:
            task (str): Task description
            
        Returns:
            str: Final execution result
        """
        if not task.strip():
            return ""
            
        # Step 1: Get AI response
        response = self.execute_task(task)
        if not response:
            return ""
            
        # Step 2: Extract code
        code = self.extract_code_from_response(response)
        if not code:
            return ""
            
        # Step 3: Execute code silently
        self.execute_python_code(code)
        return ""

    def interactive_mode(self, prompt):
        """Run Falcon AI in interactive mode"""

        task = prompt
        self.run_task(task)

def task_executor(prompt: str) -> str:
    """
    Task executor function for Falcon AI
    
    Args:
        prompt (str): User input prompt
        
    Returns:
        str: Execution result
    """
    falcon_ai = FalconAI()
    return falcon_ai.run_task(prompt) if prompt.strip() else ""

if __name__ == "__main__":
    while True:
        user_input = input("Enter your task: ")
        result = task_executor(user_input)