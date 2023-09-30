import tkinter as tk
import ControlWindow
import pyautogui
import pickle
import MainGUI

if __name__ == "__main__":
    all = {}
    file = {'hide': []}
    try:
        with open('hider.pickle', 'rb') as f:
            TempFile = pickle.load(f)
        t, h = ControlWindow.getall(True)
        for i in TempFile["hide"]:
            if i  in  h:
                file["hide"].append(i)
                all[i] = {"top":False,"hide":True,"disabled":False,"alpha":0}
    except:
        pass

    with open('hider.pickle', 'wb') as f:
        pickle.dump(file, f)

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

    root = tk.Tk()
    w, h = pyautogui.size()
    x = int(w/2)-170
    y = int(h/2)-120

    a = MainGUI.MainGUI(root, x, y, file,[key1,key2],all)
    a.run()
