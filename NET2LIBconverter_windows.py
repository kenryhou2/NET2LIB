#!/usr/bin/env python3
"""
*****************************************************************************
* NET2LIBconverter_windows.py - Version 1.0
* WV/BSR/APPS Internal Tool for SIM2PSPICE effort
* (C) Copyright 2021 Texas Instruments Incorporated. All rights reserved.
* TI Selective Dislosure Source Code - Developed by Henry Kou (h-kou@ti.com)
* Description: 
* Input PSPICE ".net" file into drag and drop. 
* Input entries to populate LIB header and convert.
* Output is PSPICE ".LIB" file in same directory as net input file.
*****************************************************************************
* This source code is subject to change without notice. Texas Instruments
* Incorporated is not responsible for updating this model.
*****************************************************************************
Last edited 12/13 11:40AM
"""
import tkinter as tk
from tkinter.constants import X
from PIL import ImageTk, Image
from tkinterdnd2 import DND_FILES, TkinterDnD
import os
from datetime import date

def main():
	init()

def init():
	#user input window
	#global vars
	global part_entry 
	global date_entry
	global nda_num_entry
	global confidentiality_var
	global model_type_entry
	global simulator_entry
	global sim_vsn_entry
	global lit_num_entry
	global evm_order_entry
	global evm_guide_entry
	global model_vsn_entry
	global pinout_list #holds UTF-8 encoded pinout names
	global subckt_list #holds UTF-8 encoded lines of sub ckt
	global net_file_path
	global msg_panel
	global subckt_name
	global header_str
	global subckts_str
	global notes_tb
	global window
	
	#window setup
	#window = tk.Tk()
	window = TkinterDnD.Tk()
	window.geometry("490x500")
	window.minsize(490,510)
	window.title('NET2LIB Converter - WV/BSR/APPS Internal Tool')
	entry_panel = tk.Frame(window)
	entry_panel.configure()
	dnd_panel = tk.Frame(window)
	button_panel = tk.Frame(window)
	msg_panel = tk.Frame(window)
	msg_panel.pack()
	notes_panel = tk.Frame(window)
	notes_panel.pack(side = tk.BOTTOM, fill = "both")
	button_panel.pack(side = tk.BOTTOM, fill = "both")
	entry_panel.pack(side = tk.LEFT)
	dnd_panel.pack(side = tk.LEFT)
	
	entry_panel.columnconfigure(0,weight=1)
	entry_panel.columnconfigure(1,weight=3)

	entry_panel.rowconfigure(0,weight=1)
	entry_panel.rowconfigure(1,weight=1)
	entry_panel.rowconfigure(2,weight=1)
	entry_panel.rowconfigure(3,weight=1)
	entry_panel.rowconfigure(4,weight=1)
	entry_panel.rowconfigure(5,weight=1)
	entry_panel.rowconfigure(6,weight=1)
	entry_panel.rowconfigure(7,weight=1)

	button_panel.columnconfigure(0,weight=1)
	button_panel.columnconfigure(1,weight=1)
	button_panel.columnconfigure(2,weight=1)


	#entry setup
	part_label = tk.Label(entry_panel,text="GPN:")
	part_label.grid(column=0,row=0,padx=5,pady=5)
	part_entry = tk.Entry(entry_panel)
	CreateToolTip(part_entry, text = 'GPN Entry must be populated')
	part_entry.grid(column=1,row=0,padx=5,pady=5)
	
	confidentiality_label = tk.Label(entry_panel,text = "Confidentiality:")
	confidentiality_label.grid(column=0,row=1,padx=5,pady=5)
	confidentiality_list = ('Selective Disclosure', 'NDA Restriction', 'Public Release')
	confidentiality_var = tk.StringVar()
	subckt_name = tk.StringVar()
	subckts_str = tk.StringVar()
	confidentiality_var.set("Select an option")
	confidentiality_dropdown = tk.OptionMenu(entry_panel,confidentiality_var, *confidentiality_list)
	confidentiality_dropdown.grid(column=1,row=1,padx=5,pady=5)
	CreateToolTip(confidentiality_dropdown, text = 'Must choose an option')

	nda_label = tk.Label(entry_panel,text = "NDA Number:")
	nda_label.grid(column = 0, row=2,padx=5,pady=5)
	nda_num_entry = tk.Entry(entry_panel)
	nda_num_entry.grid(column=1,row=2,padx=5,pady=5)
	CreateToolTip(nda_num_entry, text = 'If NDA Restriction is selected, provide number. Else leave blank.')

	# model_type_label = tk.Label(entry_panel,text = "Model Type:")
	# model_type_label.grid(column=0,row=2,padx=5,pady=5) 
	# model_type_list = ('Transient','Average','Select an option')
	# model_type_entry = tk.StringVar()
	# model_type_entry.set("Select an option")
	# model_type_dropdown = tk.OptionMenu(entry_panel,model_type_entry,*model_type_list)
	# model_type_dropdown.grid(column=1,row=2,padx=5,pady=5)
	# CreateToolTip(model_type_dropdown, text = 'Choose \'Select an option\' if unknown')
	
	sim_vsn_label = tk.Label(entry_panel,text = "PSPICE Version:")
	sim_vsn_label.grid(column=0,row=3,padx=5,pady=5)
	sim_vsn_entry = tk.Entry(entry_panel)
	CreateToolTip(sim_vsn_entry, text = 'Leave blank if unknown')
	sim_vsn_entry.insert(0,"17.4")
	sim_vsn_entry.grid(column=1,row=3,padx=5,pady=5)

	lit_num_label = tk.Label(entry_panel,text = "Datasheet LIT Number:")
	lit_num_label.grid(column=0,row=4,padx=5,pady=5)
	lit_num_entry = tk.Entry(entry_panel)
	CreateToolTip(lit_num_entry, text = 'Leave blank if unknown')
	lit_num_entry.grid(column=1,row=4,padx=5,pady=5)

	evm_order_label = tk.Label(entry_panel,text = "EVM Order Number:")
	evm_order_label.grid(column=0,row=5,padx=5,pady=5)
	evm_order_entry = tk.Entry(entry_panel)
	CreateToolTip(evm_order_entry, text = 'Leave blank if unknown')
	evm_order_entry.grid(column=1,row=5,padx=5,pady=5)
	
	evm_guide_label = tk.Label(entry_panel,text = "EVM User's Guide:")
	evm_guide_label.grid(column=0,row=6,padx=5,pady=5)
	evm_guide_entry = tk.Entry(entry_panel)
	CreateToolTip(evm_guide_entry, text = 'Leave blank if unknown')
	evm_guide_entry.grid(column=1,row=6,padx=5,pady=5)

	model_vsn_label = tk.Label(entry_panel,text = "Model Version:")
	model_vsn_label.grid(column=0,row=7,padx=5,pady=5)
	model_vsn_entry = tk.Entry(entry_panel)
	CreateToolTip(model_vsn_entry, text = 'Leave blank if unknown')
	model_vsn_entry.insert(0,"1.00")
	model_vsn_entry.grid(column=1,row=7,padx=5,pady=5)

	net_file_path = tk.StringVar()
	#drag and drop logo
	path_to_help = 'src/dragndroplogo.png'
	try:
		bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
		path_to_help = os.path.abspath(os.path.join(bundle_dir,'src/dragndroplogo.png'))
	#path = 'dragndroplogo.png'
	except:
		pass
	else:
		pass
	img = Image.open(path_to_help)
	resize_img = img.resize((200, 220), Image.ANTIALIAS)
	img = ImageTk.PhotoImage(resize_img)
	drag_drop_img = tk.Label(dnd_panel, image = img)
	drag_drop_img.pack(fill = "both")
	CreateToolTip(drag_drop_img, text = 'Drag and drop \'.net\' file here')
	#drag and drop should extract path
	drag_drop_img.drop_target_register(DND_FILES)
	drag_drop_img.dnd_bind("<<Drop>>",drop_inside_dnd_box) #event handler for file drop

	#notes text box
	scrollb = tk.Scrollbar(notes_panel)
	#scrollb.pack(side=tk.RIGHT)
	scrollx = tk.Scrollbar(notes_panel, orient=tk.HORIZONTAL)
	#scrollx.pack(side=tk.BOTTOM)
	notes_label = tk.Label(notes_panel, text="Notes:", justify = tk.LEFT)
	notes_label.pack()
	notes_tb = tk.Text(notes_panel, height = 10, width =125, xscrollcommand=scrollx.set, yscrollcommand=scrollb.set )
	scrollb.config(command="yview")
	scrollx.config(command="xview")
	scrollb.pack(side=tk.RIGHT, fill=tk.Y)
	#scrollx.pack(side=tk.BOTTOM,fill=tk.X)
	notes_tb.pack(ipady=10)
	
	#ti logo
	ti_path = 'src/ti_logo.png'
	try:
		bundle_dir1 = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
		ti_path = os.path.abspath(os.path.join(bundle_dir1,'src/ti_logo.png'))
	except:
		pass
	else:
		pass
	img1 = Image.open(ti_path)
	resize_img1 = img1.resize((116, 35), Image.ANTIALIAS)
	img1 = ImageTk.PhotoImage(resize_img1)
	ti_img = tk.Label(button_panel, image = img1, anchor = 'w',justify=tk.LEFT)
	ti_img.grid(column=0,row=0,padx=0,pady=0,sticky=tk.W)
	CreateToolTip(ti_img, text = 'Developed by Henry Kou')

	creator = tk.Label(button_panel,text = "V1.0   ", anchor = 'e')
	creator.grid(column = 2,row = 0, sticky=tk.E)
	#button
	button = tk.Button(button_panel,text="Convert",width=10,height=2,bg="blue",fg="yellow",command=handle_submit, justify=tk.LEFT)
	button.grid(column=1,row=0,padx=0,pady=15, sticky=tk.W)
	window.mainloop()
	

