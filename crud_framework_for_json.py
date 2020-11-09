data_file = 'Data.json'
menu_file = 'Menu.cfg'
fields_file = 'Fields_file.cfg'
updatable_fields_file = 'updatable_fields.cfg'
record = 'Record'
file_not_found = 'File may not exist or Error opening file.'
record_not_found = 'Record not found.'

data = {}

try:
	with open(data_file) as f_data:
		data[record] = f_data.read()
	f_data.close()
	data = eval(data[record])
except SyntaxError:
	with open(data_file, "w") as f_data:
		file = "{'Record' : []}"
		f_data.write(file)
		data = eval(file)
	f_data.close()

try:
	with open(fields_file) as f_fields:
		field_name = f_fields.read()
	f_fields.close()
except Exception:
	print(file_not_found)

field_names = eval(field_name)
try:
	with open(menu_file) as f_menu:
		menu = f_menu.read()
	f_menu.close()
except Exception:
	print(file_not_found)

try:
	with open(updatable_fields_file) as f_updatables:
		updatable_field = f_updatables.read()
	f_updatables.close()
except Exception:
	print(record_not_found)
updatable_fields = eval(updatable_field)

def get_count_of_fields():
	count_of_fields =0 
	for field_name in field_names:
		count_of_fields += 1
	return count_of_fields

count_of_fields = get_count_of_fields()

def get_max_length_of_field_names():
	max_length_of_field_names = len(field_names[0])
	for field_name in field_names:
		if max_length_of_field_names < len(field_name):
			max_length_of_field_names = len(field_name)
	return max_length_of_field_names

max_length_of_field_names = get_max_length_of_field_names()

def create_record():
	field_values = {}
	field_values['Status'] = 'True'
	for field_name in field_names:
		field_value = input("Enter " + field_name + ': ')
		field_values[field_name] = field_value
	data[record].append(field_values)
	save_record()
	print("Record saved successfully.")

def search_record():
	user_input_id = input("Enter " + field_names[0] + " to find: ")
	is_record_found = False
	print_fields()
	for records in data[record]:
		if records[field_names[0]] == user_input_id:
			if records['Status'] == 'True':
				is_record_found = True
				show_record(records)
				print_pipe()
				print("\t")
	if is_record_found == False:
		print('record not found.')


def show_record(records):
	print("|", end ="")
	for field_name in field_names:
		print(2 * " ", end ="")
		print(records[field_name], end = "")
		length_of_field = len(records[field_name])
		spaces = max_length_of_field_names - length_of_field
		print((spaces + 4) * " ", end ="")
		print("|", end = "")
	print("\t")

def display_records():
	print_fields()
	for records in data[record]:
		if records['Status'] == 'True':
			show_record(records)
	print_pipe()
	print("\t")

def update_record():
	user_input_id = input("Enter " + field_names[0] + ' to find: ')
	is_record_found = False
	for records in data[record]:
		if records[field_names[0]] == user_input_id and records['Status'] == 'True':
			is_record_found = True
			counter = 1
			for update_position in updatable_fields:
				print(str(counter) + '. Update ' + field_names[update_position - 1])
				counter += 1
			update_option = int(input("Choose your option: "))
			print("Enter " + field_names[updatable_fields[update_option - 1] - 1] + ': ', end = "")
			records[field_names[updatable_fields[update_option - 1] - 1]] = input()
			save_record()
			print("Record updated successfully.")
			break
	if is_record_found == False:
		print(record_not_found)

def delete_record():
	user_input_id = input("Enter " + field_names[0] + ' to find: ')
	is_record_found = False
	for records in data[record]:
		if records[field_names[0]] == user_input_id and records['Status'] == 'True':
			is_record_found = True
			records['Status'] = 'False'
			save_record()
			print("Record Deleted successfully.")
			break
	if is_record_found == False:
		print(record_not_found)

def save_record():
	with open(data_file, 'w') as data_fie_obj:
		data_fie_obj.write(str(data))
	data_fie_obj.close()

def print_fields():
	print("+", end = "")
	count_of_fields = get_count_of_fields()
	for counter in range(0, int(count_of_fields)):
		pipe = "-" * (max_length_of_field_names + 6)
		print( pipe + "+", end = "")
	print("\t")
	print("|", end ="")
	for counter in range(0, int(count_of_fields)):
		print(2 * " ", end ="")
		print(field_names[counter], end = "")
		length_of_field = len(field_names[counter])
		spaces = max_length_of_field_names - length_of_field
		print((spaces + 4) * " ", end ="")
		print("|", end = "")
	print("\t")
	print("+", end = "")
	for counter in range(0, int(count_of_fields)):
		pipe = "-" * (max_length_of_field_names + 6)
		print( pipe + "+", end = "")
	print("\t")

def print_pipe():
	print("+", end = "")
	for counter in range(0, int(count_of_fields)):
		pipe = "-" * (max_length_of_field_names + 6)
		print( pipe + "+", end = "")

functions = [create_record, display_records, search_record, update_record, delete_record]
while True:
	print(menu)
	try:
		user_option = int(input("Choose your option: "))
	except Exception:
		print("INVALID INPUT.")
		continue
	if user_option == 6:
		exit_option = input("Do you really want to exit? \nPress 'Y' to Exit or 'N' to Continue: ")
		if exit_option.lower() == 'y':
			exit()
	elif user_option > 0 and user_option < 6:
		functions[user_option - 1]()
	else:
		print("INVALID INPUT")
