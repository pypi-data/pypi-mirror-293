## PFam profile DB creation

### Method 1: Pfam DB creation (using mmseqs databases)
> Obtain the database file and create the profile DB from the latest version of Pfam-A.seed
mmseqs databases Pfam-A.seed pfama37 tmp/ --threads 4 --remove-tmp-files -v 3

- Aside from downloading the seed sequences from PFam, it also performs the following steps:
  - Convert the MSA: `mmseqs convertmsa tmp//18345222364982670005/db.msa.gz tmp//18345222364982670005/msa -v 3`
  - Create the profile DB: `mmseqs msa2profile tmp//18345222364982670005/msa pfama37 --match-mode 1 --match-ratio 0.5 --threads 4 -v 3`

### Method 2: Execute the single commands required
> Download the Pfam-A.seed.gz file fron the Pfam web-page

> Convert the MSA
convertmsa tmp//18345222364982670005/db.msa.gz tmp//18345222364982670005/msa -v 3
> Create the profile DB
mmseqs msa2profile tmp//18345222364982670005/msa pfama37 --match-mode 1 --match-ratio 0.5 --threads 4 -v 3
> Index the profile DB
mmseqs createindex pfama37 tmp/ -k 5 -s 7 --threads 4 -v 3


### Pfam Database information  

#### Version 33.1
PfamA.seed MSA https://ftp.ebi.ac.uk/pub/databases/Pfam/releases/Pfam33.1/Pfam-A.seed.gz  
PfamA.clans https://ftp.ebi.ac.uk/pub/databases/Pfam/releases/Pfam33.1/Pfam-A.clans.tsv.gz  
userman https://ftp.ebi.ac.uk/pub/databases/Pfam/releases/Pfam33.1/userman.txt  
`Total families:` 18259  
`Families with clans:` 7165  
`Total clans:`	635

#### Version 35
PfamA.seed MSA https://ftp.ebi.ac.uk/pub/databases/Pfam/releases/Pfam35.0/Pfam-A.seed.gz  
PfamA.full MSA https://ftp.ebi.ac.uk/pub/databases/Pfam/releases/Pfam35.0/Pfam-A.full.gz  
Pfam-A.hmm.dat.gz https://ftp.ebi.ac.uk/pub/databases/Pfam/releases/Pfam35.0/Pfam-A.hmm.dat.gz
PfamA.clans https://ftp.ebi.ac.uk/pub/databases/Pfam/releases/Pfam35.0/Pfam-A.clans.tsv.gz  
userman https://ftp.ebi.ac.uk/pub/databases/Pfam/releases/Pfam35.0/userman.txt  
`Total families:` 19633  
`Families with clans:` 7769  
`Total clans:`	655