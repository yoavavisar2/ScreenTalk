from tkinter import *
from login_page import LoginPage
from signup_page import SignUpPage
from client import Client
from PIL import Image, ImageTk
from utils import pixels2points


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

    def show_home_screen(self):
        self.clear_frame()
        self.current_frame = Frame(self.root, bg="#1e3a8a")
        self.current_frame.pack(fill="both", expand=True)
        self.create_header()
        self.create_hero_section()
        self.create_feature_section()

    def create_header(self):
        header_frame = Frame(self.current_frame, bg="#1e3a8a", pady=10)
        header_frame.pack(fill=X)
        font_size = pixels2points(self.width // 60)

        img = Image.open("logo.png")

        new_height = self.height // 5
        aspect_ratio = img.width / img.height
        new_width = int(new_height * aspect_ratio)

        img = img.resize((new_width, new_height))

        logoImage = ImageTk.PhotoImage(img)
        logoLabel = Label(header_frame, image=logoImage, bg="#1e3a8a")

        # This next line will create a reference that stops the GC from deleting the object
        logoLabel.image = logoImage

        logoLabel.pack(side=LEFT, padx=10)

        button_frame = Frame(header_frame, bg="#1e3a8a")
        button_frame.pack(side=RIGHT)

        Button(button_frame, text="Exit", bg="#dc2626", bd=0, relief=SUNKEN, activebackground="#dc2626", activeforeground="white", fg="white", command=self.root.quit, width=self.width // 150, font=("ariel", font_size)).pack(side=LEFT, padx=self.width//150)

    def create_hero_section(self):
        hero_frame = Frame(self.current_frame, bg="#1e3a8a", pady=40)
        hero_frame.place(relx=0.5, rely=0.5, anchor="center")

        hero_label = Label(hero_frame, text="Seamless Desktop Control & Voice Communication", font=("Helvetica", pixels2points(self.width//50), "bold"), fg="white", bg="#1e3a8a")
        hero_label.pack(pady=10)

        sub_label = Label(hero_frame, text="Manage desktops and communicate effortlessly in real-time.", font=("Helvetica", pixels2points(self.width//75)), fg="white", bg="#1e3a8a")
        sub_label.pack(pady=5)

        button_frame = Frame(hero_frame, bg="#1e3a8a")
        button_frame.pack(pady=10)

        font_size = pixels2points(self.width // 60)
        Button(button_frame, text="Login", bg="#2563eb", bd=0, relief=SUNKEN, activebackground="#2563eb",
               activeforeground="white", fg="white", command=self.show_login, width=self.width // 150,
               font=("ariel", font_size)).pack(side=LEFT, padx=self.width // 150)
        Button(button_frame, text="Sign Up", bg="#16a34a", bd=0, relief=SUNKEN, activebackground="#16a34a",
               activeforeground="white", fg="white", command=self.show_signup, width=self.width // 150,
               font=("ariel", font_size)).pack(side=LEFT, padx=self.width // 150)

    def create_feature_section(self):
            feature_frame = Frame(self.current_frame, bg="#1e3a8a", pady=20)
            feature_frame.pack(fill=X, padx=20, side=BOTTOM)

            # Feature 1
            card1 = Frame(feature_frame, bg="#374151", padx=10, pady=10)
            card1.pack(side=LEFT, fill=BOTH, expand=True, padx=10)

            Label(card1, text="Seamless Desktop Control", font=("Helvetica", pixels2points(self.width // 50), "bold"), fg="white", bg="#374151").pack(pady=5)
            Label(card1, text="Gain complete control of remote desktops with a smooth experience.", fg="white", bg="#374151", wraplength=400, font=("Helvetica", pixels2points(self.width//75))).pack()

            # Feature 2
            card2 = Frame(feature_frame, bg="#374151", padx=10, pady=10)
            card2.pack(side=LEFT, fill=BOTH, expand=True, padx=10)

            Label(card2, text="Crystal-Clear Voice Communication", font=("Helvetica", pixels2points(self.width // 50), "bold"), fg="white", bg="#374151").pack(pady=5)
            Label(card2, text="Communicate effortlessly with high-quality voice connections.", fg="white", bg="#374151", wraplength=400, font=("Helvetica", pixels2points(self.width//75))).pack()
