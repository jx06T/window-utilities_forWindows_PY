import tkinter as tk
import win32gui
import ControlWindow
import keyboard
import TopGUI
import win32con
from pynput import mouse
import threading

class MainGUI():
    def __init__(self, root, x, y, file,keys,all):
        print(keys)
        self.isShowMyself = 0
        self.isShowTopGUI = 0
        self.isFast = False
        self.count = -1

        self.all = all
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

        # self.window.bind("<FocusOut>", lambda event: self.focusout())
        self.window.after(500, self.update)
        self.update()


        def on_click(x, y, button, pressed):
            if self.isShowMyself == "xxx":
                return False
            if pressed:
                if self.isShowTopGUI:
                    if (x<self.TopGUI.x or x>self.TopGUI.x+120 or y<self.TopGUI.y or y>self.TopGUI.y+70 ):
                        self.TopGUI.focusout()

                # if self.isShowMyself==1:
                    # if not IsIn(self.myhwnd,x,y):
                        # self.focusout()

        def mouse_listener_thread():
            with mouse.Listener(on_click=on_click) as listener:
                listener.join() 

        # 启动鼠标监听线程
        mouse_thread = threading.Thread(target=mouse_listener_thread)
        mouse_thread.start()

    def run(self):
        self.window.mainloop()

    def focusout(MainGuiSelf):
        ControlWindow.HideWindows(MainGuiSelf.myhwnd)
        MainGuiSelf.isShowMyself = 0

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
            TopGUI.store("hide", MainGuiSelf.hider)

    def click1(MainGuiSelf):
        n, = MainGuiSelf.mylist.curselection()
        ccc = MainGuiSelf.titles[n]
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

        if MainGuiSelf.hwnds[n] in MainGuiSelf.all:
            if MainGuiSelf.all[MainGuiSelf.hwnds[n]]["hide"]:
                MainGuiSelf.label1.configure(text="(hiding)"+ccc[:15]+"...")
                return
        MainGuiSelf.label1.configure(text=ccc[:20]+"...")

    def close(MainGuiSelf):
        n, = MainGuiSelf.mylist.curselection()
        hwnd = MainGuiSelf.hwnds[n]
        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)

    def destroy(MainGuiSelf):
        MainGuiSelf.isShowMyself = "xxx"
        MainGuiSelf.window.destroy()

    def update(MainGuiSelf):
        MainGuiSelf.window.after(200, MainGuiSelf.update)
        MainGuiSelf.count += 1
        x, y = mouse.Controller().position
        # x, y = pyautogui.position()
        if MainGuiSelf.count % 2 == 1:
            for i in MainGuiSelf.unstabler:
                if MainGuiSelf.isShowTopGUI:
                    if MainGuiSelf.TopGUI.setAlphaing:
                        continue
                if IsIn(i,x,y):
                    ControlWindow.setAlpha(i,255)
                else :
                    ControlWindow.setAlpha(i, 255- MainGuiSelf.all[i]["alpha"])

        if MainGuiSelf.count % 4 == 0:
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
                MainGuiSelf.TopGUI.canDestroy = False

        if keyboard.is_pressed(MainGuiSelf.keys[0]):
            hwnd,title  = ControlWindow.GetNowWindows()
            if title == "Program Manager" or  title == "":
                return
            if MainGuiSelf.isShowTopGUI:
                if abs(x-MainGuiSelf.TopGUI.x)<50 and abs(y-MainGuiSelf.TopGUI.y)<50:
                    return    
                MainGuiSelf.TopGUI.top.destroy()
                MainGuiSelf.all,MainGuiSelf.hider,MainGuiSelf.unstabler = MainGuiSelf.TopGUI.GiveData()

            MainGuiSelf.isShowTopGUI = True
            MainGuiSelf.TopGUI  = TopGUI.TopGUI(MainGuiSelf.window,x, y,{"hwnd":hwnd,"hider":MainGuiSelf.hider,"allwindows":MainGuiSelf.all,"unstabler":MainGuiSelf.unstabler})

        if keyboard.is_pressed(MainGuiSelf.keys[1]):
            if MainGuiSelf.isShowMyself ==-1:
                MainGuiSelf.focusout()
                MainGuiSelf.isShowMyself = -2
                return

            if not MainGuiSelf.isShowMyself == 0 :
                return

            MainGuiSelf.isShowMyself = 2
            ControlWindow.doTop(MainGuiSelf.myhwnd)
            ControlWindow.movewindows(MainGuiSelf.myhwnd, x, y)
            ControlWindow.ShowWindows(MainGuiSelf.myhwnd)

        if MainGuiSelf.isShowMyself== -2 and not keyboard.is_pressed(MainGuiSelf.keys[1]):
            MainGuiSelf.isShowMyself=0

        if MainGuiSelf.isShowMyself== 2 and not keyboard.is_pressed(MainGuiSelf.keys[1]):
            MainGuiSelf.isShowMyself=-1

        iskey2 = False
        iskey3 = False
        try:
            iskey2 = keyboard.is_pressed(MainGuiSelf.keys[2])
        except:
            pass

        try:
            iskey3 = keyboard.is_pressed(MainGuiSelf.keys[3])
        except:
            pass

        if  iskey2 or iskey3 :
            hwnd,title  = ControlWindow.GetNowWindows()
            if title == "Program Manager" or title == "" or MainGuiSelf.isFast:
                return
            MainGuiSelf.isFast = True
            if MainGuiSelf.isShowTopGUI:
                MainGuiSelf.TopGUI.top.destroy()
                MainGuiSelf.all,MainGuiSelf.hider,MainGuiSelf.unstabler = MainGuiSelf.TopGUI.GiveData()
                MainGuiSelf.isShowTopGUI = False
                
            MainGuiSelf.TopGUI  = TopGUI.TopGUI(None,x, y,{"hwnd":hwnd,"hider":MainGuiSelf.hider,"allwindows":MainGuiSelf.all,"unstabler":MainGuiSelf.unstabler})
            if iskey2:
                MainGuiSelf.TopGUI.doTop()
            else:        
                MainGuiSelf.TopGUI.doHide()
            MainGuiSelf.all,MainGuiSelf.hider,MainGuiSelf.unstabler = MainGuiSelf.TopGUI.GiveData()

        if MainGuiSelf.isFast and not iskey2 and not iskey3:
            MainGuiSelf.isFast = False

    def initial(MainGuiSelf):
        MainGuiSelf.myhwnd = win32gui.FindWindow(None, '控制台!')        
        if MainGuiSelf.count < 3:
            ControlWindow.HideWindows(MainGuiSelf.myhwnd)

    def CloseButton(MainGuiSelf):
        MainGuiSelf.isShowMyself = 0
        ControlWindow.HideWindows(MainGuiSelf.myhwnd)
        


def IsIn(hwnd, x, y):
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    return (x > left and x < right and y < bottom and y > top)
