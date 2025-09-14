import pyautogui
import google.generativeai as genai
import PIL.Image

def get_next_gui_action(user_prompt: str, screenshot_file: str) -> str:
    """
    Analyzes a screenshot with a user prompt to determine the next GUI action.

    Args:
        user_prompt (str): The user's original request.
        screenshot_file (str): The path to the screenshot image.

    Returns:
        str: A string representing the next action to take (e.g., "click(100, 200)").
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    You are a helpful AI assistant that controls a computer.
    You are looking at a screenshot of the user's screen.
    The user's overall goal is: "{user_prompt}"

    Based on the screenshot, what is the single next action you should take to progress towards the goal?

    Your available actions are:
    1. click(x, y): Click a specific coordinate on the screen.
    2. type("text to type"): Type out a string of text. Use this for input fields.
    3. press("key"): Press a special key on the keyboard (e.g., "enter", "win", "esc").
    4. done(): Use this when the user's goal has been fully achieved.

    Analyze the screenshot and return ONLY the single command for the next action.
    Do not provide any explanation or conversational text.
    For example, if you need to click on a button at coordinates x=123, y=456, you should return: click(123, 456)
    """
    
    try:
        img = PIL.Image.open(screenshot_file)
        response = model.generate_content([prompt, img])
        return response.text.strip()
    except Exception as e:
        return f"Error analyzing screenshot: {e}"

def execute_gui_action(action_string: str) -> bool:
    """
    Parses an action string from the LLM and executes it using pyautogui.

    Args:
        action_string (str): The command from the LLM (e.g., "click(100, 200)").

    Returns:
        bool: True if the action loop should continue, False if the action was "done()".
    """
    action_string = action_string.strip()
    print(f"Executing action: {action_string}")

    try:
        if action_string.lower().startswith("click"):
            # A bit of parsing to extract coordinates. This can be made more robust.
            coords_str = action_string[action_string.find("(")+1:action_string.find(")")]
            x, y = map(int, coords_str.split(','))
            pyautogui.click(x, y)
        elif action_string.lower().startswith("type"):
            text_to_type = action_string[action_string.find("(")+1:action_string.find(")")].strip('"\'')
            pyautogui.typewrite(text_to_type, interval=0.1)
        elif action_string.lower().startswith("press"):
            key_to_press = action_string[action_string.find("(")+1:action_string.find(")")].strip('"\'')
            pyautogui.press(key_to_press)
        elif action_string.lower() == "done()":
            print("Task complete.")
            return False # Signal to stop the loop
        else:
            print(f"Unknown action: {action_string}")
    
    except Exception as e:
        print(f"Error executing action '{action_string}': {e}")

    return True # Signal to continue the loop


def take_screenshot(filename: str = "screenshot.png") -> str:
    """
    Takes a screenshot of the entire screen and saves it to a file.
    
    Args:
        filename (str): The name of the file to save the screenshot to.
        
    Returns:
        str: The path to the saved screenshot file.
    """
    try:
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        print(f"Screenshot saved to {filename}")
        return filename
    except Exception as e:
        print(f"Error taking screenshot: {e}")
        return None 