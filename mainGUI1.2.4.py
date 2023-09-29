import tkinter as tk
import win32gui
import ControlWindow
import keyboard
import ShowGUI
import pyautogui
import time
import win32con
import pickle


class mainwindow():
    def __init__(self, root, x, y, h):
        # self.ishind = True
        self.all = {}
        self.hinder = h
        self.titles = []
        self.hwnds = []
        self.unstabler = []
        self.count = -1
        self.istop = False
        self.GUI = False
        root.geometry("340x240+"+str(x)+"+"+str(y))
        root.title("控制台!")
        root.bind("<Map>", lambda event: self.initial())
        root.protocol("WM_DELETE_WINDOW", self.hh)
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

        self.update()

        self.scrollbar.config(command=self.mylist.yview,)
        self.xscrollbar.config(command=self.mylist.xview)
        self.mylist.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.mylist.bind("<<ListboxSelect>>", lambda event: self.click1())
        self.mylist.bind("<Double-Button-1>", lambda event: self.click())
        self.mylist.bind("<ButtonRelease-1>", lambda event: self.update())
        self.window.after(1000, self.update)
        '''-----------------------------------------------------------'''
        self.bottom_frame = tk.Frame(self.window, height=30)

        self.label1 = tk.Label(self.bottom_frame, text='...')
        self.label1.pack(side=tk.LEFT)

        self.bottom_frame.pack_propagate(False)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.button = tk.Button(self.bottom_frame, text="Close it", height=20)
        self.button.bind("<Button-1>", lambda event: self.close())
        self.button.pack(side=tk.RIGHT)

    def run(self):
        self.window.mainloop()

    def click(a):
        n, = a.mylist.curselection()  # 取得項目索引值，因為是單選，回傳 (i,)，所以使用 n, 取值

        ControlWindow.ShowWindows(a.hwnds[n])
        try:
            win32gui.SetForegroundWindow(a.hwnds[n])
        except:
            pass
        if a.hwnds[n] in a.all:
            a.all[a.hwnds[n]]["hind"] = False
            if a.hwnds[n] in a.hinder:
                a.hinder.remove(a.hwnds[n])

    def click1(a):
        n, = a.mylist.curselection()
        ccc = a.titles[n]
        if a.hwnds[n] in a.all:
            if a.all[a.hwnds[n]]["hind"]:
                a.label1.configure(text="(hiding)"+ccc[:15]+"...")
                return
        a.label1.configure(text=ccc[:20]+"...")
        if ccc == "控制台!":
            a.b2 = tk.Button(a.bottom_frame, text="Exit EXE",background="#cc0033")
            a.b2.pack_propagate(False)
            a.b2.bind("<Button-1>", lambda event: a.destroy())
            a.b2.pack()
        else :
            try:
                # a.b2.destroy()
                a.b2.pack_forget()
            except:
                pass
    def close(a):
        n, = a.mylist.curselection()
        hwnd = a.hwnds[n]
        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)

    def destroy(a):
        a.window.destroy()

    def update(a):
        a.window.after(50, a.update)
        a.count += 1
        x, y = pyautogui.position()
        if a.count % 8 == 1:
            for i in a.unstabler:
                if a.GUI:
                    if a.GUI.setAlphaing:
                        continue
                if IsIn(i,x,y):
                    ControlWindow.setAlpha(i,255)
                else :
                    ControlWindow.setAlpha(i, 255- a.all[i]["alpha"])
        if a.count % 20 == 0:
            NEWtitles, NEWhwnds = getall()
            j = 0
            for i in a.unstabler:
                if i not in NEWhwnds:
                    a.unstabler.remove(a.unstabler[j])
                    j -= 1
                j += 1
            if NEWhwnds != a.hwnds:
                j = 0
                for i in a.hwnds:
                    if a.hwnds[j] not in NEWhwnds and a.hwnds[j] not in a.hinder:
                        a.mylist.delete(j)
                        a.hwnds.remove(a.hwnds[j])
                        a.titles.remove(a.titles[j])
                        j -= 1
                    j += 1

                for i in NEWhwnds:
                    if i not in a.hwnds and i:
                        a.hwnds.append(i)
                        a.titles.append(NEWtitles[NEWhwnds.index(i)])
                        a.mylist.insert(tk.END, NEWtitles[NEWhwnds.index(i)])

            for i in a.hinder:
                if i not in a.hwnds:
                    a.hwnds.append(i)
                    a.titles.append(win32gui.GetWindowText(i))
                    a.mylist.insert(tk.END, win32gui.GetWindowText(i))

            j = 0
            for i in a.hwnds:
                if i in NEWhwnds:
                    a1 = NEWtitles[NEWhwnds.index(i)]
                else:
                    a1 = win32gui.GetWindowText(i)
                a2 = a.titles[j]
                if a1 != a2:
                    a.mylist.delete(j)
                    a.mylist.insert(j, a1)
                    a.titles[j] = a1
                    pass
                j += 1

        '''-------------------------------------------------------------------------------'''
        if a.GUI:
            if a.GUI.canDestroy == "xxx":
                a.all = a.GUI.windows
                a.hinder = a.GUI.hinder
                a.unstabler = a.GUI.unstabler
                a.istop = False
                a.GUI = False
                store("hide", a.hinder)
        if keyboard.is_pressed(key1):
            if a.istop:
                return
            hwnd = win32gui.GetForegroundWindow()
            title = win32gui.GetWindowText(hwnd)
            # print(hwnd,title)
            if title == "":
                return
            a.istop = True
            a.GUI = ShowGUI.TopGUI(x, y, a.window, hwnd,
                                   a.all, a.hinder, a.unstabler)

        if keyboard.is_pressed(key2):
            if a.GUI != False:
                a.all = a.GUI.windows
                a.hinder = a.GUI.hinder
                a.unstabler = a.GUI.unstabler
                store("hide", a.hinder)
                del a.GUI
                a.istop = False
                a.GUI = False
            a.atimes = 0 
            ControlWindow.movewindows(a.myhwnd, x, y)
            ControlWindow.ShowWindows(a.myhwnd)
            try:
                win32gui.SetForegroundWindow(a.myhwnd)
            except:
                pass

    def initial(a):
        a.myhwnd = win32gui.FindWindow(None, '控制台!')
        # print(a.count)
        if a.count < 3:
            ControlWindow.HindWindows(a.myhwnd)
            # a.ishind = True

    def hh(a):
        ControlWindow.HindWindows(a.myhwnd)
        # a.ishind = True


