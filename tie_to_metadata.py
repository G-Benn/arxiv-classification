import pandas as pd
from bs4 import BeautifulSoup
import requests
import os
import time

"""
A piece of code that ties together the full text of a paper from Arxiv to its metadata like author, abstract, field/subfield, etc
"""

"""
Comments / TODOs, etc
- Should I save out in multiple formats? - yes, and multiple dfs - it's a long build
- Should I separate out all categories into a (sparse) df? Yes, encoding easier. subcategories may be more expensive
- Should I use both the OG paper_id (YYMM.####(#) and concat int - Y for performance as join key 
- 
"""


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
    print(soup.prettify())  # remove in final, for testing

    paper_id = soup.id.string
    all_categories = soup.categories.string
    categories_list = all_categories.split()
    authors = soup.authors.string
    abstract = soup.abstract.string
    title = soup.title.string

    print("paper ID:", paper_id)
    #print(all_categories)
    print("categories:", categories_list)
    print("Authors:", authors)
    print("Abstract:", abstract)
    print("Title:", title)
    
    return paper_id, categories_list, authors, abstract, title


def construct_initial_dfs():
    """
    Create the initial dfs that we'll append each entry to.
    3 dfs, to be separately joined later on the int_id
    Columns: paper_id, text, abstract, categories, authors, title
    """
    meta_df = pd.DataFrame(columns=['int_paper_id','paper_id','abstract','authors','title'], index=['int_paper_id'])
    categories_df = pd.DataFrame(columns=['int_paper_id','categories'], index=['int_paper_id'])
    text_df = pd.DataFrame(columns=['int_paper_id','text'], index=['int_paper_id'])
    
    return meta_df, categories_df, text_df


def save_out(df: pd.DataFrame, base_filename, pickle=True, hdf=True):
    """
    given the df and filename, save out to both a pickle and hdf file. This ensures that we don't lose access to the data at any point.
    """
    if pickle:
        print("Pickling")
        df.to_pickle(base_filename+".pkl", compression="gzip")
    if hdf:
        print("hdf-ing")
        df.to_hdf(base_filename+".h5", 'table')
    if ~pickle and ~hdf:
        print("Didn't save out anywhere!")
    pass


def create_int_id(str_id):
    """Given an ID in the form of YYMM.####(#), returns an int version as a key"""
    int_str = str_id.replace(".", "")
    return int(int_str)


if __name__ == "__main__":
    print("Executing test sequence!")
    filelist = os.listdir(os.getcwd())
    number_files = len(filelist)
    print(number_files, " to process!")
    
    idx = 1
    for file in [f for f in os.listdir(os.getcwd()) if f.endswith('.txt')]:
        print("On file", idx , file)
        paper_id = os.path.splitext(file)[0]
        
        retr_url = construct_retrieval_url(paper_id)
        
        web_paper_id, categories, authors, abstract, title = parse_out_metadata(retr_url)
        time.sleep(3) # We don't want to hammer arxiv, so wait 3 seconds between each retrieval
        idx = idx + 1

