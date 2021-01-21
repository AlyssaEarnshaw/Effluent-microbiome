#Script to Merge Alyssas lines

import csv
import re
import sys
from pathlib import Path

#Lets me do manipulations of the Path like replacing the suffix.
filename = Path(sys.argv[1])
output_filename = filename.with_suffix('.csv')

d =open(filename,"r").readlines()

#Output file is named the same as input, but with a different suffix
write_results = open(output_filename, "a")
csv_writer = csv.writer(write_results)

Header_list=["OTU","Domain","Phylum","Class","Order","Family","Genius"]
csv_writer.writerow(Header_list)

# My general approach was to split everything up into the pieces I want, then stick them back together in the order I want.

for i in range(len(d) ):
    #The original data lines are in groups of three, this if statement pulls out every third line, therefore letting us work with the lines in 3's
    if (i % 3 == 0):
        #Taking the first line in each triplicate and saving it.
        first_line=d[i]
        #Taking the second line in each triplicate and saving it.
        second_line=d[i+1]
        #In order to "grab" the OTU I split the first line into a list at the ">" symbol
        #and then take the second item in the resulting list (the OTU) also removing the new line (cuz that would f*ck shit up)
        split_first_line = first_line.split('>')
        otu=split_first_line[1].strip('\n')
        #The second line is more messy, first I split it at the ";" to remove the target size info
        split_second_line=second_line.split(';')
        #Then I take the main results and split them by the , to give me seperate list elements for each result.
        #This lets me enter them into seperate coloumns in the CSV and also remove the d:, p: etc
        ss_second_line = split_second_line[1].split(',')
        #Here im spliting at the = to get rid of the niggly ugly "tax=d:" structure.
        tax_removed = ss_second_line[0].split('=')

        #This is where Im starting to stick everything back together the way I want it.
        #First make a new list to put everything in.
        new_list = []
        #First coloumn should be OTU so I stick that in first.
           new_list.append(otu)
        #Then I chuck in the domain results minus the "tax=" bit that we dont need, and strip off the "d:" its redundant.
        #new_list.append(tax_removed[1].strip("d:"))
        #new_list.append(ss_second_line)
        #Now im adding every other result.
        for j in range(1,len(ss_second_line)):
            value=re.split(':',ss_second_line[j])
            new_list.append(value[1].strip('"'))
        #just me checking my list looks how I want
        #print(new_list)
        #Adding each reformated line to the CSV. et volia
        csv_writer.writerow(new_list)