def foo(hwnd, mouse):
    global titles
    global hwnds
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) != "":
        titles.append(win32gui.GetWindowText(hwnd))
        hwnds.append(hwnd)


def getall():
    global titles
    global hwnds
    titles = []
    hwnds = []
    win32gui.EnumWindows(foo, 0)
    return (titles, hwnds)


def store(n, v):
    file[n] = v
    with open('hinder.pickle', 'wb') as f:
        pickle.dump(file, f)


def IsIn(hwnd, x, y):
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    return (x > left and x < right and y < bottom and y > top)


file = {'hide': []}
try:
    with open('hinder.pickle', 'rb') as f:
        file = pickle.load(f)
    t, h = getall()
    for i in file["hind"]:
        if i not in h:
            file["hind"].remove(i)
            print("s")
except:
    pass
key1 = "ctrl+alt+d"
key2 = "ctrl+alt+s"
try:

    f = open('hotkey.text', encoding='UTF-8')
    allText = (f.read()).split("\n")
    key1 = allText[1]
    key2 = allText[3]
except:
    with open('hotkey.text', 'a+', encoding='UTF-8') as f:
        f.write("display tool:\nctrl+alt+d\ndisplay control panel:\nctrl+alt+s")
if __name__ == "__main__":
    root = tk.Tk()
    w, h = pyautogui.size()
    x = int(w/2)-170
    y = int(h/2)-120

    a = mainwindow(root, x, y, file["hide"])
    a.run()
