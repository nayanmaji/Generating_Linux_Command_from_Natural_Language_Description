Natural Language to Linux Command – Android Application
An Android app that allows users to interact with multiple large language models (LLMs) including ChatGPT, Claude, and Gemini. Enter a natural language prompt and get an intelligent command or response instantly.

🚀 How to Run the Application
✅ Prerequisites
Before running the app, ensure the following are installed or set up:

Android Studio
Download and install the latest version from the official website.

Android Device or Emulator
Choose one of the following:

Physical Device: Enable USB Debugging under Developer Options.

Android Virtual Device (AVD): Create and run an emulator in Android Studio.

API Keys
The application uses external LLM APIs. Get valid API keys from:

OpenAI

Anthropic

Google AI Studio or Google Cloud Console

🔧 Setup Instructions
Clone or Download the Repository

bash
Copy
Edit
git clone <repository_url>
Or download the ZIP and extract it.

Open the Project in Android Studio

Open Android Studio.

Choose Open from the welcome screen or go to File > Open.

Navigate to the project root (where build.gradle is located).

Click OK/Open.

Configure API Keys

Open the relevant constants or configuration file (e.g., Config.java, strings.xml, or similar).

Replace placeholder keys with your valid OpenAI, Anthropic, and Gemini API keys.

Sync Gradle

After editing build.gradle, click Sync Now when prompted.

Or manually run: File > Sync Project with Gradle Files.

Build the Project

Go to Build > Make Project to compile the code and resolve dependencies.

Run the App

Click the Run ▶️ icon or go to Run > Run 'app'.

Select your emulator or connected device.

The app will build and launch.

📱 How to Use the Application
✏️ Enter Your Prompt
Use the text input field at the top labeled "Enter your prompt...".

Type a command, question, or query for the AI.

🤖 Select an AI Model
Tap the dropdown to choose:

ChatGPT (GPT-4)

Claude (Anthropic)

Gemini (Google)

⚡ Generate a Response
Tap the Generate button to submit your prompt.

The app will query the selected AI model and display the response.

🧰 Response Actions
Copy Response:
Tap the clipboard icon to copy the AI-generated text.
A toast message confirms: "Response copied to clipboard."

Share Response:
Tap the share icon to open your device's sharing menu and send the response via other apps (e.g., WhatsApp, Email, Notes).
