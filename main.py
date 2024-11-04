from tkinter import *
import LoginPage

root = Tk()
bg_color = "#031E49"

width = root.winfo_screenwidth()
height = root.winfo_screenheight()


def pixels2points(pixels):
    return int(0.75 * pixels)


def window():
    root.state('zoomed')
    root.overrideredirect(True)
    root.title("ScreenTalk")
    root.resizable(False, False)
    root.config(bg=bg_color)


def main_text():
    font_size = pixels2points(width / 10)
    label = Label(root, text="Screen Talk", bg=bg_color, fg='white', font=('ariel', font_size))
    label.pack(pady=height // 20)


def exit_button():
    font_size = pixels2points(width / 40)
    exitB = Button(root, text="EXIT", width=width // 300, bg="#DC143C", command=root.destroy, font=("ariel", font_size),
                   fg="white", activebackground="#DC143C", activeforeground="white", bd=0, relief=SUNKEN)
    exitB.pack(pady=(height * 0.25, 0))


def login():
    for widget in root.winfo_children():
        widget.destroy()
    LoginPage.start()


def login_and_signup_buttons():
    font_size = pixels2points(width / 40)

    button_frame = Frame(root, bg=bg_color)
    button_frame.pack(pady=(height // 7, 0))

    loginB = Button(button_frame, text="LOGIN", width=width // 250, bg="#32CD32", font=("ariel", font_size),
                    fg="white", activebackground="#32CD32", activeforeground="white", bd=0, relief=SUNKEN, command=login)
    loginB.pack(side=LEFT, padx=(0, width//5))

    signupB = Button(button_frame, text="SIGNUP", width=width // 250, bg="#00A36C", font=("ariel", font_size),
                     fg="white", activebackground="#00A36C", activeforeground="white", bd=0, relief=SUNKEN)
    signupB.pack(side=LEFT)


def main_window():
    main_text()
    login_and_signup_buttons()
    exit_button()


def start():
    window()
    main_window()


start()
root.mainloop()
