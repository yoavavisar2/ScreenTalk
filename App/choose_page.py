from tkinter import *
from client import Client
import threading
from functools import partial
from stream_page import StreamPage
from share_page import SharePage
from utils import pixels2points


class ChoosePage(Frame):
    def __init__(self, root, width, height, client: Client):
        super().__init__(root, bg="#031E49")
        self.client = client
        self.pack(fill="both", expand=True)
        self.width = width
        self.height = height
        self.choose = False
        self.usernameVar = StringVar(self)

        self.page()

    def page(self):
        for widget in self.winfo_children():
            widget.destroy()

        Label(self, text=f"welcome {self.client.username}", font=("ariel", pixels2points(self.width / 20)),
              bg="#031E49", fg="white").pack(pady=self.height // 20)

        self.buttons()

    def send_choose(self, username):
        txt = "choose:" + username
        message = self.client.encrypt(txt)
        self.client.client.send(message)
        self.choose = True

    def control(self):
        for widget in self.winfo_children():
            widget.destroy()

        Label(self, text="Enter username to connect", font=("ariel", pixels2points(self.width / 25)), bg="#031E49", fg="white").pack(pady=self.height//10)
        username_entry = Entry(self, font=("ariel", pixels2points(self.width / 50)), width=int(self.width // 100),
                               bg="lightgray", textvariable=self.usernameVar)
        username_entry.pack(pady=(0, self.height // 10))
        enter_button = Button(
            self, text="ENTER", width=self.width // 150, bg="#1EB500", font=("ariel", pixels2points(self.width / 40)),
            fg="white", activebackground="#1EB500", activeforeground="white", bd=0, relief=SUNKEN, command=self.submit
        )
        enter_button.pack()

        back = Button(self, text="BACK", width=self.width // 100, bg="#DC143C", font=("ariel", pixels2points(self.width // 50)), fg="white",
                      activebackground="#DC143C", activeforeground="white", bd=0, relief=SUNKEN, command=self.page)
        back.pack(pady=self.height // 10)

    def submit(self):
        msg = "control:" + self.usernameVar.get()
        data = self.client.encrypt(msg)
        self.client.client.send(data)
        try:
            rcv = self.client.client.recv(1024)
            decrypted = self.client.decrypt(rcv).decode()
            if decrypted == "good":
                msg = self.client.client.recv(1024)
                msg, ip = self.client.decrypt(msg).decode().split(':')
                if msg == "deny":
                    self.usernameVar.set("")
                    Label(self, text="access denied", font=("ariel", pixels2points(self.width / 50)), bg="#031E49",
                          fg="red").pack()
                if msg == "accept":
                    key = self.client.client.recv(1024)
                    key = self.client.decrypt(key)

                    for widget in self.winfo_children():
                        widget.destroy()
                    StreamPage(self, self.width, self.height, self.client, ip, key)

            elif decrypted == "bad":
                self.usernameVar.set("")
                Label(self, text="wrong username", font=("ariel", pixels2points(self.width / 50)), bg="#031E49",
                      fg="red").pack()
        except:
            print("waiting")

    def handle_recv(self):
        data = self.client.client.recv(1024)
        msg = self.client.decrypt(data).decode()

        canvas = Canvas(self, bd=0, highlightthickness=0, bg='#A9A9A9', width=self.width//2)
        canvas.place(relwidth=0.75, relheight=0.8, relx=0.5, rely=0.5, anchor="center")
        text = "new request from: " + msg
        Label(canvas, text=text, font=("ariel", pixels2points(self.width / 20)), bg="#A9A9A9", fg="white").pack(pady=self.height//10)
        canvas.tag_raise('canvas')

        button_frame = Frame(canvas, bg="#A9A9A9")
        button_frame.pack(pady=(self.height // 7, 0))
        font_size = pixels2points(self.width // 50)

        accept = Button(button_frame, text="ACCEPT", width=self.width // 100, bg="#32CD32", font=("ariel", font_size),
                        fg="white", activebackground="#32CD32", activeforeground="white",
                        bd=0, relief=SUNKEN, command=partial(self.accept, msg))
        accept.pack(side=LEFT, padx=(0, self.width // 5))

        deny = Button(button_frame, text="DENY", width=self.width // 100, bg="#DC143C", font=("ariel", font_size),
                      fg="white", activebackground="#DC143C", activeforeground="white", bd=0, relief=SUNKEN, command=partial(self.deny, msg))
        deny.pack(side=LEFT)

    def deny(self, username):
        msg = self.client.encrypt("choose:deny," + username)
        self.client.client.send(msg)
        self.allow()

    def accept(self, username):
        msg = self.client.encrypt("choose:accept," + username)
        self.client.client.send(msg)
        ip = self.client.client.recv(1024)
        ip = self.client.decrypt(ip).decode()

        key = self.client.client.recv(1024)
        key = self.client.decrypt(key)

        for widget in self.winfo_children():
            widget.destroy()
        SharePage(self, self.width, self.height, self.client, ip, key)

    def allow(self):
        encrypted_msg = self.client.encrypt("allow:")
        self.client.client.send(encrypted_msg)

        for widget in self.winfo_children():
            widget.destroy()

        text = "waiting for connection..."
        Label(self, text=text, font=("ariel", pixels2points(self.width / 20)), bg="#031E49", fg="white").pack(
            pady=self.height // 10)

        font_size = pixels2points(self.width // 50)
        back = Button(self, text="BACK", width=self.width // 100, bg="#DC143C", font=("ariel", font_size), fg="white",
                      activebackground="#DC143C", activeforeground="white", bd=0, relief=SUNKEN, command=self.back)
        back.pack(pady=self.height // 10)

        # Start the recv operation in a separate thread
        recv_thread = threading.Thread(target=self.handle_recv)
        recv_thread.daemon = True
        recv_thread.start()

    def back(self):
        encrypted_msg = self.client.encrypt("ExitAllow:")
        self.client.client.send(encrypted_msg)

        for widget in self.winfo_children():
            widget.destroy()

        Label(self, text=f"welcome {self.client.username}", font=("ariel", pixels2points(self.width / 20)),
              bg="#031E49", fg="white").pack(pady=self.height // 20)

        self.buttons()

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
