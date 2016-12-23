#!/usr/bin/env python3
#txtlock.py
#Travis Kipp
#December 13, 2015

'''
    A password entry GUI using tkinter

    TODO:
      Finish Help window
      Polish About window
      Secrets window bug

    CHANGELOG:
    12/13/2016
      Initially created as a quiz for CIS
    12/13/16
      Improved padding for Windows
      Grayed out the password label
      Removed red clear button
      Disable buttons when error occurs (except clear)
    12/14/16
      Improved Secret widget
      Added menubar
      Started to add saving a message functionality
      Added Windows beep sounds for locking and unlocking
      Stated adding keyboard input support on keypad frame
    12/15/16
      Keyboard entry now works correctly
      Enter to activate unlock()
      Ctrl + Q to quit program (root.destroy())
      F1 for  help window
    12/16/16
      Built to exe for the first time (Took way too long to figure out)
      Added Tools menu > Change Password (adding soon)
    12/17/16
      Added password changing window
    12/18/16
      Added better support for Linux (disable winsound)
      Ctrl + S to save content in secrets window
      Started adding status bar
    12/22/16
      All windows now open in the center of the screen
'''

from tkinter import *
import threading
import platform
if platform.system() == 'Windows':
    import winsound

BTN_FONT = ("Arial", 14, "bold")
PWD_FONT = ("Arial", 18, "bold")

PWD_WIN_TITLE_FONT = ("Arial", 12)
PWD_WIN_LBL_FONT = ("Arial", 10)
PWD_WIN_BTN_B_FONT = ("Arial", 10, "bold")
PWD_WIN_BTN_FONT = ("Arial", 10)

PASSWORD = ""
SAVED_MSG = "Insert content here to save it behind your password!\n" +\
            "I'd suggest overwritting this or you'll look silly."

