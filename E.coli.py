from Bio import Entrez
import os
import urllib.request
#With Biopython I need to provide the Email Address
Entrez.email = <Your Email Adress> 

# I can use "sra" databank with term "(Escherichia coli K12[Organism]) AND transcriptome" to get concrete data
handle = Entrez.esearch(db = "sra", retmax = 2400, term = "(Escherichia coli K12[Organism]) AND transcriptome")
record = Entrez.read(handle)
# After searching I have found that all the transcriptomes consist of SRRID and ERRID.
# The type of results through sra is "bytes" so I need to change it to "str"
# Hier to get all the SRRID and ERRID. The lengths of SRRID is 11 but some of ERRID is in different lengths.
lst_ID_SRR = []
lst_ID_ERR = []
for i in range(len(record["IdList"])):
    obtain = Entrez.efetch(db = "sra", id = record["IdList"][i])
    handle = obtain.read()
    start = str(handle).find("RR") - 1
    end = str(handle).find('"', start)
    ID = str(handle)[start:end].strip('')
    if ID[:3] == "SRR":
        lst_ID_SRR.append(ID)
    elif ID[:3] == "ERR":
        lst_ID_ERR.append(ID)
with open("ID_SRR.txt", "w") as f:
    for i in lst_ID_SRR:
        f.write(i + '\n')
with open("ID_ERR.txt", "w") as f:
    for i in lst_ID_ERR:
        f.write(i + '\n')

# Creating the downloading links for Aspera
lst_asp_links = []
with open("ID_ERR.txt") as f:
    lst_ID = [i.strip() for i in f.readlines()]
    for ID in lst_ID:
        if len(ID) == 10:
            with urllib.request.urlopen("ftp://ftp.sra.ebi.ac.uk/vol1/fastq/"+ID[:6]+"/00"+ID[-1]+"/"+ID+"/") as f:
                a = str(f.read())
                n1 = 0
                n2 = 0
                start = 0
                end = 0
                while start >= 0 or end >= 0:
                    start = a.find("RR", n2) - 1
                    n1 = start
                    end = a.find("gz", n1)
                    n2 = end
                    if start >= 0:
                        lst_asp_links.append("era-fasp@fasp.sra.ebi.ac.uk:/vol1/fastq/"+ID[:6]+"/00"+ID[-1]+"/"+ID+"/"
                                            +a[start:end + 2].strip())
        elif len(ID) == 9:
            with urllib.request.urlopen("ftp://ftp.sra.ebi.ac.uk/vol1/fastq/"+ID[:6]+"/"+ID+"/") as f:
                a = str(f.read())
                n1 = 0
                n2 = 0
                start = 0
                end = 0
                while start >= 0 or end >= 0:
                    start = a.find("RR", n2) - 1
                    n1 = start
                    end = a.find("gz", n1)
                    n2 = end
                    if start >= 0:
                        lst_asp_links.append("era-fasp@fasp.sra.ebi.ac.uk:/vol1/fastq/"+ID[:6]+"/"+ID+"/"
                                                +a[start:end+2].strip())
# Save the links in a txt file
with open("ENA.txt","w") as f:
    for i in lst_asp_links:
        f.write(i + '\n')

# Downloading the documents with Sratoolkit. It is so time-spent that I hide it.
# Or we can use a file shotcut copied in the same directory. Then we don't need to change the directory
os.system("prefetch.exe.lnk --option-file ID_SRR.txt -O <Here is the Output directory>)
# What we donload is .sra files. We also need to change it to fastq files.
# Because we first download the sra files with directory. We should save them in a list
for i in os.listdir():
    if i[:3] == "SRR":
        lst_dir.append(i.strip())
# Here is to change .sra to .fastq
for dir in lst_dir:
    os.system("fastq-dump.exe.lnk " +dir+ " -O <Here is the Output directory>")
# Using Aspera to download
# You can choose which directory you want to save
output_dir = os.getcwd()
# Change the directory, where Aspera is saved
os.chdir(r"C:\Users\Tanktan\AppData\Local\Programs\Aspera\Aspera Connect\bin")
for link in lst_asp_links:
    os.system("ascp.exe -Q -T -l 200m -P 33001 -k 1 -i ../etc/asperaweb_id_dsa.openssh "+link+" "+output_dir)
''' Summary: We can get all the SRRIDs and ERRIDs. With wget is the downloading so bad that I suggest, that we can use 
 Sratoolkit to get the datas. After running Sratoolkit I have found that, the results with ERRIDs cannot be downloaded. 
 So we need to use Aspera to get the results with ERRIDs through ENA. We need another terminal to use Aspera'''
