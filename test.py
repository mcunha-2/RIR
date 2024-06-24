import tkinter as tk

class UI():
	def __init__(self):
		self.window = tk.Tk()
		# setting attribute
		self.window.config(cursor="none")
		self.window.overrideredirect(True)
		w, self.h = self.window.maxsize()
		self.window.geometry(f'{w+20}x{self.h+30}+0+0')
		self.lbl = tk.Label()
		self.show_main_screen()

	def show_main_screen(self):
		self.window.configure(background='black')
		self.lbl.destroy()

	def show_accepted_screen(self, inside):
		self.window.configure(background='lime')
		if(inside):
			self.lbl = tk.Label (self.window, height=self.h, text="EXIT", bg="lime", fg="white", font="Mullish 100", anchor=tk.CENTER)
		else:
			self.lbl = tk.Label (self.window, height=self.h, text="GO", bg="lime", fg="white", font="Mullish 100", anchor=tk.CENTER)
		self.lbl.pack()

	def show_rejected_screen(self, full, same_day):
		self.window.configure(background='#ff2c00')
		if(full):
			self.lbl = tk.Label (self.window, height=self.h, text="STAND\nFULL", bg="#ff2c00", fg="white", font="Mullish 100", anchor=tk.CENTER)
		elif(same_day):
			self.lbl = tk.Label (self.window, height=self.h, text="COME\nBACK\nNEXT\nDAY", bg="#ff2c00", fg="white", font="Mullish 100", anchor=tk.CENTER)
		else:
			self.lbl = tk.Label (self.window, height=self.h, text="NO\nACCESS", bg="#ff2c00", fg="white", font="Mullish 100", anchor=tk.CENTER)
		self.lbl.pack()

	def show_access_screen(self, add):
		if(add): 
			self.lbl = tk.Label (self.window, height=self.h, text="\u2714", bg="blue", fg="white", font="Mullish 300", anchor=tk.CENTER)
		else:
			self.lbl = tk.Label (self.window, height=self.h, text="\u274C", bg="blue", fg="white", font="Mullish 300", anchor=tk.CENTER)
		self.lbl.pack()
		self.window.configure(background='blue')

	def show_interaction_screen(self, screen):
		match screen:
			case 1:
				self.window.configure(background='blue')
				self.lbl = tk.Label (self.window, height=self.h, text="ADD", bg="blue", fg="white", font="Mullish 100", anchor=tk.CENTER)
			case 2:
				self.window.configure(background='blue')
				self.lbl = tk.Label (self.window, height=self.h, text="REMOVE", bg="blue", fg="white", font="Mullish 100", anchor=tk.CENTER)
			case 3:
				self.window.configure(background='blue')
				self.lbl = tk.Label (self.window, height=self.h, text="RESET", bg="blue", fg="white", font="Mullish 100", anchor=tk.CENTER)
			case _:
				return
		self.lbl.pack()

	def wait(self):
		var = tk.IntVar()
		self.window.after(2000, var.set, 1)
		self.window.wait_variable(var)



if __name__=="__main__":

	ui = UI()
	count = 0
	while(True):
		ui.window.update_idletasks()
		ui.window.update()
		print("write")
		inp = input()

		if(inp == "1"):
			if(count == 3):
				count = 0
				continue
			count += 1
			print("count", count)
			ui.show_interaction_screen(count)
		if(count != 0):

		
		ui.wait()