# Ties together all the metadata in a way that can be picked up and resumed at any time.

import pandas as pd
import re
import os
import pickle
import requests
from bs4 import BeautifulSoup
import argparse

def construct_retrieval_url(paper_id,
                            base_url="http://export.arxiv.org/oai2?verb=GetRecord&identifier=oai:arXiv.org:###&metadataPrefix=arXivRaw",
                            sub_chars="###"
                            ):
    """
    Given the ID of a paper, sub it into the URL.
    :param paper_id : The ID of a paper, in the standard arXiv format. This should have been parsed from the filename in the format YYMM.##### (.txt).
    :param base_url : The base URL used to access arXiv metadata servers.
    :param sub_chars : The chars from the base_url that need to be substituted out.
    :returns retrieval_url: The url that we can use to retrieve the relevant metadata.
    """
    retr_url = base_url.replace(sub_chars, paper_id)
    return retr_url


# TODO Test this guy
def parse_out_metadata(url_to_read):
    """
    Given the URL, parse out all of the metadata that we want access to.
    :param url_to_read : The URL that we'll refer to.
    :returns paper_id : The id of the paper
    :returns all_categories: list. All of the categories that a paper belongs in.
    :returns authors: list. All the authors credited for the paper.
    :returns abstract: string. The abstract of the paper.
    :returns title: string. The title of the paper.
    """
    raw_html = requests.get(url_to_read)

    soup = BeautifulSoup(raw_html.text, 'html.parser')
    #print(soup.prettify())  # remove in final, for testing

    paper_id = soup.id.string
    all_categories = soup.categories.string
    categories_list = all_categories.split()
    authors = soup.authors.string
    abstract = soup.abstract.string
    title = soup.title.string

    print("paper ID:", paper_id)
    #print(all_categories)
    #print("categories:", categories_list)
    #print("num_categories:", len(categories_list))
    #print("Authors:", authors)
    #print("Abstract:", abstract)
    #print("Title:", title)
    
    return paper_id, categories_list, len(categories_list), authors, abstract, title


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


def create_int_id(str_id):
    """Given an ID in the form of YYMM.####(#), returns an int version as a key"""
    int_str = str_id.replace(".", "")
    return int(int_str)

def divide_chunks(l, n): 
      
    # looping till length l 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 

parser = argparse.ArgumentParser(description='Either run the initial setup or complete a main run, pickin up where you left off.')

parser.add_argument('--setup',action='store_true',
                   help='Run the initial setup of the full chunks to run')
                   
args = parser.parse_args()

if args.setup:
    print('creating pickle and chunks')
    all_files = [f for f in os.listdir(os.getcwd()) if f.endswith('.txt')]
    all_chunks = list(divide_chunks(all_files, 25)) #test with 5, final with 50
    with open('remaining_chunks.pkl', 'wb') as fp:
            pickle.dump(all_chunks, fp)
    print('File dumped! Exiting now.')
    exit()
        
with open ('remaining_chunks.pkl', 'rb') as fp:
    print('opening chunks')
    all_chunks = pickle.load(fp)

print('First set of files', all_chunks[0])

# Grab from remaining_chunks, which will be made manually once separately
while all_chunks: # While all_chunks is not empty 
    chunk = all_chunks.pop(0) # Take the first element and remove it from the list
    print(chunk)
    meta_df, categories_df, reduced_categories_df, expanded_categories_df, text_df = construct_initial_dfs() #remake every time
    for filename in chunk:
        # do tying
        paper_id = os.path.splitext(filename)[0]
        
        opened_file = open(filename, mode='r', encoding="utf8")
        try:
            full_text = opened_file.read()
        except UnicodeDecodeError as e:
            print("Unicode decoding error - prooably latin-1 instead of utf-8. Ignoring.")
            # TODO Modify so that when this fails we swap to latin-1, try that, then give up
            continue # Just skip the file and forget about it
        opened_file.close()
        
        retr_url = construct_retrieval_url(paper_id)
        
        web_paper_id, categories, num_categories, authors, abstract, title = parse_out_metadata(retr_url)
        
        int_paper_id = create_int_id(web_paper_id)

        # TODO add in steps to allow index to be used for speed(?)
        meta_dict = { 
            'int_paper_id': int_paper_id,
            'paper_id': web_paper_id,
            'abstract': abstract,
            'authors': authors,
            'title': title
        }
        meta_df = meta_df.append(meta_dict, ignore_index=True)
        
        categories_dict = {
            'int_paper_id': int_paper_id,
            'num_categories': num_categories,
            'categories': categories
        }
        categories_df = categories_df.append(categories_dict, ignore_index=True)
        
        reduced_categories = [i.split('.')[0] for i in categories]
        
        reduced_categories_dict = dict.fromkeys(reduced_categories, 1)
        reduced_categories_dict['int_paper_id'] = int_paper_id
        reduced_categories_df = reduced_categories_df.append(reduced_categories_dict, ignore_index=True)
        
        expanded_categories_dict = dict.fromkeys(categories, 1)
        expanded_categories_dict['int_paper_id'] = int_paper_id
        expanded_categories_df = expanded_categories_df.append(expanded_categories_dict, ignore_index=True)
        
        text_dict = {
            'int_paper_id': int_paper_id,
            'text': full_text
        }
        text_df = text_df.append(text_dict, ignore_index=True)
        
    # save out these metadate_dfs with name being chunk[0]-chunk[-1]_NAME       
    section = chunk[0] + '-' + chunk[-1]
    save_out(meta_df, "meta_df_"+section)
    save_out(categories_df, "categories_df_"+section)
    save_out(reduced_categories_df, "reduced_categories_df_"+section)
    save_out(expanded_categories_df, "expanded_categories_df_"+section)
    save_out(text_df, "text_df_"+section)
    
    # removal of chunk from list happened at the start with pop, but it won't be saved out until these are all done
    # update all_chunks
    with open('remaining_chunks.pkl', 'wb') as fp:
        print('updating chunks')
        pickle.dump(all_chunks, fp)
print('Completely done!')
print('deleting remaining_chunks.pkl')
os.remove('remaining_chunks.pkl')





