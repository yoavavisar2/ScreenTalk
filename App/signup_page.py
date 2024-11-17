from tkinter import *
from client import Client


def pixels2points(pixels):
    return int(0.75 * pixels)

class SignUpPage(Frame):
    def __init__(self, root, back_command, width: int, height, client: Client):
        super().__init__(root, bg="#031E49")
        self.client = client
        self.pack(fill="both", expand=True)
        self.width = width
        self.height = height

        self.first_name = StringVar(self)
        self.last_name = StringVar(self)
        self.username = StringVar(self)
        self.password = StringVar(self)

        Label(self, text="Signup", font=("ariel", pixels2points(self.width / 10)), bg="#031E49", fg="white").pack(pady=self.height // 20)

        up_frame = Frame(self, bg="#031E49")
        up_frame.pack()

        first_frame = Frame(up_frame, bg="#031E49")
        first_frame.grid(row=0, column=0, padx=self.width//25)

        Label(first_frame, text="first name", font=("ariel", pixels2points(self.width / 25)), bg="#031E49", fg="white").pack()
        first_entry = Entry(first_frame, font=("ariel", pixels2points(self.width / 50)), width=self.width // 100, bg="lightgray", textvariable=self.first_name)
        first_entry.pack(pady=(0, self.height // 10))

        second_frame = Frame(up_frame, bg="#031E49")
        second_frame.grid(row=0, column=1, padx=self.width // 25)

        Label(second_frame, text="last name", font=("ariel", pixels2points(self.width / 25)), bg="#031E49", fg="white").pack()
        second_entry = Entry(second_frame, font=("ariel", pixels2points(self.width / 50)), width=self.width // 100, bg="lightgray", textvariable=self.last_name)
        second_entry.pack(pady=(0, self.height // 10))

        down_frame = Frame(self, bg="#031E49")
        down_frame.pack()

        user_frame = Frame(down_frame, bg="#031E49")
        user_frame.grid(row=0, column=0, padx=self.width // 25)

        Label(user_frame, text=" username ", font=("ariel", pixels2points(self.width / 25)), bg="#031E49", fg="white").pack()
        user_entry = Entry(user_frame, font=("ariel", pixels2points(self.width / 50)), width=self.width // 100, bg="lightgray", textvariable=self.username)
        user_entry.pack(pady=(0, self.height // 10))

        password_frame = Frame(down_frame, bg="#031E49")
        password_frame.grid(row=0, column=1, padx=self.width // 25)

        Label(password_frame, text="password", font=("ariel", pixels2points(self.width / 25)), bg="#031E49",
              fg="white").pack()
        password_entry = Entry(password_frame, font=("ariel", pixels2points(self.width / 50)), width=self.width // 100, show="*", bg="lightgray", textvariable=self.password)
        password_entry.pack(pady=(0, self.height // 10))

        buttons_frame = Frame(self, bg="#031E49")
        buttons_frame.pack()

        font_size = pixels2points(self.width / 40)
        enter_button = Button(
            buttons_frame, text="ENTER", width=self.width // 250, bg="#1EB500", font=("ariel", font_size),
            fg="white", activebackground="#1EB500", activeforeground="white", bd=0, relief=SUNKEN, command=self.submit
        )
        enter_button.grid(row=0, column=0, padx=self.width // 25)

        back_button = Button(
            buttons_frame, text="BACK", width=self.width // 250, bg="#DC143C", font=("ariel", font_size),
            fg="white", activebackground="#DC143C", activeforeground="white", bd=0, relief=SUNKEN, command=back_command
        )
        back_button.grid(row=0, column=1, padx=self.width // 25)

    def submit(self):
        data = f"signup/{self.first_name.get()}/{self.last_name.get()}/{self.username.get()}/{self.password.get()}"
        encrypted_data = self.client.encrypt(data)
        self.client.client.send(encrypted_data)