def handle_submit(): 
	#print("submit clicked")
	part = part_entry.get()
	#date = date_entry.get()
	confidentiality = confidentiality_var.get()
	#model_type = model_type_entry.get()
	#simulator = simulator_entry.get()
	sim_vsn = sim_vsn_entry.get()
	lit_num = lit_num_entry.get()
	evm_order = evm_order_entry.get()
	evm_guide = evm_guide_entry.get()
	model_vsn = model_vsn_entry.get

	#parse for acceptability
	if part == "":
		display_msg("Please enter a GPN entry", "red", "warning")
	elif confidentiality == "Select an option":
		display_msg("Please enter a confidentiality option", "red", "warning")
	elif confidentiality == "NDA Restriction" and nda_num_entry.get() == "":
		display_msg("Please enter NDA Number", "red", "warning")
	elif confidentiality != "NDA Restriction":
		if nda_num_entry.get() != ""  and nda_num_entry.get() != "N/A":
			display_msg("Please leave NDA Number blank if not under NDA Restriction", "red", "warning")
		else:
			if sim_vsn_entry.get() == "":
				sim_vsn_entry.insert(0,"17.4")
			if model_vsn_entry.get() == "":
				model_vsn_entry.insert(0,"1.00")
			extract()
	#set defaults
	else:
		if sim_vsn_entry.get() == "":
			sim_vsn_entry.insert(0,"17.4")
		if model_vsn_entry.get() == "":
			model_vsn_entry.insert(0,"1.00")
		extract()

