import tkinter as tk
from tkinter import scrolledtext, Canvas, Frame, Label, StringVar, filedialog
from PIL import Image, ImageTk
import speech_recognition as sr
import openai
from gtts import gTTS
import os
import asyncio
import threading
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize the recognizer
recognizer = sr.Recognizer()

exit_program = False
conversation_thread = None  # Store the conversation thread

# Initialize conversation history with the initial AI introduction
conversation_history = [{"role": "assistant", "content": "Hi, I am AI. How can I assist you."}]

# Language options for the conversation
languages = {
    "English": "en",
    "Chinese": "zh",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
}

# Asynchronous function to listen for speech
async def listen_for_speech_async(language):
    with sr.Microphone() as source:
        print("Listening for speech...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language=language)
        print("You said: " + text)
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio.")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return ""

# Asynchronous function to handle AI conversation
async def ai_conversation_async(user_message):
    # Append the user's message to the conversation history
    conversation_history.append({"role": "user", "content": user_message})

    # Join the conversation history into a single list
    messages = [
        {"role": item["role"], "content": item["content"]} for item in conversation_history
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    ai_response = response["choices"][0]["message"]["content"]

    # Append the AI's response to the conversation history
    conversation_history.append({"role": "assistant", "content": ai_response})

    # Save the updated conversation history
    save_conversation_history()

    return ai_response

# Asynchronous function to speak text
async def speak_text_async(text, language):
    tts = gTTS(text=text, lang=language)
    tts.save("response.mp3")
    os.system("afplay response.mp3")  # On macOS, use 'afplay' to play audio

# Function to view conversation history
def view_history():
    history_window = tk.Toplevel(root)
    history_window.title("Conversation History")

    history_text = scrolledtext.ScrolledText(history_window, wrap=tk.WORD)
    history_text.pack(fill=tk.BOTH, expand=True)
    history_text.config(state=tk.NORMAL)  # Enable text widget for editing

    # Load and display the conversation history
    load_conversation_history()
    for entry in conversation_history:
        history_text.insert(tk.END, f"{entry['role']}: {entry['content']}\n")

    history_text.config(state=tk.DISABLED)  # Disable text widget for editing

    # Save History As button
    save_as_button = tk.Button(history_window, text="Save History As", command=save_history_as)
    save_as_button.pack()

# Save conversation history to a new file
def save_history_as():
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, "w") as file:
            json.dump(conversation_history, file)

# Asynchronous function to handle user's questions
async def handle_user_question_async():
    global exit_program
    while not exit_program:
        user_message = await listen_for_speech_async(languages[selected_language.get()])
        if user_message:
            ai_response = await ai_conversation_async(user_message)
            conversation_text.config(state=tk.NORMAL)  # Enable text widget for editing
            conversation_text.insert(tk.END, f"User: {user_message}\n")
            conversation_text.insert(tk.END, f"AI: {ai_response}\n")
            conversation_text.config(state=tk.DISABLED)  # Disable text widget for editing
            await speak_text_async(ai_response, languages[selected_language.get()])
            await asyncio.sleep(1)  # Delay for 1 second before continuing

# Function to start listening
# Function to start listening
def start_conversation():
    global exit_program, conversation_thread, start_button
    exit_program = True  # Signal the current conversation to exit
    start_button.config(state=tk.DISABLED)
    # Wait for the current conversation to finish
    if conversation_thread:
        conversation_thread.join()

    exit_program = False  # Reset the exit flag

    # Clear the conversation text
    conversation_text.config(state=tk.NORMAL)
    conversation_text.delete(1.0, tk.END)
    conversation_text.config(state=tk.DISABLED)

    # Get the selected subject
    subject = selected_subject.get()
    if selected_language.get() == 'Chinese':
        initial_intro = f"我是你的{subject}辅导老师，你有哪些问题？"
    else :
        initial_intro = f"I am your {subject} tutor. How can I assist you?"
    conversation_text.config(state=tk.NORMAL)  # Enable text widget for editing
    conversation_text.insert(tk.END, f"AI: {initial_intro}\n")
    conversation_text.config(state=tk.DISABLED)  # Disable text widget for editing

    asyncio.run(speak_text_async(initial_intro, languages[selected_language.get()]))

    # Start listening for user's questions
    conversation_thread = threading.Thread(target=asyncio.run, args=(handle_user_question_async(),))
    conversation_thread.start()

# Function to handle window closing
def on_closing():
    global exit_program
    exit_program = True
    save_conversation_history()
    root.destroy()

# Function to save conversation history to a file
def save_conversation_history():
    global conversation_history
    with open("conversation_history.json", "w") as file:
        json.dump(conversation_history, file)

# Function to load conversation history from a file
def load_conversation_history():
    global conversation_history
    try:
        with open("conversation_history.json", "r") as file:
            conversation_history = json.load(file)
    except FileNotFoundError:
        print("Conversation history file not found. Starting with an empty conversation.")

# Main function
def main():
    global root, conversation_text, selected_language, selected_subject, start_button
    root = tk.Tk()
    root.title("AI Conversation")
    window_width = 1000
    window_height = 400
    root.geometry(f"{window_width}x{window_height}")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"+{x}+{y}")

    frame = Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    # Background image
    canvas = Canvas(frame, width=400, height=350)
    canvas.pack(side=tk.LEFT)
    try:
        image = Image.open("robot3.jpg")
        image = image.resize((400, 350), Image.Resampling.LANCZOS)
        background_image = ImageTk.PhotoImage(image)
        canvas.image = background_image
        canvas.create_image(0, 0, anchor=tk.NW, image=background_image)
    except FileNotFoundError:
        print("Image file not found. Please check the image file path.")

    conversation_frame = Frame(frame)
    conversation_frame.pack(fill=tk.BOTH, expand=True)

    conversation_text = scrolledtext.ScrolledText(conversation_frame, wrap=tk.WORD)
    conversation_text.pack(fill=tk.BOTH, expand=True)
    conversation_text.config(state=tk.DISABLED)

    # Language selection menu
    language_label = Label(root, text="Select Language:")
    language_label.pack(side=tk.LEFT)

    selected_language = StringVar()
    selected_language.set("English")  # Set the default language
    language_menu = tk.OptionMenu(root, selected_language, *languages.keys())
    language_menu.pack(side=tk.LEFT)

    # Subject selection menu
    language_label = Label(root, text="Select Subject:")
    language_label.pack(side=tk.LEFT)
    selected_subject = StringVar()
    selected_subject.set("Mathematics")  # Default subject is Mathematics

    subjects = ["Mathematics", "History", "English", "Writing", "Chemistry"]

    choose_subject_button = tk.OptionMenu(root, selected_subject, *subjects)
    choose_subject_button.pack(side=tk.LEFT)

    # Start Conversation button
    start_button = tk.Button(root, text="Start Conversation", command=start_conversation)
    start_button.pack(side=tk.LEFT)  # Place this button at the top

    # Create a frame for the buttons
    button_frame = Frame(root)
    button_frame.pack(side=tk.BOTTOM, fill=tk.X)  # Place this frame at the bottom

    # Clear Conversation button
    clear_button = tk.Button(button_frame, text="Clear Conversation", command=clear_conversation)
    clear_button.pack(side=tk.LEFT)

    # View History button
    view_history_button = tk.Button(button_frame, text="View History", command=view_history)
    view_history_button.pack(side=tk.LEFT)

    # Save Conversation button
    save_conversation_button = tk.Button(button_frame, text="Save Conversation", command=save_conversation)
    save_conversation_button.pack(side=tk.LEFT)

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

def clear_conversation():
    global conversation_history
    conversation_history = [{"role": "teacher", "content": "Hi, I am AI. How can I assist you."}]
    conversation_text.config(state=tk.NORMAL)
    conversation_text.delete(1.0, tk.END)
    conversation_text.config(state=tk.DISABLED)

def save_conversation():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            current_text = conversation_text.get(1.0, tk.END)  # Get the current conversation text
            file.write(current_text)

if __name__ == "__main__":
    main()
