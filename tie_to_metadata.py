import numpy as np
import pandas as pd
import beautifulsoup4 as bs
import urllib3 as ul
import re

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
							base_url="http://export.arxiv.org/oai2?verb=GetRecord&identifier=oai:arXiv.org:###&metadataPrefix=arXiv",
							sub_chars="###"
							):
	"""
	Given the ID of a paper, sub it into the URL.
	:param paper_id : The ID of a paper, in the standard arXiv format. This should have been parsed from the filename in the format YYMM.##### (.txt).
	:param base_url : The base URL used to access arXiv metadata servers.
	:param sub_chars : The chars from the base_url that need to be substituted out.
	:returns retrieval_url: The url that we can use to retrieve the relevant metadata.
	"""
	pass
	
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
	pass
	
def construct_initial_df():
	"""
	Create the initial df that we'll append each entry to.
	Columns: paper_id, text, abstract, categories, authors, title
	"""
	pass

def save_out(df, base_filename, pickle=True, hdf=True):
	"""
	given the df and filename, save out to both a pickle and hdf file. This ensures that we don't lose access to the data at any point.
	"""
	pass

def create_int_id(str_id):
	"""Given an ID in the form of YYMM.####(#), returns an int version as a key"""
	pass

	
	