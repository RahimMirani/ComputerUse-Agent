import subprocess
import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
import time
from gui_controller import take_screenshot, get_next_gui_action, execute_gui_action

# Load environment variables from .env file
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def get_agent_action(user_input: str) -> dict:
    """
    Uses the Gemini LLM to determine the user's intent and required action.
    """
    prompt = f"""
    You are a helpful AI assistant that controls a computer.
    Based on the user's request, determine whether the task requires a 'SHELL' command or a 'GUI' action.

    The user is on the following operating system: {os.name}.

    Respond with a JSON object containing two keys:
    1. "type": Must be either "SHELL" or "GUI".
    2. "command": 
       - If the type is "SHELL", this should be the executable shell command.
       - If the type is "GUI", this should be a short, one-sentence description of the task to perform on the GUI.

    Do not provide any explanation or conversational text. Only return the JSON object.

    User's request: "{user_input}"
    """
    
    try:
        response = model.generate_content(prompt)
        # Clean up the response to ensure it's valid JSON
        json_str = response.text.strip().replace('```json', '').replace('```', '').strip()
        action = json.loads(json_str)
        return action
    except Exception as e:
        return {"type": "ERROR", "command": f"Error parsing LLM response: {e}"}


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
        
        # Get the structured action from the LLM
        action = get_agent_action(user_input)

        if action.get("type") == "SHELL":
            command_to_execute = action.get("command", "")
            print(f"Executing shell command: {command_to_execute}")
            output = execute_command(command_to_execute)
            print(output)
        elif action.get("type") == "GUI":
            gui_task = action.get("command", "")
            print(f"Executing GUI task: {gui_task}")
            
            # Start the Observe, Think, Act loop for GUI tasks
            while True:
                time.sleep(1) # Wait a moment for the screen to settle
                screenshot_file = take_screenshot()
                if not screenshot_file:
                    print("Failed to take screenshot. Aborting GUI task.")
                    break
                
                # Think: What is the next action?
                next_action_str = get_next_gui_action(gui_task, screenshot_file)
                
                # Act: Execute the action
                should_continue = execute_gui_action(next_action_str)
                if not should_continue:
                    break # The LLM signaled that the task is done
            
        elif action.get("type") == "ERROR":
            print(f"Error: {action.get('command')}")
        else:
            print(f"Unknown action type: {action.get('type')}")




