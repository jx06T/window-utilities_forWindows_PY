import tkinter as tk
import win32gui
import ControlWindow
import keyboard
import TopGUI
import pyautogui
import time
import win32con
import pickle

class MainGUI():
    def __init__(self, root, x, y, file,keys):
        self.isShowMyself = 0
        self.isShowTopGUI = 0
        self.count = -1

        self.all = {}
        self.titles = []
        self.hwnds = []
        self.unstabler = []
        self.file = file
        self.hider = file["hide"]
        self.keys = keys

        root.geometry("340x240+"+str(x)+"+"+str(y))
        root.title("控制台!")
        root.bind("<Map>", lambda event: self.initial())
        root.protocol("WM_DELETE_WINDOW", self.CloseButton)

        self.window = root

        self.top_frame = tk.Frame(self.window)
        self.top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.scroll_frame = tk.Frame(self.top_frame)
        self.scroll_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.scrollbar = tk.Scrollbar(self.scroll_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.xscrollbar = tk.Scrollbar(self.top_frame, orient=tk.HORIZONTAL)
        self.xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.list_frame = tk.Frame(self.top_frame, height=170)
        # 禁止 Pack geometry manager 改變該 Frame 的大小
        self.list_frame.pack_propagate(False)

        self.list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.mylist = tk.Listbox(
            self.list_frame, yscrollcommand=self.scrollbar.set, xscrollcommand=self.xscrollbar.set, selectmode=tk.SINGLE,selectbackground="gray", selectforeground="white")

        self.scrollbar.config(command=self.mylist.yview,)
        self.xscrollbar.config(command=self.mylist.xview)
        self.mylist.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.mylist.bind("<<ListboxSelect>>", lambda event: self.click1())
        self.mylist.bind("<Double-Button-1>", lambda event: self.click())
        self.mylist.bind("<ButtonRelease-1>", lambda event: self.update())
        '''-----------------------------------------------------------'''
        self.bottom_frame = tk.Frame(self.window, height=30)

        self.label1 = tk.Label(self.bottom_frame, text='...')
        self.label1.pack(side=tk.LEFT)

        self.bottom_frame.pack_propagate(False)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.button = tk.Button(self.bottom_frame, text="Close it", height=20)
        self.button.bind("<Button-1>", lambda event: self.close())
        self.button.pack(side=tk.RIGHT)

        self.window.bind("<FocusOut>", lambda event: self.focusout())
        self.window.after(1000, self.update)
        self.update()

    def run(self):
        self.window.mainloop()

    def focusout(MainGuiSelf):
        MainGuiSelf.isShowMyself = 0
        ControlWindow.HideWindows(MainGuiSelf.myhwnd)

    def click(MainGuiSelf):
        n, = MainGuiSelf.mylist.curselection()  # 取得項目索引值，因為是單選，回傳 (i,)，所以使用 n, 取值

        ControlWindow.ShowWindows(MainGuiSelf.hwnds[n])
        try:
            win32gui.SetForegroundWindow(MainGuiSelf.hwnds[n])
        except:
            pass
        if MainGuiSelf.hwnds[n] in MainGuiSelf.all:
            MainGuiSelf.all[MainGuiSelf.hwnds[n]]["hide"] = False
            if MainGuiSelf.hwnds[n] in MainGuiSelf.hider:
                MainGuiSelf.hider.remove(MainGuiSelf.hwnds[n])

    def click1(MainGuiSelf):
        n, = MainGuiSelf.mylist.curselection()
        ccc = MainGuiSelf.titles[n]
        if MainGuiSelf.hwnds[n] in MainGuiSelf.all:
            if MainGuiSelf.all[MainGuiSelf.hwnds[n]]["hide"]:
                MainGuiSelf.label1.configure(text="(hiding)"+ccc[:15]+"...")
                return
        MainGuiSelf.label1.configure(text=ccc[:20]+"...")
        if ccc == "控制台!":
            MainGuiSelf.b2 = tk.Button(MainGuiSelf.bottom_frame, text="Exit EXE",background="#cc0033")
            MainGuiSelf.b2.pack_propagate(False)
            MainGuiSelf.b2.bind("<Button-1>", lambda event: MainGuiSelf.destroy())
            MainGuiSelf.b2.pack()
        else :
            try:
                MainGuiSelf.b2.pack_forget()
            except:
                pass

    def close(MainGuiSelf):
        n, = MainGuiSelf.mylist.curselection()
        hwnd = MainGuiSelf.hwnds[n]
        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)

    def destroy(MainGuiSelf):
        MainGuiSelf.window.destroy()

    def update(MainGuiSelf):
        MainGuiSelf.window.after(200, MainGuiSelf.update)
        MainGuiSelf.count += 1
        x, y = pyautogui.position()
        if MainGuiSelf.count % 2 == 1:
            for i in MainGuiSelf.unstabler:
                if MainGuiSelf.GUI:
                    if MainGuiSelf.GUI.setAlphaing:
                        continue
                if IsIn(i,x,y):
                    ControlWindow.setAlpha(i,255)
                else :
                    ControlWindow.setAlpha(i, 255- MainGuiSelf.all[i]["alpha"])

        if MainGuiSelf.count % 5 == 0:
            NEWtitles, NEWhwnds = ControlWindow.getall()
            j = 0
            for i in MainGuiSelf.unstabler:
                if i not in NEWhwnds:
                    MainGuiSelf.unstabler.remove(MainGuiSelf.unstabler[j])
                    j -= 1
                j += 1
            if NEWhwnds != MainGuiSelf.hwnds:
                j = 0
                for i in MainGuiSelf.hwnds:
                    if MainGuiSelf.hwnds[j] not in NEWhwnds and MainGuiSelf.hwnds[j] not in MainGuiSelf.hider:
                        MainGuiSelf.mylist.delete(j)
                        MainGuiSelf.hwnds.remove(MainGuiSelf.hwnds[j])
                        MainGuiSelf.titles.remove(MainGuiSelf.titles[j])
                        j -= 1
                    j += 1

                for i in NEWhwnds:
                    if i not in MainGuiSelf.hwnds and i:
                        MainGuiSelf.hwnds.append(i)
                        MainGuiSelf.titles.append(NEWtitles[NEWhwnds.index(i)])
                        MainGuiSelf.mylist.insert(tk.END, NEWtitles[NEWhwnds.index(i)])

            for i in MainGuiSelf.hider:
                if i not in MainGuiSelf.hwnds:
                    MainGuiSelf.hwnds.append(i)
                    MainGuiSelf.titles.append(win32gui.GetWindowText(i))
                    MainGuiSelf.mylist.insert(tk.END, win32gui.GetWindowText(i))

            j = 0
            for i in MainGuiSelf.hwnds:
                if i in NEWhwnds:
                    a1 = NEWtitles[NEWhwnds.index(i)]
                else:
                    a1 = win32gui.GetWindowText(i)
                a2 = MainGuiSelf.titles[j]
                if a1 != a2:
                    MainGuiSelf.mylist.delete(j)
                    MainGuiSelf.mylist.insert(j, a1)
                    MainGuiSelf.titles[j] = a1
                    pass
                j += 1

        '''-------------------------------------------------------------------------------'''
        if MainGuiSelf.isShowTopGUI:
            if MainGuiSelf.TopGUI.canDestroy == "xxx":
                MainGuiSelf.all,MainGuiSelf.hider,MainGuiSelf.unstabler = MainGuiSelf.TopGUI.GiveData()
                store(MainGuiSelf.file,"hide", MainGuiSelf.hider)

        if keyboard.is_pressed(MainGuiSelf.keys[0]):
            hwnd = win32gui.GetForegroundWindow()
            title = win32gui.GetWindowText(hwnd)
            if title == "":
                return
            if MainGuiSelf.isShowTopGUI:
                MainGuiSelf.TopGUI.top.destroy()
                MainGuiSelf.all,MainGuiSelf.hider,MainGuiSelf.unstabler = MainGuiSelf.TopGUI.GiveData()
            
            store(MainGuiSelf.file,"hide", MainGuiSelf.hider)

            MainGuiSelf.isShowTopGUI = True
            MainGuiSelf.TopGUI  = TopGUI.TopGUI(MainGuiSelf.window,x, y,{"hwnd":hwnd,"hider":MainGuiSelf.hider,"allwindows":MainGuiSelf.all,"unstabler":MainGuiSelf.unstabler})

        if keyboard.is_pressed(MainGuiSelf.keys[1]):
            if MainGuiSelf.isShowTopGUI:
                MainGuiSelf.all,MainGuiSelf.hider,MainGuiSelf.unstabler = MainGuiSelf.TopGUI.GiveData()
                store(MainGuiSelf.file,"hide", MainGuiSelf.hider)

            MainGuiSelf.isShowMyself+=1
            if MainGuiSelf.isShowMyself>2:
                return
            
            ControlWindow.movewindows(MainGuiSelf.myhwnd, x, y)
            ControlWindow.ShowWindows(MainGuiSelf.myhwnd)

    def initial(MainGuiSelf):
        MainGuiSelf.myhwnd = win32gui.FindWindow(None, '控制台!')        
        if MainGuiSelf.count < 3:
            ControlWindow.HideWindows(MainGuiSelf.myhwnd)

    def CloseButton(MainGuiSelf):
        ControlWindow.HideWindows(MainGuiSelf.myhwnd)
        


def IsIn(hwnd, x, y):
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    return (x > left and x < right and y < bottom and y > top)

def store(file,n, v):
    file[n] = v
    with open('hider.pickle', 'wb') as f:
        pickle.dump(file, f)
