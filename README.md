### Challenges with Using Primer IDs to Improve Accuracy of Next Generation Sequencing

#### Johanna Brodin, Charlotte Hedskog, Alexander Heddini, Emmanuel Benard, Richard A. Neher, Mattias Mild, Jan Albert
#### [PLoS ONE 10(3): e0119123](http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0119123)
#### Abstract
Next generation sequencing technologies, like ultra-deep pyrosequencing (UDPS), allows detailed investigation of complex populations, like RNA viruses, but its utility is limited by errors introduced during sample preparation and sequencing. By tagging each individual cDNA molecule with barcodes, referred to as Primer IDs, before PCR and sequencing these errors could theoretically be removed. Here we evaluated the Primer ID methodology on 257,846 UDPS reads generated from a HIV-1 SG3Δenv plasmid clone and plasma samples from three HIV-infected patients. The Primer ID consisted of 11 randomized nucleotides, 4,194,304 combinations, in the primer for cDNA synthesis that introduced a unique sequence tag into each cDNA molecule. Consensus template sequences were constructed for reads with Primer IDs that were observed three or more times. Despite high numbers of input template molecules, the number of consensus template sequences was low. With 10,000 input molecules for the clone as few as 97 consensus template sequences were obtained due to highly skewed frequency of resampling. Furthermore, the number of sequenced templates was overestimated due to PCR errors in the Primer IDs. Finally, some consensus template sequences were erroneous due to hotspots for UDPS errors. The Primer ID methodology has the potential to provide highly accurate deep sequencing. However, it is important to be aware that there are remaining challenges with the methodology. In particular it is important to find ways to obtain a more even frequency of resampling of template molecules as well as to identify and remove artefactual consensus template sequences that have been generated by PCR errors in the Primer IDs.


### ANALYSIS OF PRIMER ID SEQUENCING DATA 
#### Code by Emmanuel Benard and Richard A. Neher
##### step 1:

COMMAND: python src/p1_trim_and_filter.py configfile

this will check each read for 5' and 3' primer matches (soft matching via Smith Waterman alignment) and split the reads according to their bar codes. filtered_read.fasta files will be deposited in labeled directories. 

##### step 2:

COMMAND: python src/p2_sort.py run_directory read_type

this will split the reads according to their pIDs into a largish number of temporary directories. All pIDs within each directory will be aligned by a cluster job. The parameter read_type specifies whether this is to be done one the filtered or corrected reads. In any case, the script looks for a file named  read_type+"_reads.fasta"

##### step 3:

COMMAND: python src/p3_cluster_align.py run_directory

Starts a cluster job for each of the temp directory in each of the barcode directories inside the run_directory. 

##### step 4:

COMMAND: python src/p4_consensus.py run_directory read_type

This script goes over all barcodes in the run directory, gathers the aligned read files in the temporary directory of the desired read type, and builds consensus sequences. it also writes all aligned reads into a single file. 

##### step 5:

COMMAND: python src/p5_decontamination.py bar_code_directory ref_seqs read_type true_seq_id

This script takes the aligned reads from one barcode and checks whether the individuals reads or the consensus sequence alignes reasonably well to the reference sequence with the true_seq_id. If a read does not, it is checked against all other reference sequences. All reads that don't align well to their own reference sequence are written into an extra file. 

alternatively to submit batch-jobs to the cluster:

COMMAND: python src/p5_decontamination.py run_directory ref_seqs read_type true_seq_id

##### step 6:

COMMAND: python src/p6_detect_mutants_indels.py barcode_dir read_type

Check whether PIDs of low abundance reads are less than a certain edit distance from a high abundance one. Designate a neighbor if reads in addition align well. Produce read files with likely_pIDs and original PIDs. 

After this step, the sorting, alignment and consensus steps (2-4) need to be redone with readtype corrected instead of filtered. 
