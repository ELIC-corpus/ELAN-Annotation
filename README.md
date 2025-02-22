# ELAN-Annotation
This repository contains two Python scripts to facilitate the annotation of ELAN files with lexical and grammatical information for the ELIC project. 

1. elan_autotagger

Syntax for running the script: $ python elan_autotagger.py InputFileName OutputFileName

This script takes a dictionary file (in .csv format), with column headers Words, Lemma, PoS, Feats, Gloss, LC (for language contact phenomena, coded Y/N) and an input ELAN file with the same tier names for a Speaker and Interviewer and automatically adds the annotations for the individual word-forms to the ELAN file.

The output file will be recreated under the name you choose each time you run the script. Make sure the output file name you give is distinct from the input file name and that it ends with '.eaf' so it can be opened with ELAN.

The name for the .csv dictionary file is hard-coded in the script (under comment #import list of words..., line 18). As long as you update the dictionary file and keep it in the same folder as the autotagger script, it will be able to handle new additions to the autotag list, as the script reloads the list each time it is run

TROUBLESHOOTING: If you get an error saying you do not have the pandas package installed, please run the following command in your terminal: pip install pandas. Try running the script again after the installation has completed.

The input or output files do not necessarily need to be in the same folder as the script, as long as you specify the full file path.

ELAN tiers are referenced by their position relative to the root of the xml document (i.e., the .eaf file): Header = 0, Time Order = 1, Text@SpeakerID = 2, Words@SpeakerID = 3, etc. The order of tiers is based on the ELAN template created for the ELIC project (revised in November 2024).

This script can easily be adapted for other projects: column headers in the dictionary file should correspond to the tier structure used in ELAN, and the variable names and references in the script should be changed accordingly.

2. annotations_to_dict

Syntax for running the script: $ python annotations_to_dict.py elan_file.eaf output.csv (using the appropriate file names for the ELAN file and the dictionary file)

This script takes an annotated ELAN file and creates a .csv dictionary file (columns: Words, Lemma, PoS, Feats, Gloss, LC), corresponding to the tiers used for annotation in the ELIC project.

The script can also be used to update an existing dictionary file. Put the file name of the existing dictionary in place of output.csv. The script will check for an existing file by that name, and if one exists, it will generate a new version output_updated.csv. The script also checks for duplicate entries and will only add words that are not already in the existing dictionary file.

As with the elan_autotagger script, ELAN tiers are referenced by their position relative to the root of the xml document (= .eaf file). The script can easily be modified for use in other projects.
