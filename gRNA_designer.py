import tkinter
from tkinter import filedialog
from functools import partial
import os
from design_library import *
from PIL import Image, ImageTk

def browsefunc(field):
    root.filename =  filedialog.askopenfilename(initialdir = os.getcwd(), title = "Select file",filetypes = (("FASTA files","*.fsa"),("all files","*.*")))
    field.insert(0,root.filename)
    print (root.filename)


def run(label_result, fname, PAM, region, mut_window):
    #button.config(bg='red')
    full_fname1=(fname.get()).strip()
    fname1=full_fname1.split('/')[::-1][0]       # get filename from a fullname
    dir = '/'.join(full_fname1.split('/')[:-1])  # get dirname from a fullname

    PAM1=(PAM.get()).strip()
    region1=int(region.get().strip())
    mut_window1=int(mut_window.get().strip())
    print("\n\nfname1: ",fname1,"\nPAM1: ",PAM1,"\nregion1: ",region1,"\nmut_window1: ",mut_window1)
    run_design(dir, fname1, PAM1, region1, mut_window1)
    label_result.config(text="Done!", font='Helvetica 16 bold')
    return




root = tkinter.Tk()

im = Image.open('Test3.jpg')
tkimage = ImageTk.PhotoImage(im)
myvar=tkinter.Label(root,image = tkimage)
myvar.place(x=0, y=0, relwidth=1, relheight=1)

bg_col='#014F9C'
fg_col="white"
root.configure(background=bg_col)
root.geometry('700x320+100+200')
root.title('CRISPR gRNA designer')


# Code to add widgets will go here...

labelTitle2 = tkinter.Label(root, bg=bg_col, fg=fg_col, font='Kokonor 18 bold', text="CRISPR Cytidine Deaminase").grid(row=0, column=1, padx=5, pady=5)

label1 = tkinter.Label(root, bg=bg_col, fg=fg_col, text="FASTA file with gene: ").grid(row=1, column=0, sticky='E')
label2 = tkinter.Label(root, bg=bg_col, fg=fg_col, text="PAM-sequence: ").grid(row=2, column=0, sticky='E')
label3 = tkinter.Label(root, bg=bg_col, fg=fg_col, text="Target sequence length: ").grid(row=3, column=0, sticky='E')
label4 = tkinter.Label(root, bg=bg_col, fg=fg_col, text="Mutation window: ").grid(row=4, column=0, sticky='E')

fname_str = tkinter.StringVar()
EntryFilename = tkinter.Entry(root, bd=0, text="", textvariable=fname_str)
EntryFilename.grid(row=1, column=1, padx=5, pady=5)
labelResult = tkinter.Label(root, bg=bg_col, fg=fg_col, text=".. result ..")
labelResult.grid(row=5, column=1, padx=5, pady=5)

call_browse = partial(browsefunc, EntryFilename)
browsebutton = tkinter.Button(root, activeforeground='red', bd=0, text="Browse", command=call_browse, width="10")
browsebutton.grid(row=1, column=2)

PAM_str = tkinter.StringVar()
PAM_entry = tkinter.Entry(root, bd=0, textvariable=PAM_str)
PAM_entry.insert(0, "NG")
PAM_entry.grid(row=2, column=1, padx=5, pady=5)

region_str = tkinter.StringVar()
region_entry = tkinter.Entry(root, bd=0, textvariable=region_str)
region_entry.insert(0, "20")
region_entry.grid(row=3, column=1, padx=5, pady=5)

window_str = tkinter.StringVar()
window_entry = tkinter.Entry(root, bd=0, textvariable=window_str)
window_entry.insert(0, "12")
window_entry.grid(row=4, column=1, padx=5, pady=5)



call_result = partial(run, labelResult, fname_str, PAM_str, region_str, window_str)
buttonCal = tkinter.Button(root, bd=0, activeforeground='red', text=" Design gRNAs ", command=call_result)
buttonCal.grid(row=7, column=1)

root.mainloop()
