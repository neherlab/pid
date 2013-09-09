#!/usr/bin/python
#/!\#
#### /ebio/ag-neher/share/pograms/EPD/bins/python
#/!\#

## script that aligns the temp reads files (one per pID/barcode) in the given directory
## input: directory (for a given barcode) containing the temp reads files to align (in ../templates/)
## output: aligned reads files (one per pID) contained in a directory "align" (in ../templates/)

import numpy as np
from Bio import SeqIO
from Bio.Align.Applications import MuscleCommandline
import os
import sys
import time
import lib_tools as lt

auto_file_name = str(sys.argv[0])


######
# DEF FUNCTIONS
######


if (len(sys.argv)==2):
    ####
    # parse the input directory name
    ####
    relative_path_to_temp_directory = str(sys.argv[1])
    if relative_path_to_temp_directory[-1]!='/':
        relative_path_to_temp_directory+='/'
    path_to_templates='../templates/'
    #path_to_input_dir = relative_path_to_temp_directory[:13] # "../templates/" 
    #temp_directory_basename = input_directory_name[13:] # "../templates/" to remove
    temp_directory_basename = relative_path_to_temp_directory[-2]
    [prefix_date_and_id, bc]= [temp_directory_basename.split('_')[i] for i in [0,2]]
    prefix_date_and_id = prefix_date_and_id[len('dir-'):] # "dir-" to remove
    #if bc[-1]=='/':
    #    bc= bc[:-1] # "/" to remove
    print prefix_date_and_id, bc
    ####
    # collect the temp reads files to align for the given barcode
    ####
    list_temp_files = os.popen('ls '+relative_path_to_temp_directory+'*').readlines()
    list_temp_files = [list_temp_files[i].split('/')[-1].strip() for i in range(len(list_temp_files))]
    # list of "pIDs" to generate the pID alignment files 
    list_of_pIDs = [list_temp_files[i].split('_')[3] for i in range(len(list_temp_files))]
    # cut the extension ".fasta" of pIDs
    for i in range(len(list_of_pIDs)):
        list_of_pIDs[i] = list_of_pIDs[i][:-6]# length(".fasta")=6
    print 'list_of_pIDs created, length: ' + str(len(list_of_pIDs))
    set_of_pIDs = set(list_of_pIDs) 
    print 'no duplicates in pIDs list: '+str(len(set_of_pIDs)==len(list_of_pIDs))

    ####
    # align the reads (temp files) and creates the corresponding aligned files in the align directory (created automatically)
    ####
    #create the directory for the aligned reads
    dir_align_name_bc = str(path_to_templates+'dir-'+prefix_date_and_id+'_align_'+bc)
    #print dir_align_name_bc
    dir_temp_name_bc =  str(path_to_templates+'dir-'+prefix_date_and_id+'_temp_'+bc)
    #print dir_temp_name_bc
    lt.check_and_create_directory(dir_align_name_bc)
    time_start = time.time()
    for pID in list_of_pIDs:
        temp_file_name = dir_temp_name_bc+ '/' +prefix_date_and_id + '_temp_' + bc + '_' + pID + '.fasta'
        align_file_name=dir_align_name_bc+ '/' +prefix_date_and_id + '_align_'+ bc + '_' + pID + '.fasta'
        print 'Alignment for file: ' + temp_file_name
        cline = MuscleCommandline(input = temp_file_name, out = align_file_name)
        #
        cline()
        #
    time_end = time.time()
    print 'computation time: '+str(time_end-time_start)

    #else:
    #    print 'no file created'
    
    

else:
    print auto_file_name+': usage: '+auto_file_name+' <temp directory containing temp reads files to align (in ../templates/)>'



####
#collect the list of specific barcode/pID temp files to align (files generated by pipeline2 in dir. templates)
####
# list_temp_files = os.popen('ls -l ../templates/'+prefix_date_and_id+'_temp_*').readlines()
# list_temp_files = [list_temp_files[i].split(' ')[-1].split('\n')[0] for i in range(len(list_temp_files))]
# # list of "triples" [date+id,barcode,pID] to generate the pID alignement files 
# list_file_names = [[list_temp_files[i].split('_')[j] for j in [0,2,3]] for i in range(len(list_temp_files))]
# # cut the extension ".fasta" of pIDs and the prefix "../templates/" to the date+id
# for i in range(len(list_file_names)):
#     list_file_names[i][2] = list_file_names[i][2][:-6]# length(".fasta")=6
#     list_file_names[i][0] = list_file_names[i][0][13:]# length("../templates/")=13
# print 'list_file_names created, length: ' + str(len(list_file_names))



####
#align the reads for each temp file
####
#for alignments per interval if parallelisation needed
# if len(sys.argv)==3:
#     first = int(sys.argv[1])
#     last = int(sys.argv[2])
# else:
#     first=0
#     last=len(list_file_names)
# time_start = time.time()
# for cur_file in list_file_names[first:last]:
#     temp_file_name = '../templates/' + cur_file[0] + '_temp_' + cur_file[1] + '_' + cur_file[2] + '.fasta'
#     align_file_name = '../templates/' + cur_file[0] + '_pID_' + cur_file[1] + '_' + cur_file[2] + '.fasta'
#     print 'Alignment for file: ' + temp_file_name
#     cline = MuscleCommandline(input = '../templates/' + cur_file[0] + '_temp_' + cur_file[1] + '_' + cur_file[2] + '.fasta', out = '../templates/' + cur_file[0] + '_pID_' + cur_file[1] + '_' + cur_file[2] + '.fasta')
    
    
#     #
#     cline()
#     #
# time_end = time.time()
# print 'computation time: '+str(time_end-time_start)
    
