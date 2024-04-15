import argparse
import os
import sys
import subprocess
import re
import textwrap

try:
    from Bio import SeqIO
except:
    print("SeqIO module is not installed! Please install SeqIO and try again.")
    sys.exit()

try:
    from Bio.Seq import Seq
except:
    print("Seq module is not installed! Please install Seq and try again.")
    sys.exit()

try:
    import tqdm
except:
    print("tqdm module is not installed! Please install tqdm and try again.")
    sys.exit()

parser = argparse.ArgumentParser(prog='python seq_range_fetch.py',
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog=textwrap.dedent('''\

# seq_range_fetch

Author: Murat Buyukyoruk

        seq_range_fetch help:

This script is developed to fetch range sequences of gene/CRISPR loci of interest by using the fasta file with provided position and strand information. 

SeqIO and Seq packages from Bio is required to fetch sequences. Additionally, tqdm is required to provide a progress bar since some multifasta files can contain long and many sequences.

Syntax:

        python seq_range_fetch.py -i demo.fasta -o demo_gene_flanks.fasta -d flank_info_dataframe

Example Dataframe (tab separated excel file is required):

        Accession       Start       Stop        Strand
        NZ_CP006019.1   1875203     1877050     -1
        CP000472.1      123         975         1

flank_grabber dependencies:

Bio module, SeqIO and Seq available in this package     refer to https://biopython.org/wiki/Download

tqdm                                                    refer to https://pypi.org/project/tqdm/

Input Paramaters (REQUIRED):
----------------------------
	-i/--input		FASTA			Specify a fasta file. FASTA file requires headers starting with accession number. (i.e. >NZ_CP006019 [fullname])

	-o/--output		Output file	    Specify a output file name that should contain fetched sequences.

	-d/--data		Dataframe		Specify a list of accession (Accession only). Each accession should be included in a new line (i.e. generated with Excel spreadsheet). Script works with or without '>' symbol before the accession.

Basic Options:
--------------
	-h/--help		HELP			Shows this help text and exits the run.

Output header will contain array no, original header, positions (if included in original fasta), and observed stand.

      	'''))
parser.add_argument('-i', '--input', required=True, type=str, dest='filename',
                    help='Specify a fastafile to fetch regions from.\n')
parser.add_argument('-o', '--output', required=True, dest='out',
                    help='Specify a output file name.\n')
parser.add_argument('-d', '--data', required=True, dest='data',
                    help='Specify a dataframe with accession, start, stop, strand info in that order.\n')

results = parser.parse_args()
filename = results.filename
out = results.out
data = results.data

os.system('> ' + out)

seq_id_list = []
seq_list = []
seq_description_list = []

proc = subprocess.Popen("grep -c '>' " + filename, shell=True, stdout=subprocess.PIPE, text=True)
length = int(proc.communicate()[0].split('\n')[0])

with tqdm.tqdm(range(length)) as pbar:
    pbar.set_description('Reading...')
    for record in SeqIO.parse(filename, "fasta"):
        pbar.update()
        seq_id_list.append(record.id)
        seq_list.append(record.seq)
        seq_description_list.append(record.description)

proc = subprocess.Popen("wc -l < " + data, shell=True, stdout=subprocess.PIPE, text=True)
length = int(proc.communicate()[0].split('\n')[0])
i = 0
with tqdm.tqdm(range(length), desc='Fetching...') as pbar:
    with open(data, 'r') as file:
        f = open(out, 'a')
        sys.stdout = f
        for line in file:
            pbar.update()
            if "Accession" not in line:
                # array = line.split('\t')[0]
                acc = line.split()[0]
                start = line.split('\t')[1]
                stop = line.split('\t')[2]
                strand = line.split('\t')[3].split('\n')[0]

                if strand == "F" or strand == "NA" or str(strand) == "1":
                    try:
                        ind = seq_id_list.index(acc)
                        print('>' + seq_description_list[ind] + ' | ' + str(int(start) + 1) + '-' + str(int(stop)) + ' | ' + str(strand))
                        seq = Seq(str(seq_list[ind][int(start):int(stop)]))
                        print(re.sub("(.{60})", "\\1\n", str(seq), 0, re.DOTALL))
                        # print seq
                    except:
                        pass

                elif strand == 'R' or str(strand) == "-1":
                    try:
                        ind = seq_id_list.index(acc)
                        print('>' + seq_description_list[ind] + ' | ' + str(int(start)) + '-' + str(int(stop) - 1) + ' | ' + str(strand))
                        seq = Seq(str(seq_list[ind][int(start):int(stop)])).reverse_complement()
                        print(re.sub("(.{60})", "\\1\n", str(seq), 0, re.DOTALL))
                        # print seq
                    except:
                        pass




