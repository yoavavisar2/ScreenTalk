from tkinter import *

def pixels2points(pixels):
    return int(0.75 * pixels)

class LoginPage(Frame):
    def __init__(self, root, back_command, width: int, height, conn):
        super().__init__(root, bg="#031E49")
        self.conn = conn
        self.pack(fill="both", expand=True)
        self.width = width
        self.height = height

        Label(self, text="Login", font=("ariel", pixels2points(self.width/10)), bg="#031E49", fg="white").pack(pady=self.height // 20)

        Label(self, text="Username", font=("ariel", pixels2points(self.width/25)), bg="#031E49", fg="white").pack()
        username_entry = Entry(self, font=("ariel", pixels2points(self.width/50)), width=self.width//100, bg="lightgray")
        username_entry.pack(pady=(0, self.height//10))

        Label(self, text="Password", font=("ariel", pixels2points(self.width / 25)), bg="#031E49", fg="white").pack()
        password_entry = Entry(self, font=("ariel", pixels2points(self.width / 50)), width=self.width // 100,
                               bg="lightgray", show="*")
        password_entry.pack(pady=(0, self.height // 10))

        buttons_frame = Frame(self, bg="#031E49")
        buttons_frame.pack()

        font_size = pixels2points(self.width / 40)
        enter_button = Button(
            buttons_frame, text="ENTER", width=self.width // 250, bg="#1EB500", font=("ariel", font_size),
            fg="white", activebackground="#1EB500", activeforeground="white", bd=0, relief=SUNKEN
        )
        enter_button.grid(row=0, column=0, padx=self.width//25)

        back_button = Button(
            buttons_frame, text="BACK", width=self.width // 250, bg="#DC143C", font=("ariel", font_size),
            fg="white", activebackground="#DC143C", activeforeground="white", bd=0, relief=SUNKEN, command=back_command
        )
        back_button.grid(row=0, column=1, padx=self.width//25)
