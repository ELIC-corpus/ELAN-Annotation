# ELAN annotations to dictionary script
# created by Agustin Lorenzo Oct 2024
# revised by Keith Langston v1.2 Jan 2025

import pandas as pd
import xml.etree.ElementTree as ET
from sys import argv
import os


# helper functions for getting data and finding annotations
def extract_data_from_tier(tier, tier_type):
    data = []

    for annotation in tier:
        word = annotation[0][0].text

        if word:
            word = word.encode('utf-8').decode('utf-8', 'replace').strip()
            if word.endswith('-'): # ignore cut-off words
                continue
        else:
            continue  

        annotation_id = annotation[0].attrib['ANNOTATION_ID']
        data.append({'Tier_Type': tier_type, 'Word': word, 'Annotation_ID': annotation_id})
        
    return data


def find_annotation_by_refnumber(tier, refnumber):
    for annotation in tier:
        if 'ANNOTATION_REF' in annotation[0].attrib:
            if annotation[0].attrib['ANNOTATION_REF'] == refnumber:
                return annotation[0][0].text or ''
    return ''  


# loading ELAN file and checking for correct usage
if len(argv) < 3:
    print("Usage: python script_name.py input_file.eaf output_file.csv")
    exit(1)

filename = str(argv[1])
my_doc = ET.parse(filename)
myroot = my_doc.getroot()


# pointers to speaker and interviewer tiers
tiers = {
    'Words_Speaker': myroot[3],
    'Lemma_Speaker': myroot[4],
    'PoS_Speaker': myroot[5],
    'Feats_Speaker': myroot[6],
    'Gloss_Speaker': myroot[7],
    'LC_Speaker': myroot[8],
    'Words_Interviewer': myroot[12],
    'Lemma_Interviewer': myroot[13],
    'PoS_Interviewer': myroot[14],
    'Feats_Interviewer': myroot[15],
    'Gloss_Interviewer': myroot[16],
    'LC_Interviewer': myroot[17]
}


# get data from each tier
extracted_data = []
for tier_name, tier in tiers.items():
    if 'Words' in tier_name:
        extracted_data.extend(extract_data_from_tier(tier, tier_name))

df = pd.DataFrame(extracted_data)


# adding annotations
df['Lemma'] = ''
df['PoS'] = ''
df['Feats'] = ''
df['Gloss'] = ''
df['LC'] = ''

for index, row in df.iterrows():
    tier_prefix = 'Speaker' if 'Speaker' in row['Tier_Type'] else 'Interviewer'
    annotation_id = row['Annotation_ID']

    lemma = find_annotation_by_refnumber(tiers[f'Lemma_{tier_prefix}'], annotation_id)
    pos = find_annotation_by_refnumber(tiers[f'PoS_{tier_prefix}'], annotation_id)
    feats = find_annotation_by_refnumber(tiers[f'Feats_{tier_prefix}'], annotation_id)
    gloss = find_annotation_by_refnumber(tiers[f'Gloss_{tier_prefix}'], annotation_id)
    lc = find_annotation_by_refnumber(tiers[f'LC_{tier_prefix}'], annotation_id)
    
    df.at[index, 'Lemma'] = lemma
    df.at[index, 'PoS'] = pos
    df.at[index, 'Feats'] = feats
    df.at[index, 'Gloss'] = gloss
    df.at[index, 'LC'] = lc


# clean current dataframe columns        
df = df.drop(columns=['Annotation_ID', 'Tier_Type'])
df.rename(columns={'Word': 'Words'}, inplace=True)


# checking if specified output file is an already preexisting dictionary
output_filename = argv[2]
if os.path.exists(output_filename):
    previous_dict = pd.read_csv(output_filename)
    base, ext = os.path.splitext(output_filename)
    output_filename = f"{base}_updated{ext}" # save to separate .csv to avoid potential overriting mistakes
    previous_dict.fillna('', inplace=True)
    string_columns = ['Words', 'Lemma', 'PoS', 'Feats', 'Gloss', 'LC']
    for col in string_columns:
        previous_dict[col] = previous_dict[col].astype(str).str.strip()
else:
    previous_dict = pd.DataFrame(columns=df.columns)


# combining previous dictionary with current dataframe and removing duplicates
df.fillna('', inplace=True)
df.replace(to_replace=[None], value='', inplace=True)
string_columns = ['Words', 'Lemma', 'PoS', 'Feats', 'Gloss', 'LC']

for col in string_columns:
    df[col] = df[col].astype(str).str.strip()

if 'Word' in previous_dict.columns:
    previous_dict = previous_dict.drop(columns=['Word'])

df = pd.concat([previous_dict, df], ignore_index=True)
df.drop_duplicates(subset=['Words'], inplace=True)
df.dropna(how='all', inplace=True)


# save to .csv
df.to_csv(output_filename, index=False, encoding='utf-8-sig')