def extract():
	if net_file_path.get() == "":
		display_msg("No \'.net\' file input","red","warning")
	else:
		net_file = open(net_file_path.get(),"rb")
		net_file_list = net_file.readlines() #list of strings of each line with terminations
		#print(net_file_list)
		pinout_list= [] #holds UTF-8 encoded pinout names
		subckt_list = [] #holds UTF-8 encoded lines of sub ckt
		
		#subckt_name.set(net_file_list[0][9:len(net_file_list[0])-2])
		filename = os.path.basename(net_file_path.get())
		subckt_name.set(os.path.splitext(filename)[0])
		i = 0
		begin_subckt_parsing = 0
		for i in range(1,len(net_file_list)): #skip first line of NET 
			#print(net_file_list[i])
			pinout_flag = net_file_list[i][0:17] #recovers .EXTERNAL OUTPUT
			subckt_flag = net_file_list[i][0:7] #recovers .subckt

			#extracting subckts
			if subckt_flag == ".subckt".encode():
				begin_subckt_parsing = 1
				subckt_start_index = i
				subckt_end_index = 0
				end_found = 0
				k = 0
				sub_str = "" #holds subckt contents as one string temporarily
				fin_sub_str = "" #holds subckt contents without "+"
				while k < len(net_file_list)-1 and end_found == 0:
					end_subckt_flag = net_file_list[k+subckt_start_index][0:5] #searching for .ends
					if end_subckt_flag == ".ends".encode():
						subckt_end_index = k+subckt_start_index
						end_found = 1
					k+=1
				for j in range(subckt_start_index,subckt_end_index+1):
					if net_file_list[j].decode() != "\r\n":
						sub_str+=net_file_list[j].decode().upper()
				
				h = 0
				while h < len(sub_str)-3: #parse sub list and add to subckts_str
					#print(sub_str[h])
					if sub_str[h].encode() == "\r".encode() and sub_str[h+1].encode() == "\n".encode() and sub_str[h+2].encode() == "+".encode():
						fin_sub_str += ""
						h+=3
					else:
						fin_sub_str += sub_str[h]
						h+=1
				subckts_str.set(subckts_str.get() + fin_sub_str + "\r\n.$\r\n")		
			#print(pinout_flag)
			if begin_subckt_parsing == 0:
				if pinout_flag == ".EXTERNAL OUTPUT ".encode():
					pinout = net_file_list[i][17:len(net_file_list[i])-2]
					pinout_list.append(pinout)		
				if pinout_flag != ".EXTERNAL OUTPUT ".encode() and net_file_list[i][0:2].decode() != "**" and net_file_list[i][0:2].decode() != "\r\n":
					subckt_list.append(net_file_list[i])
		net_file.close()
		#print(pinout_list)
		#print(subckt_list)
		
		convert(pinout_list,subckt_list,subckts_str.get())
	
