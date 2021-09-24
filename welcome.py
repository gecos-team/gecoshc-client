from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import subprocess
import os
import sys
import gettext
import configparser

config = configparser.ConfigParser()
language = 'es'


def set_locales():
    config.read(os.environ['APPDIR'] + '/etc/helpchannel.conf')

    language = config['i18nConfig']['language']

    try:
        lang = gettext.translation('helpchannel', os.environ['APPDIR'] + '/usr/share/locale', languages=[language])
        lang.install()    
    except IOError:
        print("No translations available")
        _ = gettext.gettext



class WelcomeHC:

    def __init__(self):

        self.name = ''
        self.server = ''
        self.key = ''
        self.file_path = os.environ['HOME'] + '/' + '.hcdata'

        self.getdata()

        root = Tk()

        root.title(_("Connecting to Helpchannel"))

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self.name_strvar = StringVar()
        nombre_entry = ttk.Entry(mainframe, width=18, textvariable=self.name_strvar)
        nombre_entry.grid(column=2, row=2, sticky=(W, E))
        if self.name != '': self.name_strvar.set(self.name)
        
        self.server_strvar = StringVar()
        ip_entry = ttk.Entry(mainframe, width=7, textvariable=self.server_strvar)
        ip_entry.grid(column=2, row=3, sticky=(W, E))
        if self.server != '': self.server_strvar.set(self.server) 

        self.key_strvar = StringVar()
        ip_entry = ttk.Entry(mainframe, width=7, textvariable=self.key_strvar)
        ip_entry.grid(column=2, row=4, sticky=(W, E))
        if self.key != '': self.key_strvar.set(self.key) 

        ttk.Button(mainframe, text=_("Connect"), command=self.validate).grid(
            column=2, row=5, sticky=E)

        ttk.Label(mainframe, text=_("Connection data")).grid(column=1, row=1, sticky=W)
        ttk.Label(mainframe, text=_("Name")).grid(column=1, row=2, sticky=W)
        ttk.Label(mainframe, text=_("Host")).grid(column=1, row=3, sticky=W)
        ttk.Label(mainframe, text=_("Key")).grid(column=1, row=4, sticky=W)

        for child in mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

        nombre_entry.focus()
        root.bind("<Return>", self.validate)

        root.eval('tk::PlaceWindow . center')
        
        root.mainloop()

    def savedata(self):
        # save for persistance
        with open(self.file_path, 'w') as f:
            f.write(self.name + '\n')
            f.write(self.server + '\n')
            f.write(self.key + '\n')

    def getdata(self):

        if os.path.isfile(self.file_path):
            with open(self.file_path, 'r') as f:
                lines = f.readlines()
                if len(lines) >= 2:
                    self.name = lines[0].rstrip('\n')
                    self.server = lines[1].rstrip('\n')
                    self.key = lines[2].rstrip('\n')

    def validate(self, *args):

        ok = True
        
        if str(self.name_strvar.get()) == '':
            messagebox.showerror(
                title='Error',
                message='El nombre de usuario no puede estar vacío.')
            ok = False
        else:
            self.name = str(self.name_strvar.get())

        if str(self.server_strvar.get()) == '':
            messagebox.showerror(
                title='Error',
                message='El servidor no puede estar vacío.')
            ok = False
        else:
            self.server = str(self.server_strvar.get())

        if str(self.key_strvar.get()) == '':
            messagebox.showerror(
                title='Error',
                message='La clave no puede estar vacía.')
            ok = False
        else:
            self.key = str(self.key_strvar.get())

        if ok:
            self.savedata()

            subprocess.call(["python3", os.environ['APPDIR'] + \
                "/usr/bin/helpchannel", self.name, self.server, self.key])


if __name__ == "__main__":

    # set locales
    set_locales()

    app = WelcomeHC()

