#!/usr/bin/env python3

import datetime
import sqlite3
import tkinter as tk
from gpiozero import Button
from smartcard.System import readers
from smartcard.util import toHexString

from config import *

class NFCReader():

	def __init__(self):
		available_readers = readers()
		if not available_readers:
			raise Exception("No smart card readers found")

		self.reader = available_readers[0]
		self.connection = self.reader.createConnection()

	def read_uid(self):
		try:
			self.connection.connect()
		except:
			return
		SELECT = [0xFF, 0xCA, 0x00, 0x00, 0x00]
		data, sw1, sw2 = self.connection.transmit(SELECT)

		if(sw1, sw2) == (0x90, 0x00):
			nfc_Id = "".join('{:02x}:'.format(data[i])
					for i in range(len(data)))[:-1]
			# get rid of trailing whitespaces
			nfc_Id = nfc_Id.rstrip().upper()
			print(nfc_Id)
			return nfc_Id


class SQL_Data():
	def __init__(self):
		self.max_capacity = MAX_CAPACITY
		self.capacity_buffer = CAPACITY_BUFFER
		self.con = sqlite3.connect("/home/sibs/Documents/RIR/RIR.db")
		self.cur = self.con.cursor()

	def check_uid_access(self, uid):
		res = self.cur.execute("SELECT has_Access FROM access WHERE uid=(?)", (uid,)).fetchone()
		return not(res is None) and res[0] != 0
	
	def check_if_uid_exists(self, uid):
		res = self.cur.execute("SELECT uid FROM access WHERE uid=(?)", (uid,)).fetchone()
		return not(res is None)
		
	def add_uid(self, uid):
		self.cur.execute("INSERT INTO access VALUES(?, 1,0)", (uid,))
		self.con.commit()

	def log_access(self, uid, state):
		self.cur.execute("INSERT INTO accessLog VALUES(?, ?,?)", (uid, state, datetime.datetime.now(datetime.timezone.utc)))
		self.con.commit()

	def check_if_inside(self, uid):
		is_inside = self.cur.execute("SELECT is_inside FROM access WHERE uid=(?)", (uid,)).fetchone()[0]
		return is_inside

	def get_current_capacity(self):
		return self.cur.execute("SELECT count(*) FROM access WHERE is_inside='1'").fetchone()[0]

	def has_available_space(self):
		return self.get_current_capacity() < self.max_capacity * (1-self.capacity_buffer)

	def toggle_inside(self, uid):
		is_inside = self.cur.execute("SELECT is_inside FROM access WHERE uid=(?)", (uid,)).fetchone()[0]
		self.cur.execute("UPDATE access SET is_inside = (?) WHERE uid=(?)", (not is_inside, uid))
		self.con.commit()
		self.log_access(uid, not is_inside)
		return is_inside

	def toggle_access(self, uid, value):
		self.cur.execute("UPDATE access SET has_Access = (?) WHERE uid=(?)", (value, uid))
		self.con.commit()

	def check_same_day_access(self, uid):
		dt = datetime.datetime.now(datetime.timezone.utc)
		dt = datetime.datetime(dt.year, dt.month, dt.day, 8)
		access_time = self.cur.execute("SELECT timestamp FROM accessLog WHERE timestamp>=(?) AND uid=(?) AND is_inside=0 ORDER BY timestamp DESC", (dt, uid)).fetchone()
		if(access_time is None):
			return not(access_time is None)
		reset_time = self.cur.execute("SELECT timestamp FROM accessLog WHERE timestamp>=(?) AND uid=(?) AND is_inside=2", (access_time[0], uid)).fetchone()
		return not(access_time is None) and reset_time is None
	
	def reset_inside(self):
		self.cur.execute("UPDATE access SET is_inside = 0")
		self.con.commit()

class UI():
	def __init__(self):
		self.window = tk.Tk()
		# setting attribute
		self.window.config(cursor="none")
		self.window.overrideredirect(True)
		self.window.attributes('-fullscreen', True)
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

	def show_reset_screen(self):
		self.lbl = tk.Label (self.window, height=self.h, text="RESET", bg="blue", fg="white", font="Mullish 100", anchor=tk.CENTER)
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
		self.window.after(WAIT_TIME, var.set, 1)
		self.window.wait_variable(var)


if __name__=="__main__":
	nfc_reader = NFCReader()

	ui = UI()
	sql = SQL_Data()
	count = 0
	last_uid = ''
	while(True):
		ui.window.update_idletasks()
		ui.window.update()
		
		uid = nfc_reader.read_uid()

		if(uid is None or last_uid == uid):
			continue
		ui.show_main_screen()
		if(uid == MASTER_KEY):
			count += 1
			if(count == 4):
				count = 0
				continue
			ui.show_interaction_screen(count)
			continue
		if(count != 0):
			match count:
				case 1:
					if(not sql.check_if_uid_exists(uid)):
						sql.add_uid(uid)
					else:
						sql.toggle_access(uid, 1)
					sql.log_access(uid, 2)
					ui.show_access_screen(True)
				case 2:
					sql.toggle_access(uid, 0)
					ui.show_access_screen(False)
				case 3:
					sql.reset_inside()
					ui.show_reset_screen()
			count = 0
			ui.wait()
			ui.show_main_screen()
			continue
		if(not(sql.check_uid_access(uid))):
			ui.show_rejected_screen(0, 0)
			ui.wait()
			ui.show_main_screen()
			continue
		if(sql.check_if_inside(uid)):
			inside = sql.toggle_inside(uid)
			ui.show_accepted_screen(inside)
			ui.wait()
			ui.show_main_screen()
			continue
		if(sql.check_same_day_access(uid)):
			ui.show_rejected_screen(0, 1)
			ui.wait()
			ui.show_main_screen()
			continue
		if(not(sql.has_available_space())):
			ui.show_rejected_screen(1, 0)
			ui.wait()
			ui.show_main_screen()
			continue
		

		inside = sql.toggle_inside(uid)
		ui.show_accepted_screen(inside)

		ui.wait()
		ui.show_main_screen()
