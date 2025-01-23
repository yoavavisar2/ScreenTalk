from tkinter import *
from login_page import LoginPage
from signup_page import SignUpPage
from client import Client
from PIL import Image, ImageTk


def pixels2points(pixels):
    return int(0.75 * pixels)


class HomePage:
    def __init__(self, root, client: Client):
        self.root = root
        self.client = client
        self.root.title("Screen Talk")
        self.root.state('zoomed')
        self.root.attributes('-fullscreen', True)

        # Ensure the window appears in the taskbar
        self.root.iconify()
        self.root.update_idletasks()
        self.root.deiconify()

        self.root.resizable(False, False)
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()

        self.current_frame = None

        self.show_home_screen()

    def clear_frame(self):
        if self.current_frame is not None:
            self.current_frame.destroy()

    def show_login(self):
        self.clear_frame()
        self.current_frame = LoginPage(self.root, self.show_home_screen, self.width, self.height, self.client)

    def show_signup(self):
        self.clear_frame()
        self.current_frame = SignUpPage(self.root, self.show_home_screen, self.width, self.height, self.client)

    def login_and_signup_buttons(self):
        button_frame = Frame(self.current_frame, bg="#031E49")
        button_frame.pack()
        font_size = pixels2points(self.width / 40)

        loginB = Button(button_frame, text="LOGIN", width=self.width // 150, bg="#32CD32", font=("ariel", font_size),
                        fg="white", activebackground="#32CD32", activeforeground="white", bd=0, relief=SUNKEN, command=self.show_login)
        loginB.pack(side=LEFT, padx=(0, self.width // 5))

        signupB = Button(button_frame, text="SIGNUP", width=self.width // 150, bg="#00A36C", font=("ariel", font_size),
                         fg="white", activebackground="#00A36C", activeforeground="white", bd=0, relief=SUNKEN, command=self.show_signup)
        signupB.pack(side=LEFT)

    def show_home_screen(self):
        self.clear_frame()
        self.current_frame = Frame(self.root, bg="#031E49")
        self.current_frame.pack(fill="both", expand=True)

        img = Image.open("car.png")

        new_height = self.height//3
        aspect_ratio = img.width / img.height
        new_width = int(new_height * aspect_ratio)

        img = img.resize((new_width, new_height))

        logoImage = ImageTk.PhotoImage(img)
        logoLabel = Label(self.current_frame, image=logoImage, bg="#031E49")

        # This next line will create a reference that stops the GC from deleting the object
        logoLabel.image = logoImage

        logoLabel.pack(pady=self.height//10)
        self.login_and_signup_buttons()

        Button(self.current_frame, text="EXIT", width=self.width // 150, bg="#DC143C", command=self.root.quit,
               font=("ariel", pixels2points(self.width/40)), fg="white", activebackground="#DC143C", activeforeground="white",
               bd=0, relief=SUNKEN).pack(pady=(self.height * 0.25, 0))
