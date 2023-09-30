import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
from PIL import Image, ImageTk
import win32gui
import ControlWindow

class TopGUI:
    def __init__(self, root,x,y,data):
        self.hwnd = data["hwnd"]
        self.hider = data["hider"]
        self.allwindows = data["allwindows"]
        self.unstabler = data["unstabler"]        
        
        self.x = x
        self.y = y
        self.canDestroy = True
        self.setAlphaing = False
        top = tk.Toplevel(root)

        top.geometry("120x70+"+str(x)+"+"+str(y))
        top.minsize(120, 1)
        top.maxsize(1924, 1781)
        top.resizable(0,  0)
        top.title("Toplevel")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        top.attributes('-topmost', True)
        top.overrideredirect(True)
        top.attributes("-alpha", 1)
        # top.bind("<FocusOut>", lambda event: self.focusout())
        top.bind("<Map>", lambda event: self.update())
        
        self.top = top
        """---------------------------------------------------------------------------------"""
        self.frame = tk.Frame(self.top, width=300,
                              height=200, borderwidth=1, relief="solid")
        self.frame.configure(background="#d9d9d9")
        self.frame.configure(highlightbackground="#d9d9d9")
        self.frame.pack(expand=True)
      
        """---------------------------------------------------------------------------------"""
        self.img1 = Image.open(r"imgs\top.png")
        self.img1 = self.img1.resize((22, 22))
        self.img1 = ImageTk.PhotoImage(self.img1)

        self.img1B = Image.open(r"imgs\notop.png")
        self.img1B = self.img1B.resize((22, 22))
        self.img1B = ImageTk.PhotoImage(self.img1B)

        self.Button1 = tk.Button(self.top, image=self.img1)
        self.Button1.place(relx=0.042, rely=0.063, height=30, width=30)
        self.Button1.configure(activebackground="beige")
        self.Button1.configure(activeforeground="black")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(compound='left')
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")

        self.Button1.bind("<Button-1>", lambda event: self.doTop())
        self.Button1.bind("<ButtonRelease>", lambda event: self.update())
        """---------------------------------------------------------------------------------"""
        self.img2 = Image.open(r"imgs\eye.png")
        self.img2 = self.img2.resize((22, 22))
        self.img2 = ImageTk.PhotoImage(self.img2)

        self.img2B = Image.open(r"imgs\Ceye.png")
        self.img2B = self.img2B.resize((22, 22))
        self.img2B = ImageTk.PhotoImage(self.img2B)

        self.Button2 = tk.Button(self.top, image=self.img2)
        self.Button2.place(relx=0.367, rely=0.063, height=30, width=30)
        self.Button2.configure(activebackground="beige")
        self.Button2.configure(activeforeground="black")
        self.Button2.configure(background="#d9d9d9")
        self.Button2.configure(compound='left')
        self.Button2.configure(disabledforeground="#a3a3a3")
        self.Button2.configure(foreground="#000000")
        self.Button2.configure(highlightbackground="#d9d9d9")
        self.Button2.configure(highlightcolor="black")
        self.Button2.configure(pady="0")

        self.Button2.bind("<Button-1>", lambda event: self.doHide())
        self.Button2.bind("<ButtonRelease>", lambda event: self.update())
        """---------------------------------------------------------------------------------"""
        self.img3 = Image.open(r"imgs\hide.png")
        self.img3 = self.img3.resize((22, 22))
        self.img3 = ImageTk.PhotoImage(self.img3)

        self.img3B = Image.open(r"imgs\show.png")
        self.img3B = self.img3B.resize((22, 22))
        self.img3B = ImageTk.PhotoImage(self.img3B)

        self.Button3 = tk.Button(self.top, image=self.img3)
        self.Button3.place(relx=0.692, rely=0.063, height=30, width=30)
        self.Button3.configure(activebackground="beige")
        self.Button3.configure(activeforeground="black")
        self.Button3.configure(background="#d9d9d9")
        self.Button3.configure(compound='left')
        self.Button3.configure(cursor="fleur")
        self.Button3.configure(disabledforeground="#a3a3a3")
        self.Button3.configure(foreground="#000000")
        self.Button3.configure(highlightbackground="#d9d9d9")
        self.Button3.configure(highlightcolor="black")
        self.Button3.configure(pady="0")

        self.Button3.bind("<Button-1>", lambda event: self.doDisabled())
        self.Button3.bind("<ButtonRelease>", lambda event: self.delayupdate())
        """---------------------------------------------------------------------------------"""
        self.img4 = Image.open(r"imgs\unstable.png")
        self.img4 = self.img4.resize((28, 28))
        self.img4 = ImageTk.PhotoImage(self.img4)

        self.img4B = Image.open(r"imgs\nounstable.png")
        self.img4B = self.img4B.resize((28, 28))
        self.img4B = ImageTk.PhotoImage(self.img4B)

        self.Button4 = tk.Button(self.top, image=self.img4)
        self.Button4.place(relx=0.042, rely=0.526, height=30, width=30)
        self.Button4.configure(activebackground="beige")
        self.Button4.configure(activeforeground="black")
        self.Button4.configure(background="#d9d9d9")
        self.Button4.configure(compound='left')
        self.Button4.configure(cursor="fleur")
        self.Button4.configure(disabledforeground="#a3a3a3")
        self.Button4.configure(foreground="#000000")
        self.Button4.configure(highlightbackground="#d9d9d9")
        self.Button4.configure(highlightcolor="black")
        self.Button4.configure(pady="0")

        self.Button4.bind("<Button-1>", lambda event: self.dounstabler())
        self.Button4.bind("<ButtonRelease>", lambda event: self.update())
        """---------------------------------------------------------------------------------"""

        s = ttk.Style()
        s.theme_use('default')
        s.configure('my.Horizontal.TScale', background='#d9d9d9',
                    troughcolor='#d9d9d9', sliderlength=15, sliderthickness=20)

        self.TScale1 = ttk.Scale(
            self.top, from_=0, to=255, style='my.Horizontal.TScale')
        self.TScale1.place(relx=0.346, rely=0.554,
                           relheight=0.380, relwidth=0.624)
        self.TScale1.configure(length="70")
        self.TScale1.configure(takefocus="")
        self.TScale1.bind("<B1-Motion>", lambda event: self.setAlpha())
        self.TScale1.bind("<ButtonRelease-1>", lambda event: self.update())
       



    def GiveData(TopGuiSelf):
        return (TopGuiSelf.allwindows,TopGuiSelf.hider,TopGuiSelf.unstabler)

    def start(self):
        self.top.mainloop()
        
    def focusout(TopGuiSelf):
        if TopGuiSelf.canDestroy:
            TopGuiSelf.top.destroy()
            TopGuiSelf.x = -100000000000000000
            TopGuiSelf.y = -100000000000000000
            TopGuiSelf.canDestroy = "xxx"


    def doTop(TopGuiSelf):
        TopGuiSelf.canDestroy = False
        if TopGuiSelf.allwindows[TopGuiSelf.hwnd]["top"]:
            ControlWindow.reset(TopGuiSelf.hwnd)
            TopGuiSelf.allwindows[TopGuiSelf.hwnd]["top"] = False
        else:
            ControlWindow.doTop(TopGuiSelf.hwnd)
            TopGuiSelf.allwindows[TopGuiSelf.hwnd]["top"] = True            

    def doHide(TopGuiSelf):
        TopGuiSelf.canDestroy = False
        if TopGuiSelf.allwindows[TopGuiSelf.hwnd]["hide"]:
            ControlWindow.ShowWindows(TopGuiSelf.hwnd)
            TopGuiSelf.allwindows[TopGuiSelf.hwnd]["hide"]=False
            TopGuiSelf.hider.remove(TopGuiSelf.hwnd)
        else:
            ControlWindow.HideWindows(TopGuiSelf.hwnd)
            TopGuiSelf.allwindows[TopGuiSelf.hwnd]["hide"] = True
            TopGuiSelf.hider.append(TopGuiSelf.hwnd)

    def doDisabled(TopGuiSelf):
        TopGuiSelf.canDestroy = False
        if TopGuiSelf.allwindows[TopGuiSelf.hwnd]["disabled"]:
            ControlWindow.doAbled(TopGuiSelf.hwnd)
            TopGuiSelf.allwindows[TopGuiSelf.hwnd]["disabled"] = False
        else:
            ControlWindow.doDisabled(TopGuiSelf.hwnd)
            TopGuiSelf.allwindows[TopGuiSelf.hwnd]["disabled"] = True
            
    def setAlpha(TopGuiSelf):
        value = 255-int(TopGuiSelf.TScale1.get())
        ControlWindow.setAlpha(TopGuiSelf.hwnd,value)
        TopGuiSelf.allwindows[TopGuiSelf.hwnd]["alpha"] = 255-value    
        TopGuiSelf.setAlphaing = True  
        
    def dounstabler(TopGuiSelf):
        if TopGuiSelf.hwnd in TopGuiSelf.unstabler:
            ControlWindow.setAlpha(TopGuiSelf.hwnd, 255- TopGuiSelf.allwindows[TopGuiSelf.hwnd]["alpha"])
            TopGuiSelf.unstabler.remove(TopGuiSelf.hwnd)
        else:
            TopGuiSelf.unstabler.append(TopGuiSelf.hwnd)

    def delayupdate(TopGuiSelf):
        TopGuiSelf.top.after(100, TopGuiSelf.update())
    
    def update(TopGuiSelf):
        TopGuiSelf.setAlphaing = False
        if not  TopGuiSelf.hwnd in TopGuiSelf.allwindows:
           TopGuiSelf.allwindows[TopGuiSelf.hwnd] = {"top":False,"hide":False,"disabled":False,"alpha":0}

        this = TopGuiSelf.allwindows[TopGuiSelf.hwnd]
        if TopGuiSelf.hwnd in TopGuiSelf.unstabler:
            TopGuiSelf.Button4.configure(image=TopGuiSelf.img4B)
        else:
            TopGuiSelf.Button4.configure(image=TopGuiSelf.img4)
        if this["top"]:
            TopGuiSelf.Button1.configure(image=TopGuiSelf.img1B)
        else:
            TopGuiSelf.Button1.configure(image=TopGuiSelf.img1)
        if this["hide"]:
            TopGuiSelf.Button2.configure(image=TopGuiSelf.img2)
        else:
            TopGuiSelf.Button2.configure(image=TopGuiSelf.img2B)
        if this["disabled"]:
            TopGuiSelf.Button3.configure(image=TopGuiSelf.img3B)
        else:
            TopGuiSelf.Button3.configure(image=TopGuiSelf.img3)
        TopGuiSelf.TScale1.set(this["alpha"])
        try:
            hwnd = win32gui.FindWindow(None, 'Toplevel')
            win32gui.SetForegroundWindow(hwnd)
            ControlWindow.doTop(hwnd)
            TopGuiSelf.canDestroy = True
        except:
            pass

        
if __name__ == "__main__":
    a =tk.Tk()
    a = TopGUI(a,300,300,{"hwnd":[],"hider":[],"allwindows":{},"unstabler":[]})
    a.start()