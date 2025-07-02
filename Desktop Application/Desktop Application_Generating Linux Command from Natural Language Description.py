import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import requests
import json
import threading
import os
from datetime import datetime
import configparser

class LinuxCommandGenerator:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_colors()
        self.animate_loading = False
        
        # Configuration
        self.config = configparser.ConfigParser()
        self.config_file = 'config.ini'
        self.load_config()
        
        # API Keys - Replace with your actual keys
        self.api_keys = {
            'claude': 'YOUR_CLAUDE_API_KEY_HERE',
            'gemini': 'AIzaSyBt7aNiu4y6PuVusEyiev1sqFQUnoJMWQk',
            'perplexity': 'YOUR_PERPLEXITY_API_KEY_HERE',
            'openai': 'YOUR_OPENAI_API_KEY_HERE'
        }
        
        self.api_configs = {
            'Claude': {
                'url': 'https://api.anthropic.com/v1/messages',
                'headers_template': {
                    'Content-Type': 'application/json',
                    'x-api-key': '',
                    'anthropic-version': '2023-06-01'
                },
                'model': 'claude-3-sonnet-20240229'
            },
            'Gemini': {
                'url': 'https://generativelanguage.googleapis.com/v1/',
                'headers_template': {
                    'Content-Type': 'application/json'
                },
                'model': 'models/gemini-2.0-flash'
            },
            'Perplexity': {
                'url': 'https://api.perplexity.ai/chat/completions',
                'headers_template': {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer '
                },
                'model': 'llama-3.1-sonar-small-128k-online'
            },
            'OpenAI': {
                'url': 'https://api.openai.com/v1/chat/completions',
                'headers_template': {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer '
                },
                'model': 'gpt-3.5-turbo'
            }
        }
        
        self.command_history = []
        self.create_modern_ui()
        self.load_history()
        self.start_background_animation()
    
    def setup_window(self):
        """Configure the main window with modern styling"""
        self.root.title("🐧 Modern Linux Command Generator")
        self.root.geometry("1000x800")
        self.root.minsize(800, 600)
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1000 // 2)
        y = (self.root.winfo_screenheight() // 2) - (800 // 2)
        self.root.geometry(f"1000x800+{x}+{y}")
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
    
    def setup_colors(self):
        """Define the color scheme"""
        self.colors = {
            'bg_primary': '#0f1419',      # Dark blue-black
            'bg_secondary': '#1a1f29',    # Slightly lighter
            'bg_tertiary': '#252a35',     # Card background
            'accent_primary': '#00d4aa',  # Teal accent
            'accent_secondary': '#ff6b6b', # Red accent
            'text_primary': '#ffffff',    # White text
            'text_secondary': '#b8c5d1',  # Light gray text
            'text_accent': '#00ff88',     # Green terminal text
            'border': '#3d4752',          # Border color
            'gradient_start': '#667eea',  # Gradient colors
            'gradient_end': '#764ba2'
        }
        
        self.root.configure(bg=self.colors['bg_primary'])
    
    def load_config(self):
        """Load configuration from file"""
        try:
            self.config.read(self.config_file)
            if not self.config.has_section('API_KEYS'):
                self.config.add_section('API_KEYS')
        except:
            self.config.add_section('API_KEYS')
    
    def create_modern_ui(self):
        """Create the modern UI with enhanced visuals"""
        # Main container with gradient effect
        self.main_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header section
        self.create_header()
        
        # API selection section
        self.create_api_section()
        
        # Input section
        self.create_input_section()
        
        # Control buttons
        self.create_control_section()
        
        # Output section
        self.create_output_section()
        
        # Status and footer
        self.create_footer()
    
    def create_header(self):
        """Create animated header with logo and title"""
        header_frame = tk.Frame(self.main_container, bg=self.colors['bg_primary'])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Animated title
        self.title_label = tk.Label(
            header_frame,
            text="🐧 LINUX COMMAND GENERATOR",
            font=('JetBrains Mono', 24, 'bold'),
            fg=self.colors['accent_primary'],
            bg=self.colors['bg_primary']
        )
        self.title_label.pack()
        
        # Subtitle with animation
        self.subtitle_label = tk.Label(
            header_frame,
            text="✨ Generate powerful Linux commands with AI assistance ✨",
            font=('Arial', 12, 'italic'),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_primary']
        )
        self.subtitle_label.pack(pady=(5, 0))
        
        # Animated separator
        separator = tk.Frame(header_frame, height=2, bg=self.colors['accent_primary'])
        separator.pack(fill=tk.X, pady=10)
    
    def create_api_section(self):
        """Create modern API selection section"""
        api_frame = tk.Frame(
            self.main_container,
            bg=self.colors['bg_tertiary'],
            relief=tk.FLAT,
            bd=0
        )
        api_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Add rounded corners effect with padding
        inner_frame = tk.Frame(api_frame, bg=self.colors['bg_tertiary'])
        inner_frame.pack(fill=tk.X, padx=20, pady=15)
        
        # API selection label
        api_label = tk.Label(
            inner_frame,
            text="🤖 Select AI Provider:",
            font=('Arial', 12, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_tertiary']
        )
        api_label.pack(side=tk.LEFT)
        
        # Modern combobox
        self.api_var = tk.StringVar(value='Gemini')
        self.api_combo = ttk.Combobox(
            inner_frame,
            textvariable=self.api_var,
            values=list(self.api_configs.keys()),
            state='readonly',
            width=15,
            font=('Arial', 11)
        )
        self.api_combo.pack(side=tk.LEFT, padx=(15, 0))
        
        # API status indicator
        self.api_status = tk.Label(
            inner_frame,
            text="● Ready",
            font=('Arial', 10),
            fg=self.colors['accent_primary'],
            bg=self.colors['bg_tertiary']
        )
        self.api_status.pack(side=tk.RIGHT)
    
    def create_input_section(self):
        """Create enhanced input section"""
        input_frame = tk.Frame(
            self.main_container,
            bg=self.colors['bg_tertiary'],
            relief=tk.FLAT
        )
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Input header
        input_header = tk.Frame(input_frame, bg=self.colors['bg_tertiary'])
        input_header.pack(fill=tk.X, padx=20, pady=(15, 10))
        
        tk.Label(
            input_header,
            text="💬 Describe your Linux task:",
            font=('Arial', 12, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_tertiary']
        ).pack(side=tk.LEFT)
        
        # Character counter
        self.char_counter = tk.Label(
            input_header,
            text="0/500",
            font=('Arial', 9),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_tertiary']
        )
        self.char_counter.pack(side=tk.RIGHT)
        
        # Enhanced text input with placeholder
        input_container = tk.Frame(input_frame, bg=self.colors['bg_tertiary'])
        input_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        self.input_text = scrolledtext.ScrolledText(
            input_container,
            height=6,
            font=('Consolas', 11),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            relief=tk.FLAT,
            bd=0,
            insertbackground=self.colors['accent_primary'],
            selectbackground=self.colors['accent_primary'],
            selectforeground=self.colors['bg_primary']
        )
        self.input_text.pack(fill=tk.BOTH, expand=True)
        
        # Bind events for character counter
        self.input_text.bind('<KeyRelease>', self.update_char_counter)
        
        # Add placeholder text
        self.add_placeholder()
    
    def add_placeholder(self):
        """Add placeholder text to input field"""
        placeholder = "Example: List all files in the current directory recursively, show hidden files, and sort by modification time..."
        self.input_text.insert('1.0', placeholder)
        self.input_text.config(fg=self.colors['text_secondary'])
        
        def on_focus_in(event):
            if self.input_text.get('1.0', 'end-1c') == placeholder:
                self.input_text.delete('1.0', tk.END)
                self.input_text.config(fg=self.colors['text_primary'])
        
        def on_focus_out(event):
            if not self.input_text.get('1.0', 'end-1c'):
                self.input_text.insert('1.0', placeholder)
                self.input_text.config(fg=self.colors['text_secondary'])
        
        self.input_text.bind('<FocusIn>', on_focus_in)
        self.input_text.bind('<FocusOut>', on_focus_out)
    
    def update_char_counter(self, event=None):
        """Update character counter"""
        content = self.input_text.get('1.0', 'end-1c')
        char_count = len(content)
        self.char_counter.config(text=f"{char_count}/500")
        
        # Change color based on length
        if char_count > 450:
            self.char_counter.config(fg=self.colors['accent_secondary'])
        elif char_count > 300:
            self.char_counter.config(fg='#ffa500')
        else:
            self.char_counter.config(fg=self.colors['text_secondary'])
    
    def create_control_section(self):
        """Create modern control buttons"""
        control_frame = tk.Frame(self.main_container, bg=self.colors['bg_primary'])
        control_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Generate button with gradient effect
        self.generate_btn = tk.Button(
            control_frame,
            text="🚀 Generate Command",
            command=self.generate_command,
            bg=self.colors['accent_primary'],
            fg=self.colors['bg_primary'],
            font=('Arial', 12, 'bold'),
            relief=tk.FLAT,
            padx=30,
            pady=12,
            cursor='hand2'
        )
        self.generate_btn.pack(side=tk.LEFT)
        
        # Add hover effects
        self.add_modern_hover_effects(self.generate_btn)
        
        # Additional control buttons
        btn_frame = tk.Frame(control_frame, bg=self.colors['bg_primary'])
        btn_frame.pack(side=tk.RIGHT)
        
        self.copy_btn = tk.Button(
            btn_frame,
            text="📋 Copy",
            command=self.copy_command,
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_primary'],
            font=('Arial', 10),
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor='hand2'
        )
        self.copy_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.save_btn = tk.Button(
            btn_frame,
            text="💾 Save",
            command=self.save_command,
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_primary'],
            font=('Arial', 10),
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor='hand2'
        )
        self.save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.history_btn = tk.Button(
            btn_frame,
            text="📚 History",
            command=self.show_history,
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_primary'],
            font=('Arial', 10),
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor='hand2'
        )
        self.history_btn.pack(side=tk.LEFT)
        
        # Add hover effects to all buttons
        for btn in [self.copy_btn, self.save_btn, self.history_btn]:
            self.add_secondary_hover_effects(btn)
    
    def create_output_section(self):
        """Create enhanced output section"""
        output_frame = tk.Frame(
            self.main_container,
            bg=self.colors['bg_tertiary'],
            relief=tk.FLAT
        )
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        # Output header
        output_header = tk.Frame(output_frame, bg=self.colors['bg_tertiary'])
        output_header.pack(fill=tk.X, padx=20, pady=(15, 10))
        
        tk.Label(
            output_header,
            text="⚡ Generated Command:",
            font=('Arial', 12, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_tertiary']
        ).pack(side=tk.LEFT)
        
        # Output container with terminal styling
        output_container = tk.Frame(output_frame, bg=self.colors['bg_secondary'])
        output_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        # Terminal header
        terminal_header = tk.Frame(output_container, bg=self.colors['bg_primary'], height=30)
        terminal_header.pack(fill=tk.X)
        terminal_header.pack_propagate(False)
        
        # Terminal buttons (aesthetic)
        btn_container = tk.Frame(terminal_header, bg=self.colors['bg_primary'])
        btn_container.pack(side=tk.LEFT, padx=10, pady=8)
        
        for color in ['#ff5f56', '#ffbd2e', '#27ca3f']:
            btn = tk.Label(btn_container, text='●', fg=color, bg=self.colors['bg_primary'], font=('Arial', 8))
            btn.pack(side=tk.LEFT, padx=2)
        
        tk.Label(
            terminal_header,
            text="terminal",
            font=('Arial', 9),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_primary']
        ).pack(pady=8)
        
        # Output text area
        self.output_text = scrolledtext.ScrolledText(
            output_container,
            height=8,
            font=('JetBrains Mono', 11),
            bg=self.colors['bg_primary'],
            fg=self.colors['text_accent'],
            relief=tk.FLAT,
            bd=0,
            insertbackground=self.colors['text_accent'],
            selectbackground=self.colors['accent_primary'],
            selectforeground=self.colors['bg_primary']
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
    
    def create_footer(self):
        """Create status bar and footer"""
        footer_frame = tk.Frame(self.main_container, bg=self.colors['bg_primary'])
        footer_frame.pack(fill=tk.X, pady=(15, 0))
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready to generate commands")
        status_bar = tk.Label(
            footer_frame,
            textvariable=self.status_var,
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary'],
            relief=tk.FLAT,
            anchor=tk.W,
            font=('Arial', 9),
            padx=10,
            pady=5
        )
        status_bar.pack(fill=tk.X)
    
    def add_modern_hover_effects(self, button):
        """Add modern hover effects to primary button"""
        original_bg = button['bg']
        
        def on_enter(e):
            button.config(bg='#00b894', font=('Arial', 12, 'bold'))
            
        def on_leave(e):
            button.config(bg=original_bg, font=('Arial', 12, 'bold'))
            
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    def add_secondary_hover_effects(self, button):
        """Add hover effects to secondary buttons"""
        def on_enter(e):
            button.config(bg=self.colors['border'])
            
        def on_leave(e):
            button.config(bg=self.colors['bg_tertiary'])
            
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    def start_background_animation(self):
        """Start subtle background animations"""
        self.animate_title()
    
    def animate_title(self):
        """Animate the title with color transitions"""
        colors = [self.colors['accent_primary'], '#00ff88', '#667eea', self.colors['accent_primary']]
        current_color = 0
        
        def change_color():
            nonlocal current_color
            self.title_label.config(fg=colors[current_color])
            current_color = (current_color + 1) % len(colors)
            self.root.after(3000, change_color)
        
        change_color()
    
    def generate_command(self):
        """Generate Linux command using selected API"""
        prompt = self.input_text.get(1.0, tk.END).strip()
        if not prompt or prompt.startswith("Example:"):
            messagebox.showwarning("Warning", "Please enter a description of your Linux task!")
            return
        
        selected_api = self.api_var.get()
        api_key = self.api_keys.get(selected_api.lower())
        
        if not api_key or api_key.startswith("YOUR"):
            messagebox.showerror(
                "API Key Required", 
                f"Please configure your {selected_api} API key in the source code!\n\n"
                f"Replace 'YOUR_{selected_api.upper()}_API_KEY_HERE' with your actual API key."
            )
            return
        
        # Disable button and start animation
        self.generate_btn.config(state='disabled', text='🔄 Generating...')
        self.status_var.set(f"Generating command using {selected_api}...")
        self.output_text.delete(1.0, tk.END)
        self.api_status.config(text="● Processing", fg='#ffa500')
        
        # Start loading animation
        self.animate_loading = True
        threading.Thread(target=self.loading_animation, daemon=True).start()
        
        # Start API call in separate thread
        threading.Thread(target=self.call_api, args=(prompt, selected_api), daemon=True).start()
    
    def loading_animation(self):
        """Show loading animation in output"""
        animation_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        i = 0
        
        while self.animate_loading:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"{animation_chars[i % len(animation_chars)]} Analyzing your request and generating command...")
            self.output_text.update()
            i += 1
            
            # Use threading-safe method
            import time
            time.sleep(0.1)
    
    def call_api(self, prompt, api_name):
        """Make API call to generate command"""
        try:
            api_key = self.api_keys.get(api_name.lower())
            
            # Create enhanced prompt for Linux command generation
            enhanced_prompt = f"""You are a Linux command expert. Generate ONLY the Linux command(s) needed for this task. Do not include explanations or additional text.

Task: {prompt}

Respond with only the command(s), one per line if multiple commands are needed."""
            
            if api_name == 'Claude':
                response = self.call_claude_api(enhanced_prompt, api_key)
            elif api_name == 'Gemini':
                response = self.call_gemini_api(enhanced_prompt, api_key)
            elif api_name == 'Perplexity':
                response = self.call_perplexity_api(enhanced_prompt, api_key)
            elif api_name == 'OpenAI':
                response = self.call_openai_api(enhanced_prompt, api_key)
            else:
                response = "API not implemented yet."
            
            # Update UI in main thread
            self.root.after(0, self.update_output, response, prompt, api_name)
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.root.after(0, self.update_output, error_msg, prompt, api_name)
    
    def call_claude_api(self, prompt, api_key):
        """Call Claude API"""
        config = self.api_configs['Claude']
        headers = config['headers_template'].copy()
        headers['x-api-key'] = api_key
        
        payload = {
            "model": config['model'],
            "max_tokens": 1024,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        response = requests.post(config['url'], headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result['content'][0]['text']
    
    def call_gemini_api(self, prompt, api_key):
        """Call Gemini API"""
        config = self.api_configs['Gemini']
        url = f"{config['url']}{config['model']}:generateContent?key={api_key}"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }]
        }
        
        response = requests.post(url, headers=config['headers_template'], json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text']
    
    def call_perplexity_api(self, prompt, api_key):
        """Call Perplexity API"""
        config = self.api_configs['Perplexity']
        headers = config['headers_template'].copy()
        headers['Authorization'] = f"Bearer {api_key}"
        
        payload = {
            "model": config['model'],
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 1024
        }
        
        response = requests.post(config['url'], headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result['choices'][0]['message']['content']
    
    def call_openai_api(self, prompt, api_key):
        """Call OpenAI API"""
        config = self.api_configs['OpenAI']
        headers = config['headers_template'].copy()
        headers['Authorization'] = f"Bearer {api_key}"
        
        payload = {
            "model": config['model'],
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 1024,
            "temperature": 0.7
        }
        
        response = requests.post(config['url'], headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result['choices'][0]['message']['content']
    
    def update_output(self, response, original_prompt, api_name):
        """Update output with generated command"""
        self.animate_loading = False
        self.output_text.delete(1.0, tk.END)
        
        # Typewriter effect
        def type_text(text, index=0):
            if index < len(text):
                self.output_text.insert(tk.END, text[index])
                self.output_text.see(tk.END)
                self.root.after(20, lambda: type_text(text, index + 1))
            else:
                # Animation complete
                self.generate_btn.config(state='normal', text='🚀 Generate Command')
                self.status_var.set(f"Command generated successfully using {api_name}")
                self.api_status.config(text="● Ready", fg=self.colors['accent_primary'])
                
                # Save to history
                self.save_to_history(original_prompt, response, api_name)
        
        type_text(response)
    
    def copy_command(self):
        """Copy generated command to clipboard"""
        command = self.output_text.get(1.0, tk.END).strip()
        if command:
            self.root.clipboard_clear()
            self.root.clipboard_append(command)
            self.status_var.set("Command copied to clipboard!")
            
            # Visual feedback
            original_text = self.copy_btn['text']
            self.copy_btn.config(text='✅ Copied!')
            self.root.after(2000, lambda: self.copy_btn.config(text=original_text))
        else:
            messagebox.showinfo("Info", "No command to copy!")
    
    def save_command(self):
        """Save command to file"""
        command = self.output_text.get(1.0, tk.END).strip()
        if command:
            filename = filedialog.asksaveasfilename(
                defaultextension=".sh",
                filetypes=[("Shell scripts", "*.sh"), ("Text files", "*.txt"), ("All files", "*.*")]
            )
            if filename:
                with open(filename, 'w') as f:
                    f.write(command)
                self.status_var.set(f"Command saved to {filename}")
        else:
            messagebox.showinfo("Info", "No command to save!")
    
    def show_history(self):
        """Show command history in a new window"""
        if not self.command_history:
            messagebox.showinfo("History", "No command history available!")
            return
        
        history_window = tk.Toplevel(self.root)
        history_window.title("Command History")
        history_window.geometry("800x600")
        history_window.configure(bg=self.colors['bg_primary'])
        
        # History list
        history_frame = tk.Frame(history_window, bg=self.colors['bg_primary'])
        history_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(
            history_frame,
            text="📚 Command History",
            font=('Arial', 16, 'bold'),
            fg=self.colors['accent_primary'],
            bg=self.colors['bg_primary']
        ).pack(pady=(0, 20))
        
        history_text = scrolledtext.ScrolledText(
            history_frame,
            font=('Consolas', 10),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            relief=tk.FLAT
        )
        history_text.pack(fill=tk.BOTH, expand=True)
        
        for i, entry in enumerate(self.command_history[-20:], 1):  # Show last 20 entries
            history_text.insert(tk.END, f"{i}. Prompt: {entry['prompt'][:100]}...\n")
            history_text.insert(tk.END, f"   Command: {entry['command']}\n")
            history_text.insert(tk.END, f"   API: {entry['api']} | Time: {entry['timestamp']}\n\n")

    def save_to_history(self, prompt, command, api_name):
        """Save command to history"""
        entry = {
            'prompt': prompt,
            'command': command,
            'api': api_name,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.command_history.append(entry)
        
        # Keep only last 100 entries
        if len(self.command_history) > 100:
            self.command_history = self.command_history[-100:]
    
    def load_history(self):
        """Load command history from file"""
        try:
            with open('command_history.json', 'r') as f:
                self.command_history = json.load(f)
        except:
            self.command_history = []
    
    def save_history(self):
        """Save command history to file"""
        try:
            with open('command_history.json', 'w') as f:
                json.dump(self.command_history, f, indent=2)
        except Exception as e:
            print(f"Error saving history: {e}")

def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = LinuxCommandGenerator(root)
    
    def on_closing():
        """Handle application closing"""
        app.save_history()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start the application
    print("🚀 Starting Modern Linux Command Generator...")
    print("📝 Note: Replace API keys in the source code with your actual keys")
    print("🔧 Supported APIs: Claude, Gemini, Perplexity, OpenAI")
    
    root.mainloop()

if __name__ == "__main__":
    main()