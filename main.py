import subprocess
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def get_command_from_llm(user_input: str) -> str:
    """
    Uses the Gemini LLM to translate natural language into a shell command.
    """
    # We can improve this prompt over time.
    prompt = f"""
    You are an expert in command-line interfaces. A user will provide a task in natural language.
    Your sole responsibility is to return a single, executable shell command that accomplishes the task.
    The user is on the following operating system: {os.name}.
    Do not provide any explanation, clarification, or conversational text.
    Only return the shell command.

    User's request: "{user_input}"
    Command:
    """
    
    try:
        response = model.generate_content(prompt)
        # We'll do more robust parsing later if needed.
        command = response.text.strip()
        return command
    except Exception as e:
        return f"Error communicating with the LLM: {e}"


## Function to execute and run commands in the terminal/shell
def execute_command(command: str) -> str:
    """
    Executes a shell command and returns its output.
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error executing command: {e}\n{e.stderr}"

if __name__ == "__main__":
    while True:
        user_input = input("Hello, how can I help you today? ")
        if user_input.lower() in ["exit", "quit"]:
            break
        
        # Get the command from the LLM
        command_to_execute = get_command_from_llm(user_input)
        print(f"Executing: {command_to_execute}")

        # Execute the command
        output = execute_command(command_to_execute)
        print(output)




