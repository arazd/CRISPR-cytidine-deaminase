import sys
import re
import xlsxwriter
import os
from design_library import *

dir=os.getcwd()
fname1=str(sys.argv[1])      # .fsa file in the same folder with this script
PAM1=str(sys.argv[2])        # usually NGG or NG; should be sequence of nucleotides (AGG, CAT etc.). Put N for any nucleotide
region1=int(sys.argv[3])     # usually 20
mut_window1=int(sys.argv[4]) # mutation window (in base-pairs), usually 12

run_design(dir, fname1, PAM1, region1, mut_window1)
print('Done!')
