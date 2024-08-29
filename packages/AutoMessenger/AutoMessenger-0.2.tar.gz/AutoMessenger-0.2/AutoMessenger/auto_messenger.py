# import time
# import pyautogui
# import random

# # Wait for a few seconds to allow you to open WhatsApp in your browser or desktop application.
# time.sleep(10)

# xx, yy = pyautogui.position()

# # Your message to send.
# message = [
#     "Hello",
#     "Hi",
#     "How are you?",
# ]


# def get_text():
#     rand_letter = random.choice(message)

#     pyautogui.typewrite(rand_letter, interval=0.2)

#     # Press Enter to send the message.r
#     pyautogui.press("enter")


# # Click on the input field to focus it.
# pyautogui.click(xx, yy)

# try:
#     while True:
#         #  on keyboard key press enter break loop condition

#         # Type your message.
#         get_text()
# except KeyboardInterrupt:
#     print("interrupted!")



import time
import pyautogui
import random


class AutoMessenger:
    def __init__(self, external_messages=None):
        """Initialize with default and external messages."""
        self.default_messages = [
            "Hello",
            "Hi",
            "How are you?",
        ]
        self.messages = self.load_messages(external_messages)
        self.input_position = None

    def load_messages(self, external_messages):
        """Load external messages if provided, otherwise use default ones."""
        if external_messages and isinstance(external_messages, list):
            return external_messages 
        return self.default_messages

    def set_input_position(self, sleep_time=5):
        """Get and set the cursor position for typing messages."""
        print("Please focus on the input field, position will be recorded in 5 seconds.")
        time.sleep(sleep_time)
        self.input_position = pyautogui.position()
        print(f"Position recorded: {self.input_position}")

    def send_message(self):
        """Select a random message and type it in the focused input field."""
        if not self.input_position:
            print("Input position not set. Call set_input_position() first.")
            return
        
        # Click on the input field to focus it.
        pyautogui.click(self.input_position)
        rand_message = random.choice(self.messages)
        pyautogui.typewrite(rand_message, interval=0.2)
        pyautogui.press("enter")

    def start_sending(self, delay=10):
        """Start the messaging process with a time delay."""
        print(f"Waiting for {delay} seconds. Prepare WhatsApp or any chat window.")
        time.sleep(delay)

        try:
            while True:
                self.send_message()
                time.sleep(random.randint(1, 5))  # Add a random delay between messages.
        except KeyboardInterrupt:
            print("Messaging interrupted!")