def populate_header():
	curr_dir = os.getcwd()
	template_file_path = curr_dir + "/templates/ModelHeader_Public_Release.txt"
	try:
		bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
		template_file_path = os.path.abspath(os.path.join(bundle_dir,'templates/ModelHeader_Public_Release.txt'))
	#path = 'dragndroplogo.png'
	except:
		pass
	else:
		pass
	template_file = open(template_file_path,"rb")
	template_file_list =template_file.readlines()
	header_str = template_file_list[0].decode()
	header_str += "* GPN: "+ part_entry.get() + "\r\n"
	header_str += template_file_list[2].decode() + template_file_list[3].decode()
	if confidentiality_var.get() == "Selective Disclosure":
		header_str+= "* TI Confidential - Selective Disclosure\r\n"
	elif confidentiality_var.get() == "NDA Restriction":
		header_str+="* TI Confidential - NDA Restrictions per NDA# " + nda_num_entry.get() + "\r\n"
	elif confidentiality_var.get() == "Public Release":
		pass
	for i in range(4,16):
		header_str+=template_file_list[i].decode()
	today = date.today()
	d1 = today.strftime("%m/%d/%Y")
	simvsn = sim_vsn_entry.get()
	if sim_vsn_entry.get() == "":
		simvsn = "N/A"
	litnum = lit_num_entry.get()
	if lit_num_entry.get() == "":
		litnum = "N/A"
	evmorder = evm_order_entry.get()
	if evm_order_entry.get() == "":
		evmorder = "N/A"
	evmguide = evm_guide_entry.get()
	if evm_guide_entry.get() == "":
		evmguide = "N/A"
	modelvsn = model_vsn_entry.get()
	if model_vsn_entry.get() == "":
		modelvsn = "N/A"
	header_str+= "* Part: " + part_entry.get() + "\r\n* Date: " + d1 + "\r\n" + "* Model Type: TRANSIENT\r\n* Simulator: PSPICE\r\n* Simulator Version: " + simvsn + "\r\n* Datasheet LIT number: " + litnum + "\r\n* EVM Order Number: " + evmorder + "\r\n* EVM User's Guide: " + evmguide + "\r\n* Model Version: " + modelvsn + "\r\n"  
	for i in range(25,27):
		header_str+=template_file_list[i].decode()
	notes_list = []
	bypass_notes = 0
	if len(notes_tb.get("1.0","end")) == 1:
		bypass_notes = 1
	if bypass_notes == 0:
		if notes_tb.get("end-1c","end") == "\n":
			notes_list = notes_tb.get("1.0","end").split("\n")
		elif notes_tb.get("end-1c","end") == "\r\n":
			notes_list = notes_tb.get("1.0","end").split("\r\n")
		for line in notes_list:
			header_str += "* " + line + "\r\n"
	header_str+=template_file_list[25].decode()
	return header_str


