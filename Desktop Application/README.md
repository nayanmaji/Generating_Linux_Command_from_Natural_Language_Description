**How to Run the Application**
This section provides detailed instructions for setting up and running the "Linux Command Generator."
**Prerequisites**
Ensure the following software components are installed on your system:
1. Python 3.8+
2. Required Python Libraries:
`tkinter` (usually bundled with Python).
`requests`
`json` (standard library).
`threading` (standard library).
`os` (standard library).
`datetime` (standard library).
`configparser` (standard library).
3.  AI API Keys:
Obtain API keys from your chosen AI providers (Anthropic for Claude, Google Cloud Console for Gemini, Perplexity AI, OpenAI platform). These are essential for the application's core functionality.

**Setup Procedure**
Follow these steps to prepare the application for execution:
Step 1: Save the Source Code
Create a new file named `linux_command_generator.py` (or any other `.py` extension) on your computer.
Copy the entire provided Python code into this file and save it.
Step 2: Install Python Dependencies
Open your terminal or command prompt.
Navigate to the directory where you saved `linux_command_generator.py` using the `cd` command.
Step 3: Configure AI API Keys
This is a critical step for the application to function correctly.
Open the `linux_command_generator.py` file in a text editor (e.g., Visual Studio Code, Sublime Text, Notepad++).
Locate the `self.api_keys` dictionary within the `__init__` method of the `LinuxCommandGenerator` class. It will look like this:
self.api_keys = {
'claude': 'YOUR_CLAUDE_API_KEY_HERE',
'gemini': ''YOUR_GEMINI_API_KEY_HERE'',
'perplexity': 'YOUR_PERPLEXITY_API_KEY_HERE',
'openai': 'YOUR_OPENAI_API_KEY_HERE'
}
For each AI service you wish to use, replace the placeholder string (e.g., `'YOUR_CLAUDE_API_KEY_HERE'`) with your actual API key.

**Execution Procedure**
After completing the setup:
1.  Open Terminal / Command Prompt : Navigate to the directory containing `linux_command_generator.py`.
2.  Run the Script: Execute the Python script using:
python linux_command_generator.py
    	The desktop application window will appear.
    
**Execution Procedure (Using PyInstaller for Application)**
The user specified `pyinstaller --onefile --noconsole linux_command_generator.py` to create a standalone executable.
1.  Install PyInstaller: pip install pyinstaller
2.  Build the Executable: Navigate to the directory containing `linux_command_generator.py` in your terminal and execute the command:
pyinstaller --onefile --noconsole linux_command_generator.py
       `--onefile`: Packages the entire application into a single executable file.
       `--noconsole`: Prevents a console window from appearing when the GUI application runs (recommended for desktop apps).
3.  Locate the Executable: After PyInstaller completes, a `dist` folder will be created in the same directory. Inside `dist`, you will find the standalone executable (e.g., `linux_command_generator` on Linux/macOS, `linux_command_generator.exe` on Windows).
4.  Run the Executable: Double-click the executable file in your file explorer, or run it from the terminal:
./dist/linux_command_generator  # On Linux/macOS
.\dist\linux_command_generator.exe # On Windows (from PowerShell/CMD)

**How to Use the Application**
i.	Describe Your Task: In the large text area labeled "Describe your Linux task:", type a clear and concise description of the Linux command you need. For example: "List all files in the current directory, including hidden ones, and show their permissions."

ii.	Select AI Provider: Choose your preferred AI model from the "Select AI Provider:" dropdown menu (e.g., "Gemini," "Claude").

iii.	Generate Command: Click the "Generate Command" button. The application will contact the selected AI service, and the generated command will appear in the "Generated Command:" area. A loading animation will be displayed during this process.

iv.	Copy Command: Click the "Copy" button to copy the generated command to your clipboard. You can then paste it directly into your terminal.

v.	Save Command: Click the "Save" button to save the generated command to a `.sh` or `.txt` file on your system.

vi.	View History: Click the "History" button to open a new window showing a list of your past generated commands and their corresponding prompts.

