import re
import xlsxwriter
import os

amino_acid_dict={"UUU":"Phe", "UUC":"Phe", "UUA":"Leu", "UUG":"Leu",
       "UCU":"Ser", "UCC":"Ser", "UCA":"Ser", "UCG":"Ser",
       "UAU":"Tyr", "UAC":"Tyr", "UAA":"STOP", "UAG":"STOP",
       "UGU":"Cys", "UGC":"Cys", "UGA":"STOP", "UGG":"Trp",
       "CUU":"Leu", "CUC":"Leu", "CUA":"Leu", "CUG":"Leu",
       "CCU":"Pro", "CCC":"Pro", "CCA":"Pro", "CCG":"Pro",
       "CAU":"His", "CAC":"His", "CAA":"Gln", "CAG":"Gln",
       "CGU":"Arg", "CGC":"Arg", "CGA":"Arg", "CGG":"Arg",
       "AUU":"Ile", "AUC":"Ile", "AUA":"Ile", "AUG":"Met",
       "ACU":"Thr", "ACC":"Thr", "ACA":"Thr", "ACG":"Thr",
       "AAU":"Asn", "AAC":"Asn", "AAA":"Lys", "AAG":"Lys",
       "AGU":"Ser", "AGC":"Ser", "AGA":"Arg", "AGG":"Arg",
       "GUU":"Val", "GUC":"Val", "GUA":"Val", "GUG":"Val",
       "GCU":"Ala", "GCC":"Ala", "GCA":"Ala", "GCG":"Ala",
       "GAU":"Asp", "GAC":"Asp", "GAA":"Glu", "GAG":"Glu",
       "GGU":"Gly", "GGC":"Gly", "GGA":"Gly", "GGG":"Gly"}

rna_dict={"A":"U", "T":"A", "C":"G", "G":"C"}

# ------------------- DNA to RNA ------------------
def to_RNA_minus(dna):      # transcribing from template (minus) strand
    rna=''
    for i in range(len(dna)):
        rna+=rna_dict[dna[i]]
    return rna


def to_RNA_plus(dna):       # RNA if plus strand given
    rna= dna.replace('T', 'U')
    return rna