class Application(Frame):
    """ GUI application which will show a keypad.

    The user is able to input their password with buttons.
    If the password it incorrect, it displays an error.
    If the password is correct, it says unlocked but does nothing else.
    """

    def __init__(self, master):
        """ Initialize the frame. """
        super(Application, self).__init__(master)
        self.MAX = 0
        self.grid()
        self.PASSWORD = PASSWORD
        self.SAVED_MSG = SAVED_MSG
        self.create_widgets()

    def create_widgets(self):
        """ Create buttons and sunken label"""
        # label
        self.pwdLbl = Label(self, text = "", font=PWD_FONT,
                            background="grey", fg="black", justify=CENTER)
        self.pwdLbl.grid(row=0, column=0, columnspan=100, sticky=W+E,
                         padx=(10,0), pady=(10,0))
        self.pwdLbl.configure(relief=SUNKEN, width=10, height=2)

        # numeric buttons
        # row 2
        self.btn7 = Button(self, text = "7", font=BTN_FONT, command=lambda:
                           self.any_click("7"))
        self.btn8 = Button(self, text = "8", font=BTN_FONT, command=lambda:
                           self.any_click("8"))
        self.btn9 = Button(self, text = "9", font=BTN_FONT, command=lambda:
                           self.any_click("9"))

        self.btn7.grid(row=1, column=0, padx=(10, 0))
        self.btn8.grid(row=1, column=1)
        self.btn9.grid(row=1, column=3)

        self.btn7.configure(height=2, width=4)
        self.btn8.configure(height=2, width=4)
        self.btn9.configure(height=2, width=4)

        # row 3
        self.btn4 = Button(self, text = "4", font=BTN_FONT, command=lambda:
                           self.any_click("4"))
        self.btn5 = Button(self, text = "5", font=BTN_FONT, command=lambda:
                           self.any_click("5"))
        self.btn6 = Button(self, text = "6", font=BTN_FONT, command=lambda:
                           self.any_click("6"))

        self.btn4.grid(row=2, column=0, padx=(10, 0))
        self.btn5.grid(row=2, column=1)
        self.btn6.grid(row=2, column=3)

        self.btn4.configure(height=2, width=4)
        self.btn5.configure(height=2, width=4)
        self.btn6.configure(height=2, width=4)

        # row 4
        self.btn1 = Button(self, text = "1", font=BTN_FONT, command=lambda:
                           self.any_click("1"))
        self.btn2 = Button(self, text = "2", font=BTN_FONT, command=lambda:
                           self.any_click("2"))
        self.btn3 = Button(self, text = "3", font=BTN_FONT, command=lambda:
                           self.any_click("3"))

        self.btn1.grid(row=3, column=0, padx=(10, 0))
        self.btn2.grid(row=3, column=1)
        self.btn3.grid(row=3, column=3)

        self.btn1.configure(height=2, width=4)
        self.btn2.configure(height=2, width=4)
        self.btn3.configure(height=2, width=4)

        # row 5
        self.btn0 = Button(self, text = "0", font=BTN_FONT, command=lambda:
                           self.any_click("0"))
        self.btnClear = Button(self, text = "Clear", font=BTN_FONT,
                               command=lambda: self.clear())

        self.btn0.grid(row=4, column=0, padx=(10, 0))
        self.btnClear.grid(row=4, column=1, columnspan=3, sticky=W+E)

        self.btn0.configure(height=2, width=4)
        self.btnClear.configure(height=2, width=4)

        # row 6 - Unlock
        self.btnUnlock = Button(self, text = "Unlock", font=BTN_FONT,
                                command=lambda: app.unlock())

        self.btnUnlock.grid(row=5, column=0, columnspan=4, sticky=W+E,
                            padx=(10, 0))

        self.btnUnlock.configure(height=2, width=4)

    def any_click(self, newText):
        """Changes label based on button click"""
        text = self.pwdLbl.cget("text")
        if self.MAX < 7:
            self.pwdLbl.configure(text=text + newText)
            self.MAX += 1
        else:
            print('Too many digits!')

    def remove_char(self):
        """Removes other characters if the total characters exceeds 7."""
        text = self.pwdLbl.cget("text")
        self.pwdLbl.configure(text=text[:-1])
        if self.MAX != 0:
            self.MAX -= 1

    def clear(self):
        """Clears the password entry box and resets the counter to 0"""
        self.enable_btns()
        self.pwdLbl.configure(text= "")
        self.btnUnlock.configure(text= "Unlock",
                                 command=lambda: app.unlock())
        self.MAX = 0
        print('Cleared password entry box')
        print('Reset counter')

    def unlock(self):
        """Checks if entred numbers are the password

        If the entered numbers are correct, display UNLOCKED
        If the entered numbers are incorrect, display ERROR
        """
        if self.pwdLbl.cget("text") == self.PASSWORD:
            self.pwdLbl.configure(text= "UNLOCKED")
            self.btnUnlock.configure(text="Lock", command=lambda:
                                     self.lock())
            self.secrets_win()
            self.disable_btns()
            if platform.system() == 'Windows':
                winsound.Beep(400, 100)
                winsound.Beep(500, 100)
            print('UNLOCKED')
        else:
            self.pwdLbl.configure(text= "ERROR")
            self.MAX = 7
            self.disable_btns()
            self.btnUnlock.configure(state=DISABLED)
            self.btnClear.configure(state=NORMAL)
            #time.sleep(1) - Does not work correctly
            #self.clear() - Must manually clear
            print('ERROR')

    def disable_btns(self):
        """Disables all buttons except Clear button when there's an error"""
        self.btn7.configure(state=DISABLED)
        self.btn8.configure(state=DISABLED)
        self.btn9.configure(state=DISABLED)

        self.btn4.configure(state=DISABLED)
        self.btn5.configure(state=DISABLED)
        self.btn6.configure(state=DISABLED)

        self.btn1.configure(state=DISABLED)
        self.btn2.configure(state=DISABLED)
        self.btn3.configure(state=DISABLED)

        self.btn0.configure(state=DISABLED)
        self.btnClear.configure(state=DISABLED)

    def enable_btns(self):
        """Enables all buttons"""
        self.btn7.configure(state=NORMAL)
        self.btn8.configure(state=NORMAL)
        self.btn9.configure(state=NORMAL)

        self.btn4.configure(state=NORMAL)
        self.btn5.configure(state=NORMAL)
        self.btn6.configure(state=NORMAL)

        self.btn1.configure(state=NORMAL)
        self.btn2.configure(state=NORMAL)
        self.btn3.configure(state=NORMAL)

        self.btn0.configure(state=NORMAL)
        self.btnUnlock.configure(state=NORMAL)

    def secrets_win(self):
        """Displayed after correct password"""
        self.secrets_win = Toplevel()
        self.secrets_win.title("Secrets")
        if platform.system() == 'Windows':
            w = 645
            h = 406
            x = (ws/2) - (w/2)
            y = (hs/2) - (h/2)
            self.secrets_win.geometry('%dx%d+%d+%d' % (w, h, x, y))
        else:
            w = 567
            h = 360
            x = (ws/2) - (w/2)
            y = (hs/2) - (h/2)
            self.secrets_win.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.secrets_win.resizable(width=False, height=False)

        self.usrTxt = Text(self.secrets_win, wrap='word')
        self.usrTxt.insert(0.0, self.SAVED_MSG)
        self.usrTxt.grid()
        self.usrTxt.focus_set()

        self.status = Label(self.secrets_win, text="Test", bd=1,
                            relief=SUNKEN, anchor=W)
        self.status.grid(sticky=W+E)

        self.secrets_win.bind('<Control-s>', lock_combo)

        # Menubar
        menubar = Menu(self.secrets_win)

        # File menu
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save      Ctrl+S",
                             command=lambda: self.save())
        filemenu.add_command(label="Close",
                             command=lambda: self.secrets_win.withdraw())
        menubar.add_cascade(label="File", menu=filemenu)

        self.secrets_win.config(menu=menubar)

        #self.update_status()
        #self.secrets_win.protocol("WM_DELETE_WINDOW", self.handler)

    '''
    def update_status(self):
        """Updates the status bar status

        If the user input = the saved contents disaplay 'saved'
        If the user input != the saved contents display 'unsaved changes'
        """
        threading.Timer(2.0, self.update_status).start()
        if self.SAVED_MSG == self.usrTxt.get("0.0", END)[:-1]:
            self.status.configure(text="✓ Saved")
        else:
            self.status.configure(text="✕ Unsaved changes")

    def handler(self):
        """Handles closing the secrets_win"""
        self.update_status().terminate()
    '''


    def lock(self):
        """Closes the Secrets Window"""
        self.clear()
        self.save()
        if platform.system() == 'Windows':
            winsound.Beep(500, 100)
            winsound.Beep(400, 100)
        self.btnClear.configure(state=NORMAL)
        self.btnUnlock.configure(text='Unlock', command=lambda:
                                 app.unlock())
        self.secrets_win.withdraw()
        print('LOCKED')

    def save(self):
        self.SAVED_MSG = self.usrTxt.get("0.0", END)[:-1]
        print("Saved text:\n" + self.SAVED_MSG)

    def changePwd_win(self):
        """Displayed if Tools > Change Password is clicked"""
        changePwd_win = Toplevel()
        changePwd_win.title("Change Password")
        changePwd_win.resizable(width=False, height=False)

        w = 200
        h = 165
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        changePwd_win.geometry('%dx%d+%d+%d' % (w, h, x, y))

        # row 0
        titleLbl = Label(changePwd_win, text="Change your password",
                     font=PWD_WIN_TITLE_FONT, anchor=CENTER)
        titleLbl.grid(row=0, column=0, padx=(10, 10), columnspan=2)

        # row 1
        currentLbl = Label(changePwd_win, text="Current Password",
                           font=PWD_WIN_LBL_FONT, anchor=W)
        currentLbl.grid(row=1, column=0, sticky=W+E, padx=(10,0),
                        columnspan=2)

        # row 2
        self.currentPwdEntry = Entry(changePwd_win)
        self.currentPwdEntry.grid(row=2, column=0, sticky=W+E, padx=(10,0),
                                  columnspan=2)
        self.currentPwdEntry.focus_set()

        # row 3
        newLbl = Label(changePwd_win, text="New Password",
                       font=PWD_WIN_LBL_FONT, anchor=W)
        newLbl.grid(row=3, column=0, sticky=W+E, padx=(10,0), columnspan=2)

        # row 4
        self.newPwdEntry = Entry(changePwd_win)
        self.newPwdEntry.grid(row=4, column=0, sticky=W+E, padx=(10,0),
                              columnspan=2)

        # row 5
        self.msg = Label(changePwd_win, text="")
        self.msg.grid(row=5, column=0, sticky=W+E, columnspan=2)

        # row 6
        btnSave = Button(changePwd_win, text = "Save", command=lambda:
                         self.pwdCheck(), font=PWD_WIN_BTN_B_FONT,
                         height=1, width=5)
        btnSave.grid(row=6, column=0, sticky=W+E, padx=(10,0))

        btnClose = Button(changePwd_win, text = "Close", command=lambda:
                          changePwd_win.destroy(), font=PWD_WIN_BTN_FONT,
                          height=1, width=5)
        btnClose.grid(row=6, column=1, sticky=W+E)

    def pwdCheck(self):
        """Checks if current password = inputed password"""
        if self.currentPwdEntry.get() == self.PASSWORD:
            self.PASSWORD = self.newPwdEntry.get()
            self.msg.configure(text="Password changed to: " + self.PASSWORD)
            print("Password changed to:", self.PASSWORD)

        else:
            self.msg.configure(text="Current password is incorrect!")
            print("Current password is incorrect!")


    def about_win(self):
        """Displayed if Help > About is clicked"""
        about_win = Toplevel()
        about_win.title("About")
        w = 200
        h = 115
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        about_win.geometry('%dx%d+%d+%d' % (w, h, x, y))
        about_win.resizable(width=False, height=False)

        # row 0
        lbl1 = Label(about_win, text="Created by:")
        lbl1.grid(row=0, column=0)

        lbl2 = Label(about_win, text="Travis Kipp")
        lbl2.grid(row=0, column=1)


        # row 2
        lbl3 = Label(about_win, text="Website:")
        lbl3.grid(row=2, column=0)

        lbl4 = Label(about_win, text="https://invisamage.com")
        lbl4.grid(row=2, column=1)

        # row 3
        lbl5 = Label(about_win, text="OS:")
        lbl5.grid(row=3, column=0)

        lbl6 = Label(about_win, text=platform.system())
        lbl6.grid(row=3, column=1)

        # row 4
        btnClose = Button(about_win, text = "Close", command=
                          about_win.destroy)
        btnClose.grid(row=4, column=0, columnspan=2)

    def help_win(self):
        """Displayed if Help > TxtLock Help is clicked"""
        help_win = Toplevel()
        help_win.title("TxtLock Help")
        w = 250
        h = 200
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        help_win.geometry('%dx%d+%d+%d' % (w, h, x, y))
        help_win.resizable(width=False, height=False)

        lbl1 = Label(help_win, text="WIP")
        lbl1.grid(row=0, column=0)
        btnClose = Button(help_win, text = "Close", command=
                          help_win.destroy)
        btnClose.grid(row=3, column=0)

