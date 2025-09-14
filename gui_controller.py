import pyautogui

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