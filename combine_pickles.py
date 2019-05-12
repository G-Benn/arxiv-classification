# Combine all sectioned pickle files into a single df / pickle file
import glob
import pandas as pd

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
files = glob.glob('test_src/categories_df*.pkl')
categories_df = pd.concat([pd.read_pickle(fp) for fp in files], ignore_index=True)

# iterate over all expanded_categories_df
print('expanded categories')
files = glob.glob('test_src/expanded_categories_df*.pkl')
expanded_categories_df = pd.concat([pd.read_pickle(fp) for fp in files], ignore_index=True)

# iterate over all expanded_categories_df
print('meta')
files = glob.glob('test_src/meta_df*.pkl')
meta_df = pd.concat([pd.read_pickle(fp) for fp in files], ignore_index=True)

# iterate over all reduced_categories_df
print('reduced categories')
files = glob.glob('test_src/reduced_categories_df*.pkl')
reduced_categories_df = pd.concat([pd.read_pickle(fp) for fp in files], ignore_index=True)

# iterate over all text_df
print('text')
files = glob.glob('test_src/text_df*.pkl')
text_df = pd.concat([pd.read_pickle(fp) for fp in files], ignore_index=True)

# Save out to Pickle
print('pickling all')
categories_df.to_pickle("final_src/categories_df.pkl")
reduced_categories_df.to_pickle("final_src/reduced_categories_df.pkl")
expanded_categories_df.to_pickle("final_src/expanded_categories_df.pkl")
meta_df.to_pickle("final_src/meta_df.pkl")
text_df.to_pickle("final_src/text_df.pkl")
print('pickling completed')