if __name__ == "__main__":
    root = Tk()

    menubar = Menu(root)

    # File menu
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Quit      Ctrl+Q", command=root.destroy)
    menubar.add_cascade(label="File", menu=filemenu)

    # Edit menu
    editmenu = Menu(menubar, tearoff=0)
    editmenu.add_command(label="Cut")
    editmenu.add_command(label="Copy")
    editmenu.add_command(label="Paste")
    editmenu.configure()
    menubar.add_cascade(label="Edit", menu=editmenu)

    # Tools menu
    toolsmenu = Menu(menubar, tearoff=0)
    toolsmenu.add_command(label="Change Password", command=lambda:
                          app.changePwd_win())
    menubar.add_cascade(label="Tools", menu=toolsmenu)

    # Help menu
    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="TxtLock Help      F1", command=lambda:
                         app.help_win())
    helpmenu.add_command(label="About", command=lambda:
                         app.about_win())
    menubar.add_cascade(label="Help", menu=helpmenu)

    # display the menu
    root.config(menu=menubar)

    root.title("TxtLock")
    
    # get screen width and height
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
        
    #Adjust window size based on operating system
    if platform.system() == 'Linux':
        w = 240
        h = 360
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    else:
        w = 195
        h = 390
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    root.resizable(width=False, height=False)
    #root.iconbitmap('txtlock.ico')

    app = Application(root)

    #Detect button down
    def keyup(e):
        if e.char == '1':
            app.any_click("1")
        if e.char == '2':
            app.any_click("2")
        if e.char == '3':
            app.any_click("3")
        if e.char == '4':
            app.any_click("4")
        if e.char == '5':
            app.any_click("5")
        if e.char == '6':
            app.any_click("6")
        if e.char == '7':
            app.any_click("7")
        if e.char == '8':
            app.any_click("8")
        if e.char == '9':
            app.any_click("9")
        if e.char == '0':
            app.any_click("0")
        print ('up', e.char)

    def enter(event):
        app.unlock()
        print("Return/Enter")

    def lock_combo(event):
        app.save()
        print("Ctrl + S")

    def quit_combo(event):
        root.destroy()
        print("Ctrl + Q")

    def remove_char(event):
        app.remove_char()
        print('BackSpace')

    def help_combo(event):
        app.help_win()
        print('F1')

    app.bind('<Return>', enter)
    app.bind('<KP_Enter>', enter)
    app.bind('<Control-q>', quit_combo)
    app.bind('<BackSpace>', remove_char)
    app.bind('<F1>', help_combo)
    app.bind("<KeyRelease>", keyup)
    app.focus_set()

    root.mainloop()
