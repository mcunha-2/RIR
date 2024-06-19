# Import the tkinter module 
import tkinter as tk
  
window = tk.Tk()
# setting attribute
window.config(cursor="none")
window.overrideredirect(True)
w, h = window.maxsize()
window.geometry(f'{w}x{h}+0+0')
window.configure(background='lime')
# Creating our text widget. 

lbl2 = tk.Label (window, height=h, text="GO", bg="lime", fg="white", font="Mullish 260",wraplength=1, anchor=tk.CENTER)
lbl2.pack()
window.mainloop() 