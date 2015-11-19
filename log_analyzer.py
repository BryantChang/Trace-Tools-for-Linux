#!/usr/bin/env python
"this script can analysis the log of ftrace automaticlly and display the kernel function calling for one cmd"
import os
import sys

#keys of the config file 
MODE = 'mode'
FTRACE_LOG_PATH = 'ftrace_log_path'
OUTPUT_TEXT_LOG_PATH = 'output_text_log_path'
OUTPUT_PIC_LOG_DIR = 'output_pic_log_dir'


#parse the config file return the dictionary of key value
def parse_config(file_path):
    file_dic = {}
    try:
        fobj = open(file_path, 'r')
    except IOError, e:
        print 'the config file is not exists'  #file not exists return
        return file_dic
    else:   #gernerate the dictionary
        for eachline in fobj:
            if eachline[0] == '#':   #skip the statement
                continue
   	    k_v_items = eachline.split('=')
            key = k_v_items[0]
	    value = k_v_items[1][:-1]
	    file_dic[key] = value
        fobj.close()
    return file_dic


def output_tab(tab_num):
    return '    ' * tab_num

def is_same_list(list1, list2):
    list1.sort()
    list2.sort()
    if list1 == list2:
        return True
    return False


def gen_text(file_dic): 
    output_fobj = open(file_dic[OUTPUT_TEXT_LOG_PATH], 'w')
    try:
        ftrace_fobj = open(file_dic[FTRACE_LOG_PATH], 'r')
    except IOError, e:
        print 'the ftrace log does not exists'
        exit()
    else:
        last_parent = ''
        func_list = []
        for eachline in ftrace_fobj:
            k_v_items = eachline.split('<-')
            child = k_v_items[0]
            parent = k_v_items[1][:-1]
            child.replace('.', '_')
            parent.replace('.', '_')
            if last_parent == '':
                func_list.append(parent)
                func_list.append(child)
                last_parent = child
            elif parent == last_parent:
                func_list.append(child)
                last_parent = child
            else:
                length = len(func_list)
                for count in range(0,length):
                    line =  "\n" + output_tab(count) + func_list[count]
                    output_fobj.write(line)
                output_fobj.write("\n")
                func_list = []
                func_list.append(parent)
                func_list.append(child)
                last_parent = child

        ftrace_fobj.close()
        output_fobj.close()



def gen_dot(file_dic):
    line_counter = 0
    file_counter = 0
    output_fobj = open(file_dic[OUTPUT_PIC_LOG_DIR] + 'output0.dot', 'w')
    output_fobj.write("digraph G{\n")
    try:
        ftrace_fobj = open(file_dic[FTRACE_LOG_PATH], 'r')
    except IOError, e:
        print 'the ftrace log does not exists'
        exit()
    else:
        last_parent = ''
        func_list = []
        #last_func_list=[]
        for eachline in ftrace_fobj:
            k_v_items = eachline.split('<-')  #parse eachline of the file
            child = k_v_items[0]
            parent = k_v_items[1][:-1]
            child.replace('.', '_')
            parent.replace('.', '_')
            if last_parent == '':
                func_list.append(parent)
                func_list.append(child)
                last_parent = child
            elif parent == last_parent:
                func_list.append(child)
                last_parent = child
            else:
                #if func_list == last_func_list:
                 #    continue
                line = ''
                length = len(func_list)
                output_fobj.write('    ')
                for count in range(0,length):
                    line =  line + func_list[count][:-1] + '->'
                output_fobj.write(line[:-2])
                output_fobj.write(";\n")
                #last_func_list = func_list
                func_list = []
                func_list.append(parent)
                func_list.append(child)
                last_parent = child
                line_counter = line_counter + 1
                if line_counter == 100:
                    file_counter = file_counter + 1
                    line_counter = 0
                    output_fobj.write("}\n")
                    output_fobj.close()
                    output_fobj = open(file_dic[OUTPUT_PIC_LOG_DIR] + 'output' + str(file_counter) + '.dot', 'w')
                    output_fobj.write("digraph G{\n")
        output_fobj.write("}\n")
        ftrace_fobj.close()
        output_fobj.close()

def usage():
    print "usage: log_analyzer <config_file_path>"
    return


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
        exit()
    file_dic = parse_config(sys.argv[1])
    if file_dic == {}:
        print "your config file is empty please check"
        exit()
    mode = file_dic[MODE]
    if mode == 'text':
	gen_text(file_dic)
    elif mode == 'pic':
        gen_dot(file_dic)
    else:
        print "the mode must be 'text' or 'pic' please check your config file"
        exit()
    