# ------------------- RNA to protein ------------------
def to_protein(mRNA):
    protein=''
    for i in range(len(mRNA)//3):       #  floor (integer) division by 3
        codon=mRNA[i*3]+mRNA[i*3+1]+mRNA[i*3+2]
        protein += amino_acid_dict[codon]+'-'
    protein = protein[:-1]              #  remove last character
    return protein


# ------------------- reading fasta file ------------------
def read_fasta(f):
    content = f.readlines()
    content = [x.strip() for x in content]      #  remove spaces
    content = [x for x in content if x != '']   #  remove empty elements
    #print(content)

    header=content[0]
    if ('>' in header):
        content.pop(0)                          #  removing header line from the content

    for line in content:                        #  removing all comments
        if (line.startswith(';')):
            list.remove(line)

    sequence=''.join(content)
    sequence=sequence.replace('*', '')          #  remove asterisks at the end of the file (if there are any)
    #print("\nseq=",seq,"\nlength=",len(seq))
    return header, sequence




# ------------------- finding gRNAs ------------------
def find_gRNAs(seq, PAM='NG', region=20, mutation_window=12):
    c20=region
    c12=mutation_window
    c2=len(PAM)

    PAM_plus=PAM.replace('N', "[A,C,T,G]{1}")        #  {1} = match exactly 1 time
    PAM_plus='(?='+PAM_plus+')'                      # PAM sequence on + strand

    PAM_minus=PAM[::-1]                              # PAM sequence on - strand
    table=''.maketrans("ATCG", "TAGC")
    PAM_minus=PAM_minus.translate(table)
    PAM_minus=PAM_minus.replace('N', "[A,C,T,G]{1}")
    PAM_minus='(?='+PAM_minus+')'                   # (?=abc) helps to find overlapping PAMs

    #PAM_matches=re.findall(PAM,seq)
    PAM_plus_matches=[m.start() for m in re.finditer(PAM_plus,seq)]
    PAM_plus_matches=[x for x in PAM_plus_matches if x>region]   # make sure there is space for guide seq before PAM

    PAM_minus_matches=[m.start() for m in re.finditer(PAM_minus,seq)]
    PAM_minus_matches=[x for x in PAM_minus_matches if (len(seq)-(x+1))>region]   # make sure there is space for guide seq before PAM (account for opposite strand)


    # gRNAs on '+' strand
    gRNAs_plus=[]
    start_pos_plus=[]
    PAMs_plus=[]
    mutated_seqs_plus=[]
    mutation_positions_plus=[]

    for k in PAM_plus_matches:
        grna=seq[k-c20:k]#.replace('T', 'U')
        #muts=[x.start() for x in re.finditer('C', seq[k-20:k][:12])]
        muts=[x.start() for x in re.finditer('C', seq[k-c20:k][:c12])]
        #if (muts!=[]):
            #mutation_positions_plus.append(muts)

        if (('C' in seq[k-c20:k][:c12]) and ("TTTTT" not in seq[k-c20:k])):
            gRNAs_plus.append(grna)
            PAMs_plus.append(seq[k:k+c2])
            start_pos_plus.append(k-c20)
            mutation_positions_plus.append(muts)

            seq_mutated=seq[0:k-c20]+seq[k-c20:k-(c20-c12)].replace('C', 'T')+seq[k-(c20-c12):]      # mutated seq with C->T in first 12 bp of guide region
            mutated_seqs_plus.append(seq_mutated)


    # gRNAs on '-' strand
    gRNAs_minus=[]
    start_pos_minus=[]
    PAMs_minus=[]
    mutated_seqs_minus=[]
    mutation_positions_minus=[]

    for k in PAM_minus_matches:
        c10=c20+c2-c12
        c8=c20-c12

        grna=to_RNA_minus(seq[k+c2:k+c20+c2])[::-1]  # reverting sequence, so that we have 5'->3' orientation
        grna=grna.replace('U', 'T')
        #muts=[x.start()+c20-c12-1 for x in re.finditer('G', seq[k+c2:k+c20+c2][-c12:][::-1])]
        #muts=[x.start() for x in re.finditer('G', seq[k+c10:k+c20+c2])]
        muts=[x.start() for x in re.finditer('G', seq[k+c2:k+c20+c2])]
        muts=[a for a in muts if (a>c8-1)]
        #if (muts!=[]):
            #mutation_positions_minus.append(muts)

        if (('G' in seq[k+c2:k+c20+c2][-c12:]) and ("TTTTT" not in seq[k+c2:k+c20+c2])):
            gRNAs_minus.append(grna)
            PAMs_minus.append(seq[k:k+c2])
            start_pos_minus.append(k+c2)
            mutation_positions_minus.append(muts)
                                    # mutate 12 bp from the start (inverse)

            seq_mutated=seq[0:k+c10]+seq[k+c10:k+c20+c2].replace('G', 'A')+seq[k+c20+c2:]      # mutated seq with C->T in first 12 bp of guide region (inverse cause - strand)
            mutated_seqs_minus.append(seq_mutated)

    info = {"gRNAs_plus":gRNAs_plus, "PAMs_plus":PAMs_plus, "start_pos_plus":start_pos_plus, "mutated_seqs_plus":mutated_seqs_plus,
            "mutation_positions_plus": mutation_positions_plus,
        "gRNAs_minus":gRNAs_minus, "PAMs_minus":PAMs_minus, "start_pos_minus":start_pos_minus, "mutated_seqs_minus":mutated_seqs_minus,
            "mutation_positions_minus": mutation_positions_minus}

    return info


# ------------------- amino acid changes ------------------
def amino_acid_change(seq, seq_mutated, strand='+'):            # sequences in 5'->3' order
    if (strand=="+"):
        protein=to_protein(to_RNA_plus(seq)).split('-')
        protein_mutated=to_protein(to_RNA_plus(seq_mutated)).split('-')
    elif (strand=="-"):
        protein=to_protein(to_RNA_minus(seq)).split('-')
        protein_mutated=to_protein(to_RNA_minus(seq_mutated)).split('-')

    amino_acid_changes={}       # dictionary{ position : amino acid change}

    for i in range(len(protein)):
        if (protein[i]!=protein_mutated[i]):
            amino_acid_changes[i]=protein[i]+str(i+1)+protein_mutated[i]

    return amino_acid_changes


# ------------------- save to excel ------------------
def to_excel(filename, my_tuple):
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(filename+'.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.set_column(1, 1, 30)
    worksheet.set_column(3, 3, 10)
    worksheet.set_column(4, 4, 30)
    worksheet.set_column(5, 5, 20)
    worksheet.set_column(6, 6, 30)
    bold_red = workbook.add_format({'bold': True, 'color': 'red'})
    bold_italic = workbook.add_format({'bold': True, 'italic': True})
    center = workbook.add_format({'align': 'center',
                                   'valign': 'vcenter',})

    row = 0
    col = 0

    worksheet.write(row, col,     'start position')
    worksheet.write(row, col + 1, 'gRNA')
    worksheet.write(row, col + 2, 'PAM')
    worksheet.write(row, col + 3, 'strand with PAM sequence')
    worksheet.write(row, col + 4, 'mutated region')
    worksheet.write(row, col + 5, 'amino acid changes (by a single DNA mutation)')
    worksheet.write(row, col + 6, 'amino acid changes (all DNA mutations combined)')
    row += 1


    for position, gRNA, pam, strand, mut_region, ind_mut_seqs, mutation_positions, amino_acid_changes, ind_changes in (my_tuple):
        '''
             print("\n\n",position)
             print(gRNA)
             print(strand)
             print(mut_region)
             print(ind_mut_seqs)
             print(mutation_positions)
             print(amino_acid_changes)
             print(ind_changes)'''

        worksheet.write(row, col,     position+1)   # we start indexing from 0 in python, so add 1
        worksheet.write(row, col + 1, gRNA)
        worksheet.write(row, col + 2, pam)
        worksheet.write(row, col + 3, strand)
        worksheet.write(row, col + 4, mut_region)
         #worksheet.write(row, col + 4, amino_acid_changes)
        if (row!=row+len(mutation_positions)-1):
             worksheet.merge_range(row, col + 6, row+len(mutation_positions)-1, col + 6, amino_acid_changes,center)
        else: worksheet.write(row, col + 6, amino_acid_changes,center) # cannot merge 1 cell

        j=0    # iterator in a loop below
        for i in mutation_positions:
            #print(i)
             #worksheet.write_rich_string(row, col + 3, mut_region[:i],bold_red,mut_region[i],mut_region[i+1:])
             worksheet.write_rich_string(row, col + 4, ind_mut_seqs[j][:i],bold_red, ind_mut_seqs[j][i], ind_mut_seqs[j][i+1:])
             worksheet.write_rich_string(row, col + 5, ind_changes[j])
             j+=1
             row+=1
        worksheet.write_rich_string(row, col + 4, bold_italic, mut_region)

        row+=2





# ----------------------------------------------------------
def run_design(dir, fname, PAM, region, mut_window):
    os.chdir(dir) # go to file's directory

    with open(fname) as f:
        head, seq = read_fasta(f)
        #print("\nseq (5' -> 3') =",seq,"\nlength=",len(seq))

    filename=head.split(' ')[0][1:]+'_gRNA_design'


    #info = find_gRNAs(seq, 'NGG')
    info=find_gRNAs(seq, PAM, region, mut_window)
    tup=()  # tuple


    ### PAM on plus strand
    for i in range (len(info["gRNAs_plus"])):
        grna =      info["gRNAs_plus"][i]
        mut_pos =   info["mutation_positions_plus"][i]      # positions of mutations on guide region
        pam =       info["PAMs_plus"][i]
        pos =       info["start_pos_plus"][i]
        strand = "+"
        mutated_seq = info["mutated_seqs_plus"][i]
        am_ac_changes = amino_acid_change(seq, mutated_seq)
        values = list(am_ac_changes.values())
        if (values==[]):                                    # join amino acid changes list into string
            values='0'
        else:
            values=', '.join(values)

        mut_region = mutated_seq[ pos : pos+region ]    # highlighting mutations in guide region in red

        ind_mut_seqs=[]                                 # understanding individual nucleotide mutations effects
        for k in info["mutation_positions_plus"][i]:
            ind_mut_seqs.append(seq[:k+pos]+'T'+seq[k+pos+1:])  # C -> T
        changes_array=[]
        for j in range(len(ind_mut_seqs)) :
            ind_changes=amino_acid_change(seq, ind_mut_seqs[j])
            ind_changes = list(ind_changes.values())
            if (ind_changes==[]):
                ind_changes='0'
            else:
                ind_changes=', '.join(ind_changes)
            changes_array.append(ind_changes)           # array with individual amino acid changes caused by individual mutations in DNA

        for i in range(len(ind_mut_seqs)) :
            ind_mut_seqs[i]=ind_mut_seqs[i][pos : pos+region]

        tup += ([pos, grna, pam, strand, mut_region, ind_mut_seqs, mut_pos, values, changes_array],)


    ### PAM on minus strand
    for i in range (len(info["gRNAs_minus"])):
        grna =      info["gRNAs_minus"][i]
        mut_pos =   info["mutation_positions_minus"][i]     # positions of mutations on guide region
        pam =       info["PAMs_minus"][i]
        pos =       info["start_pos_minus"][i]
        strand = "-"
        mutated_seq = info["mutated_seqs_minus"][i]
        am_ac_changes = amino_acid_change(seq, mutated_seq)
        changes = list(am_ac_changes.values())
        if (changes==[]):
            changes='0'
        else:
            changes=', '.join(changes)

        pam=pam[::-1]                              # PAM sequence on - strand
        table=''.maketrans("ATCG", "TAGC")
        pam=pam.translate(table)

        mut_region = mutated_seq[ pos : pos+region ]

        ind_mut_seqs=[]                                 # what happens with individual mutations?
        for k in info["mutation_positions_minus"][i]:
            ind_mut_seqs.append(seq[:k+pos]+'A'+seq[k+pos+1:])  # G -> A
        changes_array=[]
        for j in range(len(ind_mut_seqs)) :
            ind_changes=amino_acid_change(seq, ind_mut_seqs[j])
            ind_changes = list(ind_changes.values())
            if (ind_changes==[]):
                ind_changes='0'
            else:
                ind_changes=', '.join(ind_changes)
            changes_array.append(ind_changes)           # array with individual amino acid changes caused by individual mutations in DNA

        for i in range(len(ind_mut_seqs)) :
            ind_mut_seqs[i]=ind_mut_seqs[i][pos : pos+region]

        tup += ([pos, grna, pam, strand, mut_region, ind_mut_seqs, mut_pos, changes, changes_array],)

    to_excel(filename, tup)
