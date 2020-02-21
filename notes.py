#!/usr/bin/env python3

import os
import os.path

try:
    import tkinter as tk
except:
    os.system('sudo apt-get install -y python3-tk')
    import tkinter as tk
from pathlib import Path


storage_path=os.path.join(Path(__file__).parent.absolute(),'notes.txt')
icon_path=os.path.join(Path(__file__).parent.absolute(),'note.png')


class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        """A text widget that report on internal widget commands"""
        tk.Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, command, *args):
        cmd = (self._orig, command) + args
        result = self.tk.call(cmd)

        if command in ("insert", "delete", "replace"):
            self.event_generate("<<TextModified>>")

        return result

root = tk.Tk()
imgicon = tk.PhotoImage(file=icon_path)
root.tk.call('wm', 'iconphoto', root._w, imgicon)  
root.title('Anotações do Dengo')
label = tk.Label(root, anchor="w")
text = CustomText(root, width=40, height=4, font=('Courier',16), fg='#FFFFFF', bg='#002B36', insertbackground='white' )

if os.path.exists(storage_path):
    text.insert(tk.END, open(storage_path).read())

label.pack(side="bottom", fill="x")
text.pack(side="top", fill="both", expand=True)
label.configure(text="Relaxe, mas não ao ponto de esquecer de ser feliz e bondoso!")

def onModification(event):
    content = event.widget.get("1.0", "end-1c")
    chars = len(content)
    with open(storage_path,'w') as the_file:
        the_file.write(content)

# setStatusBar()
text.bind("<<TextModified>>", onModification)
root.call('wm', 'attributes', '.', '-topmost', '1')
root.mainloop()


