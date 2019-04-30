import pandas as pd

text_df = pd.read_pickle('text_df_test.pkl')
meta_df = pd.read_pickle('meta_df_test.pkl')
categories_df = pd.read_pickle('categories_df_test.pkl')
expanded_categories_df('expanded_categories_df_test.pkl')


with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(text_df)
    print(meta_df)
    print(categories_df)
    print(expanded_categories_df)