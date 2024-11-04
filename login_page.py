from tkinter import *

def pixels2points(pixels):
    return int(0.75 * pixels)

class LoginPage(Frame):
    def __init__(self, root, back_command, width: int, height):
        super().__init__(root, bg="#031E49")
        self.pack(fill="both", expand=True)
        self.width = width
        self.height = height

        Label(self, text="Login", font=("ariel", pixels2points(self.width/10)), bg="#031E49", fg="white").pack(pady=self.height // 20)

        Label(self, text="Username", font=("ariel", pixels2points(self.width/25)), bg="#031E49", fg="white").pack()
        username_entry = Entry(self, font=("ariel", pixels2points(self.width/50)), width=self.width//100, bg="lightgray")
        username_entry.pack(pady=(0, 100))

        # Password entry
        Label(self, text="Password", font=("Helvetica", 12), bg="blue", fg="white").pack(pady=5)
        password_entry = Entry(self, font=("Helvetica", 14), width=20, show="*", bg="lightgray")
        password_entry.pack(pady=5)

        # Buttons frame
        buttons_frame = Frame(self, bg="blue")
        buttons_frame.pack(pady=20)

        # Enter button
        enter_button = Button(
            buttons_frame, text="Enter", font=("Helvetica", 12), bg="green", fg="white", width=10
        )
        enter_button.grid(row=0, column=0, padx=10)

        # Back button
        back_button = Button(
            buttons_frame, text="Back", font=("Helvetica", 12), bg="red", fg="white", width=10, command=back_command
        )
        back_button.grid(row=0, column=1, padx=10)
