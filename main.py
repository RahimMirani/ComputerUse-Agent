import subprocess

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
    # For Windows, 'dir' lists directory contents. For macOS/Linux, it's 'ls'.
    # You can change this to any command you like.
    while True:
        user_input = input("Enter a command:")
        if user_input == "exit" or user_input == "quit":
            break
        output = execute_command(user_input)
        print(output)
        
        


