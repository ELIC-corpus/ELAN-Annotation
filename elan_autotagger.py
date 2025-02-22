#Updated January 2025 
#Created by Hareem Khokhar (hak86462@uga.edu)
#Updated by Keith Langston (langston@uga.edu)
#ELAN Autotagger for frequent word-forms

from sys import argv
import pandas as pd
import xml.etree.ElementTree as ET

#helper method to search for refnumber
def find_node_by_refnumber(node, refnumber):
  for annotation in node:
    if(annotation[0].attrib['ANNOTATION_REF'] == refnumber):
      return annotation[0][0]
  return None

#import list of words to be autotagged as a dataframe
wordlist_df = pd.read_csv("ckm_dictionary.csv")

#replace blank values with 0, that can be skipped over later
wordlist_df = wordlist_df.fillna(0)

#load ELAN file
filename = str(argv[1])
my_doc = ET.parse(filename)
myroot = my_doc.getroot()

#get pointers to speaker tiers
tier_words_speaker = myroot[3]
tier_lemma_speaker = myroot[4]
tier_pos_speaker = myroot[5]
tier_feats_speaker = myroot[6]
tier_gloss_speaker = myroot[7]
tier_lc_speaker = myroot[8]

#get pointers to interviewer tiers
tier_words_interviewer = myroot[12]
tier_lemma_interviewer = myroot[13]
tier_pos_interviewer = myroot[14]
tier_feats_interviewer = myroot[15]
tier_gloss_interviewer = myroot[16]
tier_lc_interviewer = myroot[17]

#Autotag interviewer words
for word in tier_words_interviewer:
    for index, row in wordlist_df.iterrows():
        if(word[0][0].text == row['Words']):
            tagged_word = word[0][0].text
            annotation_id = str(word[0].attrib['ANNOTATION_ID'])
            #set lemma
            lemma = find_node_by_refnumber(tier_lemma_interviewer, annotation_id)
            if(row['Lemma']!= 0):
                lemma.text = str(row['Lemma'])
            #set PoS
            pos = find_node_by_refnumber(tier_pos_interviewer, annotation_id)
            if(row['PoS']!= 0):
                pos.text = str(row['PoS'])
            #set feats
            feats = find_node_by_refnumber(tier_feats_interviewer, annotation_id)
            if(row['Feats']!= 0):
                feats.text = str(row['Feats'])
            #set gloss
            gloss = find_node_by_refnumber(tier_gloss_interviewer, annotation_id)
            if(row['Gloss']!= 0):
                gloss.text = str(row['Gloss'])
            #set lc
            lc = find_node_by_refnumber(tier_lc_interviewer, annotation_id)
            if(row['LC']!= 0):
                lc.text = str(row['LC'])

#Autotag speaker words
for word in tier_words_speaker:
    for index, row in wordlist_df.iterrows():
        if(word[0][0].text == row['Words']):
            tagged_word = word[0][0].text
            annotation_id = str(word[0].attrib['ANNOTATION_ID'])
            #set lemma
            lemma = find_node_by_refnumber(tier_lemma_speaker, annotation_id)
            if(row['Lemma']!= 0):
                lemma.text = str(row['Lemma'])
            #set PoS
            pos = find_node_by_refnumber(tier_pos_speaker, annotation_id)
            if(row['PoS']!= 0):
                pos.text = str(row['PoS'])
            #set feats
            feats = find_node_by_refnumber(tier_feats_speaker, annotation_id)
            if(row['Feats']!= 0):
                feats.text = str(row['Feats'])
            #set gloss
            gloss = find_node_by_refnumber(tier_gloss_speaker, annotation_id)
            if(row['Gloss']!= 0):
                gloss.text = str(row['Gloss'])
            #set lc
            lc = find_node_by_refnumber(tier_lc_speaker, annotation_id)
            if(row['LC']!= 0):
                lc.text = str(row['LC'])

#create the output file and write in the tagged data
file = open(argv[2], 'w')
file.write("""<?xml version="1.0" encoding="UTF-8"?>\n""")
file.close()
tree = ET.tostring(myroot)
with open(argv[2], 'a+b') as f:
   f.write(tree)
file.close()