def convert(pins,subckt_body,subckts):
	converted_output_str = populate_header()
	subckt_name_str = str(subckt_name.get()).upper()
	converted_filename = subckt_name_str + ".LIB"
	converted_output_str += "*$\r\n.SUBCKT " + subckt_name_str
	for i in pins:
		pin_line = " " + i.decode()
		converted_output_str+=pin_line
	converted_output_str+="\r\n"
	for line in subckt_body:
		converted_output_str+=line.decode()
	converted_output_str+=".ENDS " + subckt_name_str + "\r\n*$\r\n"
	converted_output_str += subckts
	converted_output_b = converted_output_str.encode()
	converted_dir = os.path.split(net_file_path.get())[0]
	tmp_filepath = str(converted_dir) + "/" + converted_filename
	converted_file = open(tmp_filepath,"wb")
	converted_file.write(converted_output_b)
	converted_file.close()
	display_msg(tmp_filepath,"green","converted")
	reset()

	
class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                      background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

def drop_inside_dnd_box(event):
	#dropped_file_path = event.data[1:len(event.data)-1]
	dropped_file_path = event.data.replace("{","").replace("}","")
	#print(dropped_file_path)
	#check for net file
	extension = dropped_file_path[len(dropped_file_path)-4:len(dropped_file_path)]
	#print(extension)
	net_file_path.set("")
	if extension != ".net" and extension != ".NET":
		display_msg("Please use file with extension \'.net\'","red","warning")
	else:
		net_file_path.set(dropped_file_path)
		#print("Net file detected")
		display_msg(net_file_path.get(),"green","notification")
		#print(net_file_path.get())

def display_msg(input, color,type):
	for widget in msg_panel.winfo_children():
		widget.destroy()
	if type == "notification":
		display = tk.Label(msg_panel, text = input, fg=color)
		msg = tk.Label(msg_panel,text = "Uploaded file:", fg=color)
		msg.pack()
		window.geometry("490x535")
		window.minsize(490,535)
	elif type== "converted":
		display = tk.Label(msg_panel, text = input, fg=color)
		msg = tk.Label(msg_panel,text = "Converted \'.LIB\' file to location:", fg=color)
		msg.pack()
		window.geometry("490x520")
		window.minsize(490,520)
	else:
		display = tk.Label(msg_panel, text = input, fg=color)
		window.geometry("490x520")
		window.minsize(490,520)
	display.pack()
	

def reset():
	#print("reset")
	net_file_path.set("")
	part_entry.insert(0,"")
	nda_num_entry.insert(0,"")
	sim_vsn_entry.insert(0,"")
	lit_num_entry.insert(0,"")
	evm_order_entry.insert(0,"")
	evm_guide_entry.insert(0,"")
	model_vsn_entry.insert(0,"")
	subckts_str.set("")

if __name__ == "__main__":
	main()