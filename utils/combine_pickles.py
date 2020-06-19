# Combine all sectioned pickle files into a single df / pickle file
import glob
import pandas as pd
import numpy as np

def construct_initial_dfs():
    """
    Create the initial dfs that we'll append each entry to.
    4 dfs, to be separately joined later on the int_paper_id
    Columns: paper_id, text, abstract, categories, expanded_categories, authors, title
    """
    meta_df = pd.DataFrame(columns=['int_paper_id','paper_id','abstract','authors','title'], index=['int_paper_id'])
    categories_df = pd.DataFrame(columns=['int_paper_id','num_categories','categories'], index=['int_paper_id'], dtype='object')
    text_df = pd.DataFrame(columns=['int_paper_id','text'], index=['int_paper_id'])
    expanded_categories_df = pd.DataFrame(columns=['int_paper_id'], index = ['int_paper_id'])
    reduced_categories_df = pd.DataFrame(columns=['int_paper_id'], index = ['int_paper_id'])
    
    return meta_df, categories_df, reduced_categories_df, expanded_categories_df, text_df

meta_df, categories_df, reduced_categories_df, expanded_categories_df, text_df = construct_initial_dfs()
#iterate over all pickles
# No failsafe built in if it fails; I'll just have to deal with it then. 5+ GB of files so likely will come up.

# iterate over all categories_df
print('Category dfs')
files = glob.glob('src/categories_df*.pkl')
categories_df = pd.concat([pd.read_pickle(fp) for fp in files], ignore_index=True)
categories_df['int_paper_id'] = pd.to_numeric(categories_df['int_paper_id'])
categories_df['num_categories'] = pd.to_numeric(categories_df['num_categories'])
print(categories_df.info(memory_usage='deep'))

# iterate over all expanded_categories_df
print('expanded categories')
files = glob.glob('src/expanded_categories_df*.pkl')
expanded_categories_df = pd.concat([pd.read_pickle(fp) for fp in files], ignore_index=True)
print(expanded_categories_df.info(memory_usage='deep'))

# iterate over all expanded_categories_df
print('meta')
files = glob.glob('src/meta_df*.pkl')
meta_df = pd.concat([pd.read_pickle(fp) for fp in files], ignore_index=True)
meta_df['int_paper_id'] = pd.to_numeric(meta_df['int_paper_id'])
meta_df['paper_id'] = pd.to_numeric(meta_df['int_paper_id'])
meta_df['abstract'] = meta_df['abstract'].astype(str)
meta_df['title'] = meta_df['title'].astype(str)
print(meta_df.info(memory_usage='deep'))

# iterate over all reduced_categories_df
print('reduced categories')
files = glob.glob('src/reduced_categories_df*.pkl')
reduced_categories_df = pd.concat([pd.read_pickle(fp) for fp in files], ignore_index=True)
print(reduced_categories_df.info(memory_usage='deep'))

# iterate over all text_df
print('text')
files = glob.glob('src/text_df*.pkl')
text_df = pd.concat([pd.read_pickle(fp) for fp in files], ignore_index=True)
print(int(text_df.shape[0]/2))
half_len = int(text_df.shape[0]/2)
text_df_a = text_df.iloc[:,:half_len]
text_df_b = text_df.iloc[:,half_len:]

#text_df_a = text_df_a.astype({'text': str, 'int_paper_id': np.float64})
#text_df['text'] = text_df['text'].astype('|S')
print('a')
print(text_df_a.info(memory_usage='deep'))
#text_df_b = text_df_b.astype({'text': str, 'int_paper_id': np.float64})
#text_df['text'] = text_df['text'].astype('|S')
print('b')
print(text_df_b.info(memory_usage='deep'))

# Save out to Pickle
print('pickling categories')
categories_df.to_pickle("final_src/categories_df.pkl")
print('pickling reduced categories')
reduced_categories_df.to_pickle("final_src/reduced_categories_df.pkl")
print('pickling expanded categories')
expanded_categories_df.to_pickle("final_src/expanded_categories_df.pkl")
print('skip pickling meta')
#meta_df.to_pickle("final_src/meta_df.pkl")
print('pickling text')
text_df_a.to_pickle("final_src/text_df_a.pkl")
text_df_b.to_pickle("final_src/text_df_b.pkl")




