
# seq_range_fetch

Author: Murat Buyukyoruk

        seq_range_fetch help:

This script is developed to fetch range sequences of gene/CRISPR loci of interest by using the fasta file with provided position and strand information. 

SeqIO and Seq packages from Bio is required to fetch sequences. Additionally, tqdm is required to provide a progress bar since some multifasta files can contain 
long and many sequences.

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
	-i/--input		FASTA			Specify a fasta file. FASTA file requires headers starting with accession number. (i.e. >NZ_CP006019 
[fullname])

	-o/--output		Output file	    Specify a output file name that should contain fetched sequences.

	-d/--data		Dataframe		Specify a list of accession (Accession only). Each accession should be included in a new line (i.e. 
generated with Excel spreadsheet). Script works with or without '>' symbol before the accession.

Basic Options:
--------------
	-h/--help		HELP			Shows this help text and exits the run.

Output header will contain array no, original header, positions (if included in original fasta), and observed stand.

