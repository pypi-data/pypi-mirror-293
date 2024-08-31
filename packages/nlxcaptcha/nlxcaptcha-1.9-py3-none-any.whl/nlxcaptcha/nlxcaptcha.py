import tkinter as tk
import openai
import platform
import threading
from tkinter import ttk
import sv_ttk
import random

class NLXCaptcha:
    def __init__(self, api_key, difficulty):
        self.api_key = api_key
        self.difficulty = difficulty
        openai.api_key = api_key
        self.device = self.detect_device()
        self.result = None

    def detect_device(self):
        device = "Unknown Device"
        if platform.system() == "Darwin":
            if "iPad" in platform.platform():
                device = "iPad"
            else:
                device = "Mac"
        elif platform.system() == "Windows":
            device = "Windows PC"
        elif platform.system() == "Linux":
            device = "Linux PC"
        elif "Android" in platform.platform():
            device = "Phone"
        return device

    def start_verification(self):
        self.window = tk.Tk()
        self.window.title("NLX CAPTCHA")
        self.window.geometry("400x200")
        topiclist = [
        "What is a cat?",
        "How to make ice?",
        "How does a smartphone boot up?",
        "What do you use an iPad for? If you don't have one, then what do you do on a rainy day?"
        ]
        global topic
        topic = random.choice(topiclist)
        prompt = tk.Label(self.window, text=f"Write a short paragraph about '{topic}'")
        prompt.pack(pady=20)

        self.text_entry = tk.Text(self.window, height=5, width=40)
        self.text_entry.pack()

        submit_button = tk.Button(self.window, text="Submit", command=self.run_verification)
        submit_button.pack(pady=10)

        sv_ttk.set_theme("dark")
        
        self.window.mainloop()

    def run_verification(self):
        self.loading = ttk.Progressbar(self.window, mode='indeterminate')
        self.loading.pack(pady=10)
        self.loading.start()

        threading.Thread(target=self.verify_response).start()

    def verify_response(self):
        user_input = self.text_entry.get("1.0", tk.END).strip()

        system_prompt = (
            f"You are an AI tasked with identifying whether a given text was written by a child, specifically one who frequently uses an iPad or similar device."
            f" Children who are considered 'iPad kids' often write with simple sentence structures, basic vocabulary, and have a casual tone. HOWEVER, if there is proper punctuation, and the information provided is not imaginative, straight and to the point, and also uses synonyms, then they are NOT an iPad kid. They should also stay consistent with the topic they were given. In this case, the topic they should write about is '{topic}'"
            f" The device the user is using is: {self.device}. Keep in mind that 'iPad kids' are most likely to use an iPad or a phone."
            f" Be more strict if the difficulty level is high. Difficulty: {self.difficulty}/10."
            f" Respond with '1' if you think the text was written by an 'iPad kid,' otherwise respond with '0'."
        )

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Sample: {user_input}"}
            ]
        )

        content = response['choices'][0]['message']['content'].strip()

        # Ensure the response is either '1' or '0'
        if content not in ["1", "0"]:
            content = "0"  # Default to '0' if the response is unexpected

        self.result = content  # Set the result here

        self.loading.stop()
        self.loading.pack_forget()

        self.window.destroy()

def verify(difficulty, openaiapikey):
    captcha = NLXCaptcha(api_key=openaiapikey, difficulty=difficulty)
    captcha.start_verification()

    # Ensure that the result is set before returning it
    if captcha.result is None:
        captcha.result = "0"  # Default to "0" if no result was set

    return captcha.result
