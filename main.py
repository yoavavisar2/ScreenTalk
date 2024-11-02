from tkinter import *

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
    font_size = pixels2points(width/10)
    label = Label(root, text="Screen Talk", bg=bg_color, fg='white', font=('ariel', font_size))
    label.pack(pady=height//20)


def exit_button():
    font_size = pixels2points(width / 40)
    exitB = Button(root, text="Exit", width=width//300, bg="#DC143C", command=root.destroy, font=("ariel", font_size),
                   fg="white", activebackground="#DC143C", activeforeground="white", bd=0, relief=SUNKEN)
    exitB.pack()


def main_window():
    main_text()
    exit_button()


def start():
    window()
    main_window()


start()
root.mainloop()
