import re
import sys

def tokenizer(pstr):
    token_list = list()
    token_list = re.split(r' ', pstr)
    token_list = filter(None, token_list)
    #print(token_list)
    return token_list;

def get_function_detail(line):
    ln_tokens = tokenizer(line) 
    sub_token = tokens[3].split("(")
    #print(sub_token)
    if len(sub_token) > 1:
        return {sub_token[0]:sub_token[1].rstrip()[:-1]};

    return {sub_token[0]:""};



# Define dictionaries
call_d = {}
ret_d  = {}
nami_list = list()
gio_d  = {}
errno_d = {}
fd_dic = {}
opened_fd = {}
opened_fd_list = list()

file = open(sys.argv[1], "r")
lines = file.readlines()
file.close()

def openat_parser(num):
    filename_dic = {}
    #import pdb; pdb.set_trace()
    openat_tokens = tokenizer(lines[num])
    nami_tokens  = tokenizer(lines[num + 1])
    filename   = nami_tokens[3].rstrip() if len(nami_tokens) > 3 else ""
    if not filename:
        return;
    ret_tokens = tokenizer( lines[num + 2]) 
    if len(ret_tokens) > 3:
        fd_num = ret_tokens[4].rstrip()
    #print("fd " + str(fd_num) + " opened for " + filename)
    if not filename in fd_dic:
        filename_dic[openat_tokens[3].rstrip()] = fd_num
        fd_dic[filename] = filename_dic
    else:
        filename_dic = fd_dic[filename]
        filename_dic[openat_tokens[3]] = fd_num
        fd_dic[filename] = filename_dic

    #print(fd_dic[filename])
    return {int(fd_num):filename};

def get_RET_value(index, function_name):
    ret_value = ""
    while index < len(lines):
        index += 1
        next_ln_tokens = tokenizer(lines[index])
        if "RET" in next_ln_tokens and len(next_ln_tokens) > 3 and next_ln_tokens[3] == function_name:
            ret_value = next_ln_tokens[4].rstrip()
            break

    if ret_value == "":
        print("Couldn't find relative RET value!!")
    return ret_value;
    
for ln in lines:
    #print(ln)
    tokens = tokenizer(ln)
    #print(tokens)
    #print(tokens[0])
    if tokens[0] != '""\n' and tokens[0] != '\n':
        m = re.search('[^(1-9)]*[0-9]*', tokens[0])
	#print(m.group(0))
	if len(m.group(0)) > 1 and m.group(0) != '':
		if len(tokens) >= 4:	
			#print("it has passed aaaaaaallll the tests :D ")
			if tokens[2] == "CALL":
                                #import pdb; pdb.set_trace()
				sub_token = tokens[3].split("(")
				#print(sub_token)
                                if len(sub_token) > 1:
				    call_d[sub_token[0]]= sub_token[1]
                                    function = sub_token[0]
                                    if function == "openat":
                                        temp_dic = openat_parser(lines.index(ln)) # A fd would open to be traced
                                        fd = temp_dic.keys()[0]
                                        opened_file_path  = temp_dic[fd]
                                        opened_fd_list.append(fd) 
                                        #print(temp_dic.keys()[0] + ":" + temp_dic[temp_dic.keys()[0]])                                        
                                        opened_fd.update(temp_dic);# There won't be any opened two files with the same fd at a time
                                    elif function == "close":
                                        #import pdb; pdb.set_trace()
                                        fd = int(sub_token[1].rstrip()[:-1],16)#The string showing the fd number in hexadecimal format
                                        if fd in opened_fd.keys():
                                            print("")
                                            print("we are done with the fd:" + str(fd) + " for the file: " + opened_fd[fd])
                                            print(fd_dic[opened_fd[fd]])
                                            del opened_fd[fd]
                                            del opened_fd_list[opened_fd_list.index(fd)]
                                    elif len(opened_fd) > 0:
                                        #import pdb; pdb.set_trace()
                                        last_opened_fd = opened_fd_list[-1]
                                        #print("The last opened fd is:" + str(last_opened_fd))
                                        filename = opened_fd[last_opened_fd]
                                        temp_dic = fd_dic[filename]
                                        function = tokenizer(ln)[3].rstrip()
                                        temp_dic[function] = get_RET_value(lines.index(ln),get_function_detail(ln).keys()[0])
                                        fd_dic[filename] = temp_dic
                                else:
				    call_d[sub_token[0]]= "no_args"
			elif tokens[2] == "RET":
				ret_d[tokens[3]] = tokens[4] # functionname and the returned value
				if tokens[4] != '0\n' and 'errno' in tokens and tokens[5] == "errno":
				        print("An error occured!")
                                        print(tokens[6])
                                        err_msg = ""
					i = 7
					while True:	
						err_msg += str(' ') + str(tokens[i])
						if tokens[i].endswith("\n"):
							break
						i += 1
					print(err_msg)
					errno_d[str(tokens[6])] = err_msg.rstrip()
                	elif tokens[2] == "NAMI":
	                    nami_list.append(tokens[3])
        	        elif tokens[2] == "GIO":
                	    gio_d[tokens[3] + " " + tokens[4]] = tokens[5] + " " + tokens[6] + "" + tokens[7]
        #print("")


print("\n")
print("call_list lenght:")
print( len(call_d))
print(call_d)
print("\n")

print("\n")
print("ret_list lenght:")
print( len(ret_d))
print(ret_d)
print("\n")

print("\n")
print("nami_list lenght:")
print( len(nami_list))
print(nami_list)
print("\n")

print("\n")
print("gio_list lenght:")
print( len(gio_d))
print(gio_d)
print("\n")


print("\n")
print("errno_list lenght:")
print(len(errno_d))
print(errno_d)
print("\n")


print("\n")
print("fd dictionary contains lists of operation applied to files, its lenght and opened files are:")
print(len(fd_dic))
print(fd_dic.keys())
print("\n")

print("It's Done!!!!")
