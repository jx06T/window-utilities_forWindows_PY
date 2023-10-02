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
    print(file)
    keys = ["ctrl+alt+d","ctrl+alt+s","ctrl+alt+t","ctrl+alt+h"]
    try:
        f = open('hotkey.text', encoding='UTF-8')
        allText = (f.read()).split("\n")
        keys[0] = allText[1]
        keys[1] = allText[3]
        keys[2] = allText[5]
        keys[3] = allText[7]
    except:
        with open('hotkey.text', 'a+', encoding='UTF-8') as f:
            f.write("display tool:\nctrl+alt+d\ndisplay control panel:\nctrl+alt+s\nsticky window:\nctrl+alt+t\ninvisible window:\nctrl+alt+h")

    root = tk.Tk()
    w, h = pyautogui.size()
    x = int(w/2)-170
    y = int(h/2)-120

    a = MainGUI.MainGUI(root, x, y, file,keys,all)
    a.run()
