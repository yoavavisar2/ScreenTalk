from tkinter import *
from client import Client


def pixels2points(pixels):
    return int(0.75 * pixels)


class ChoosePage(Frame):
    def __init__(self, root, width, height, client: Client):
        super().__init__(root, bg="#031E49")
        self.client = client
        self.pack(fill="both", expand=True)
        self.width = width
        self.height = height

        Label(self, text=f"welcome {self.client.username}", font=("ariel", pixels2points(self.width/20)),
              bg="#031E49", fg="white").pack(pady=self.height // 20)

        self.buttons()

    def control(self):
        pass
    # TODO: send the server this user is control and receive allow list

    def allow(self):
        encrypted_msg = self.client.encrypt("allow:")
        self.client.client.send(encrypted_msg)

    def buttons(self):
        button_frame = Frame(self, bg="#031E49")
        button_frame.pack(pady=(self.height // 7, 0))
        font_size = pixels2points(self.width // 50)

        control = Button(button_frame, text="CONTROL", width=self.width // 100, bg="#32CD32", font=("ariel", font_size),
                         fg="white", activebackground="#32CD32", activeforeground="white",
                         bd=0, relief=SUNKEN, command=self.control)
        control.pack(side=LEFT, padx=(0, self.width // 5))

        allow = Button(button_frame, text="AUTHORIZE", width=self.width // 100, bg="#00A36C", font=("ariel", font_size),
                       fg="white", activebackground="#00A36C", activeforeground="white", bd=0, relief=SUNKEN,
                       command=self.allow)
        allow.pack(side=LEFT)

        Button(self, text="EXIT", width=self.width // 150, bg="#DC143C", command=self.quit,
               font=("ariel", pixels2points(self.width / 40)), fg="white", activebackground="#DC143C",
               activeforeground="white",
               bd=0, relief=SUNKEN).pack(pady=(self.height * 0.25, 0))
