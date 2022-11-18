#!/usr/bin/env python3
"""
*****************************************************************************
* NET2LIBconverter_windows.py - Version 1.2
* WV/BSR/APPS Internal Tool for SIM2PSPICE effort
* (C) Copyright 2021 Texas Instruments Incorporated. All rights reserved.
* TI Selective Disclosure Source Code - Developed by Henry Kou (h-kou@ti.com)
* Description: 
* Input PSPICE ".net" file into drag and drop. 
* Input entries to populate LIB header and convert.
* Output is PSPICE ".LIB" file in same directory as net input file.
*****************************************************************************
* This source code is subject to change without notice. Texas Instruments
* Incorporated is not responsible for updating this model.
*****************************************************************************
Last edited 11/17/22
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
	global existing_subckt_list
	global requested_subckt_list
	global net_file_path
	global msg_panel
	global subckt_name
	global header_str
	global subckts_str
	global notes_tb
	global window
	global version
	global analog_dict
	global digital_dict
	global misc_dict
	global special_dict

	version = "V1.3"
	
	window = TkinterDnD.Tk()
	window.geometry("500x500")
	window.minsize(500,500)
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

	#dictionary setup
	analog_dict = {}
	digital_dict = {}
	misc_dict = {}
	special_dict = {}

	extract_lib()
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
	# notes_label = tk.Label(notes_panel, text="Notes:", justify = tk.LEFT)
	# notes_label.pack()
	notes_tb = tk.Text(notes_panel, height = 10, width =125, xscrollcommand=scrollx.set, yscrollcommand=scrollb.set )
	scrollb.config(command="yview")
	scrollx.config(command="xview")
	scrollb.pack(side=tk.RIGHT, fill=tk.Y)
	#scrollx.pack(side=tk.BOTTOM,fill=tk.X)
	notes_tb.pack(ipady=10)
	notes_tb.insert(tk.INSERT,"Notes:")
	
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
	version_tmp = version + "   "
	creator = tk.Label(button_panel,text = version_tmp, anchor = 'e')
	creator.grid(column = 2,row = 0, sticky=tk.E)
	#button
	button = tk.Button(button_panel,text="Convert",width=10,height=2,bg="blue",fg="yellow",command=handle_submit, justify=tk.LEFT)
	button.grid(column=1,row=0,padx=0,pady=15, sticky=tk.W)
	window.mainloop()


def handle_submit(): 
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

def extract_lib():
	analog_lib_path = 'lib/SIM2PSPICE_ANALOG.LIB'
	try:
		bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
		analog_lib_path = os.path.abspath(os.path.join(bundle_dir,'lib/SIM2PSPICE_ANALOG.LIB'))
	except:
		pass
	else:
		pass
	digital_lib_path = 'lib/SIM2PSPICE_DIGITAL.LIB'
	try:
		bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
		digital_lib_path = os.path.abspath(os.path.join(bundle_dir,'lib/SIM2PSPICE_DIGITAL.LIB'))
	except:
		pass
	else:
		pass
	misc_lib_path = 'lib/SIM2PSPICE_MISC.LIB'
	try:
		bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
		misc_lib_path = os.path.abspath(os.path.join(bundle_dir,'lib/SIM2PSPICE_MISC.LIB'))
	except:
		pass
	else:
		pass
	special_lib_path = 'lib/SIM2PSPICE_SPECIAL.LIB'
	try:
		bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
		special_lib_path = os.path.abspath(os.path.join(bundle_dir,'lib/SIM2PSPICE_SPECIAL.LIB'))
	except:
		pass
	else:
		pass

	#forming analog library
	analog_file = open(analog_lib_path,"rb")
	analog_file_lines = analog_file.readlines()
	analog_file_str = ""
	for line in analog_file_lines:
		l = line.decode()
		if l[0] != "*" or l[1] == "$":
			#add bc it's either *$ or subckt material
			analog_file_str += l
	#print(analog_file_str)
	
	for subckt in analog_file_str.split("*$"):
		if ".SUBCKT" in subckt:
			words = subckt.split(" ")
			key = words[1]
			#print(key)
			analog_dict.update({key:subckt})
	
	#forming digital library
	digital_file = open(digital_lib_path,"rb")
	digital_file_lines = digital_file.readlines()
	digital_file_str = ""
	for line in digital_file_lines:
		l = line.decode()
		if l[0] != "*" or l[1] == "$":
			#add bc it's either *$ or subckt material
			digital_file_str += l
	for subckt in digital_file_str.split("*$"):
		if ".SUBCKT" in subckt:
			words = subckt.split(" ")
			key = words[1]
			#print(key)
			digital_dict.update({key:subckt})

	#forming misc library
	misc_file = open(misc_lib_path,"rb")
	misc_file_lines = misc_file.readlines()
	misc_file_str = ""
	for line in misc_file_lines:
		l = line.decode()
		if l[0] != "*" or l[1] == "$":
			#add bc it's either *$ or subckt material
			misc_file_str += l
	for subckt in misc_file_str.split("*$"):
		if ".SUBCKT" in subckt:
			words = subckt.split(" ")
			key = words[1]
			#print(key)
			misc_dict.update({key:subckt})

	#forming special library
	special_file = open(special_lib_path,"rb")
	special_file_lines = special_file.readlines()
	special_file_str = ""
	for line in special_file_lines:
		l = line.decode()
		if l[0] != "*" or l[1] == "$":
			#add bc it's either *$ or subckt material
			special_file_str += l
	for subckt in special_file_str.split("*$"):
		if ".SUBCKT" in subckt:
			words = subckt.split(" ")
			key = words[1]
			#print(key)
			special_dict.update({key:subckt})

def extract():
	if net_file_path.get() == "":
		display_msg("No \'.net\' file input","red","warning")
	else:
		net_file = open(net_file_path.get(),"rb")
		net_file_list = net_file.readlines() #list of strings of each line with terminations
		#print(net_file_list)
		pinout_list= [] #holds UTF-8 encoded pinout names
		subckt_list = [] #holds UTF-8 encoded lines of sub ckt
		existing_subckt_list = [] #holds string names of implemented subckts from the net file.
		requested_subckt_list = [] #holds string names of all subckts used in the main subckt of the net file. May include existing subckts or subckts from library.
		#subckt_name.set(net_file_list[0][9:len(net_file_list[0])-2])
		filename = os.path.basename(net_file_path.get())
		filename_header = filename.upper().replace(".NET","")
		subckt_name.set(os.path.splitext(filename)[0])
		i = 0
		begin_subckt_parsing = 0
		for i in range(1,len(net_file_list)): #skip first line of NET 
			#print(net_file_list[i])
			pinout_flag = net_file_list[i][0:17] #recovers .EXTERNAL OUTPUT
			subckt_flag = net_file_list[i][0:7] #recovers .subckt

			#extracting subsubckts
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
					if net_file_list[j][0:7].decode() == ".subckt":
						temp_list = net_file_list[j].decode().split(" ",2)
						existing_subckt_list.append(temp_list[1].upper())
						temp_list[1] = " " + temp_list[1] + " "
						#temp_list[1] = " " + temp_list[1] + "_" + filename_header + " " #adding PSPICE for TI postscript
						for item in temp_list:
							sub_str+=item.upper()

					elif net_file_list[j][0:5].decode() == ".ends":
						#ends_str = "_" + filename_header + "\r\n"
						# print(ends_str)
						#temp_ends = net_file_list[j].decode().replace("\r\n", ends_str) #adding PSPICE for TI postscript
						temp_ends = net_file_list[j].decode()
						sub_str+=temp_ends.upper()

					elif net_file_list[j].decode() != "\r\n":
						sub_str+=net_file_list[j].decode().upper()
				
				single_subckt_list = sub_str.splitlines() #split by line
				model_list = [] 
				for e in range(len(single_subckt_list)):
					list_line = single_subckt_list[e].split(" ")
					for f in range(len(list_line)):
						if list_line[f] == ".MODEL":
							model_list.append(list_line[f+1])
				#print(model_list)
				#at this point Models for subsubckt have been extracted.
				single_subckt_body = ""
				#print(single_subckt_list)
				for i in range(1, len(single_subckt_list) - 1):
					single_subckt_body += single_subckt_list[i] + "\r\n"
				# for item in model_list:
				# 	single_subckt_body = single_subckt_body.replace(item,item+"_"+filename_header)
				sub_str = single_subckt_list[0] + "\r\n" + single_subckt_body + single_subckt_list[len(single_subckt_list)-1] 
				#print(sub_str + "reload")
				h = 0
				while h < len(sub_str)-2: #parse sub list and add to subckts_str
					#print(sub_str[h])
					if sub_str[h].encode() == "\r".encode() and sub_str[h+1].encode() == "\n".encode() and sub_str[h+2].encode() == "+".encode():
						fin_sub_str += ""
						h+=3
					else:
						fin_sub_str += sub_str[h]
						h+=1
				#print(fin_sub_str)
				#fin_sub_str holds subckt models from the original Net.
				subckts_str.set(subckts_str.get() + fin_sub_str + sub_str[len(sub_str)-2] + sub_str[len(sub_str)-1]+"\r\n*$\r\n")		
			#print(pinout_flag)
			if begin_subckt_parsing == 0:
				if pinout_flag == ".EXTERNAL OUTPUT ".encode():
					pinout = net_file_list[i][17:len(net_file_list[i])-2]
					pinout_list.append(pinout)		
				if pinout_flag != ".EXTERNAL OUTPUT ".encode() and net_file_list[i][0:2].decode() != "**" and net_file_list[i][0:2].decode() != "\r\n":
					subckt_list.append(net_file_list[i])
		net_file.close()

		#parses main subckt for subsubckt names. (populates requested_subckt_list)
		for l in subckt_list:
			for w in l.decode().upper().split(" "):
				if "S2P" in w and w not in requested_subckt_list:
					requested_subckt_list.append(w)

		#adding the postscript to applicable subckts and models...
		for f in range(len(subckt_list)):
			splitted_line_list = subckt_list[f].decode().upper().split(" ")
			line = ""
			# for h in range(1,len(splitted_line_list)):
			# 	if splitted_line_list[h] == "PARAMS:":
			# 		splitted_line_list[h-1] = splitted_line_list[h-1] + "_" + filename_header #adding PSPICE for TI postscript
			for element in splitted_line_list:
				temp_line = " " + element
				line += temp_line
			subckt_list[f] = line.encode()
		
		# print(requested_subckt_list)
		# print(existing_subckt_list)
		for r in requested_subckt_list:
			if r not in existing_subckt_list:
				if r in analog_dict:
					#pull from analog lib
					subckts_str.set(subckts_str.get() + analog_dict[r] + "*$")
				elif r in digital_dict:
					#pull from digital lib
					subckts_str.set(subckts_str.get() + digital_dict[r] + "*$")
				elif r in misc_dict:
					#pull from misc lib
					subckts_str.set(subckts_str.get() + misc_dict[r] + "*$")
				elif r in special_dict:
					#pull from special lib
					subckts_str.set(subckts_str.get() + special_dict[r] + "*$")
				else:
					#r not in any lib.... not sure what to do here
					continue
			#else r is in the existing_subckt_list, so we've covered that case

		# print(subckts_str.get())
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
	
	if len(notes_tb.get("1.0","end")) == 1 or notes_tb.get("1.0","end") =="Notes:\n" or notes_tb.get("1.0","end") =="Notes:\r\n":
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
		if len(input) > 80:
			#find pixel to ave character width ratio
			filepath_pixel_x = (len(input)*6)
			geometry_str = str(filepath_pixel_x) + "x525"
			window.geometry(geometry_str)
		else:
			window.geometry("500x525")
		window.minsize(500,525)
		display = tk.Label(msg_panel, text = input, fg=color)
		msg = tk.Label(msg_panel,text = "Uploaded file:", fg=color)
		msg.pack()
	elif type== "converted":
		
		display = tk.Label(msg_panel, text = input, fg=color)
		if len(input) > 80:
			#find pixel to ave character width ratio
			filepath_pixel_x = (len(input)*6)
			geometry_str = str(filepath_pixel_x) + "x525"
			window.geometry(geometry_str)
		else:
			window.geometry("500x525")
		msg = tk.Label(msg_panel,text = "Conversion Success! \'.LIB\' file to location:", fg=color)
		msg.pack()
		window.minsize(500,525)
	else:
		display = tk.Label(msg_panel, text = input, fg=color)
		window.geometry("500x520")
		window.minsize(500,520)
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