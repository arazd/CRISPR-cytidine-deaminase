# gRNA designer for CRISPR cytidine deaminase

This repository contains open-source tools for gRNA design for CRISPR cytidine deaminase.

## Biology overview
### CRISPR-Cas9
<img src="images/crispr0.png" width="30%" style="float:right"/> 

CRISPR-Cas9 is a molecular system that can target specific DNA sequences and make cuts, allowing to perform genome editing by "turning off" some genes. 

CRISPR stands for <i>clustered regularly interspaced short palindromic repeats</i> - short DNA sequences originally found in bacteria, which serve as bacterial immune system and participate in anti-viral defence [1]. In bacterial cell these sequences are transcribed into short RNA sequences that guide the CRISPR-Cas9 system to matching sequences of DNA of the invading virus. Once target DNA is found, protein Cas9 performs a cut and blocks a target gene. This mechanism of defence allows bacteria to protect against viruses by turning off their important genes and, hence, killing the virus.

## CRISPR as genome editing tool
In 2013 the first CRISPR system was engineered to perform genome editing in mouse and human cells [2]. After that, the system became widely used in biomedical laboratories across the world as a genome editing tool.

The principle behing genome editing with CRISPR is "find and edit". Cas9 protein is matched with a specifically engineered **guide RNA** (or gRNA) that allows the system to find a DNA sequence that we want to edit. After complementary DNA is found, Cas9 protein cuts it. Instead of using Cas9, we can also use other DNA-editing proteins (like Cytidine deaminase).

### Cytidine deaminase
<img src="images/crispr2.png" width="80%" style="float:right"/> 
To overcome cutting the DNA with Cas9, researchers have developed a CRISPR-based system that allows to change a nucleotide in DNA that will result in subsequent mutation in the expressed protein. Cytidine base editors are engineered by fusing catalytically inactive "dead" Cas9 to a cytidine deaminase. CRISPR Cytidine deaminase system is targeted to a specific locus on DNA by its gRNA, where Cytidine deaminase performs a C -> T change on one DNA strand (G to A on the opposite strand). C to T conversion is bounded by a small editing window near PAM site on a locus determined by gRNA.

## How to use

## Examples of outputs
