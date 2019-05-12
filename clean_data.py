"""
Given the input pickles, clean up all the data and combine it
"""

import pandas as pd
import re
from nltk.corpus import stopwords
import matplotlib.pyplot as plt

text_df = pd.read_pickle('final_src/text_df.pkl')
meta_df = pd.read_pickle('final_src/meta_df.pkl')
categories_df = pd.read_pickle('final_src/categories_df.pkl')
reduced_categories_df = pd.read_pickle('final_src/reduced_categories_df.pkl')
expanded_categories_df = pd.read_pickle('final_src/expanded_categories_df.pkl')

# Remove the 1st row of each df that's there to hold the original shape.
text_df.drop(text_df.index[0], inplace=True)
meta_df.drop(meta_df.index[0], inplace=True)
categories_df.drop(categories_df.index[0], inplace=True)
reduced_categories_df.drop(reduced_categories_df.index[0], inplace=True)
expanded_categories_df.drop(expanded_categories_df.index[0], inplace=True)


# Make sure the categories are encoded correctly
reduced_categories_df.fillna(0, inplace=True)
reduced_categories_df = reduced_categories_df.astype(int, inplace=True)
expanded_categories_df.fillna(0,inplace=True)
expanded_categories_df = expanded_categories_df.astype(int, inplace=True)

# Clean up the text and abstract datasets
REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
TRIM_SPACE_RE = re.compile(r'\s+')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
STOPWORDS = set(stopwords.words('english'))
CAT_TO_REPLACE_RE = re.compile(r'\.|-')


def clean_text(text):
    """
        text: a string
        
        return: modified initial string
    """
    text = text.lower() # lowercase text
    text = REPLACE_BY_SPACE_RE.sub(' ', text) # replace REPLACE_BY_SPACE_RE symbols by space in text
    text = TRIM_SPACE_RE.sub(' ', text)
    text = BAD_SYMBOLS_RE.sub('', text) # delete symbols which are in BAD_SYMBOLS_RE from text
    text = ' '.join(word for word in text.split() if word not in STOPWORDS) # delete stopwors from text
    return text

text_df['cleantext'] = text_df['text'].apply(clean_text)
text_df['length'] = text_df['cleantext'].apply(len)
text_df = text_df[text_df['length'] != 0]

meta_df['cleanabstract'] = meta_df['abstract'].apply(clean_text)

# Add string columns to categories
categories_df['string_categories'] = categories_df['categories'].apply(', '.join)
categories_df['string_categories1'] = categories_df['string_categories'].apply(lambda x: CAT_TO_REPLACE_RE.sub('_',x))
categories_df['string_categories2'] = categories_df['string_categories'].apply(lambda x: CAT_TO_REPLACE_RE.sub('',x))

def save_out(df: pd.DataFrame, base_filename, pickle=True, hdf=False):
    """
    given the df and filename, save out to both a pickle and hdf file. This ensures that we don't lose access to the data at any point.
    """
    if pickle:
        print("Pickling")
        df.to_pickle(base_filename+".pkl")
    if hdf:
        print("hdf-ing")
        df.to_hdf(base_filename+".h5", 'table', complevel=9)
    if not pickle and not hdf:
        print("Didn't save out anywhere!")
        

info_df = text_df.merge(meta_df, on='int_paper_id', how='inner')
full_expanded_df = expanded_categories_df.merge(info_df, on='int_paper_id', how='inner')
full_reduced_df = reduced_categories_df.merge(info_df, on='int_paper_id', how='inner')

save_out(full_expanded_df, 'final_src/clean_expanded_df')
save_out(full_reduced_df, 'final_src/clean_reduced_df')
save_out(info_df, 'final_src/clean_info_df')
save_out(categories_df, 'final_src/clean_categories_df')