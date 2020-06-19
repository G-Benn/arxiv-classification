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
- Iteratively creating catagories_df every run with unique column title of each category that will get appended (part of one-hot encoding)
"""
categories_with_desc = {
    "astro-ph.GA" : "Astrophysics of Galaxies",
    "astro-ph.CO" : "Cosmology and Nongalactic Astrophysics",
    "astro-ph.EP" : "Earth and Planetary Astrophysics",
    "astro-ph.HE" : "High Energy Astrophysical Phenomena",
    "astro-ph.IM" : "Instrumentation and Methods for Astrophysics",
    "astro-ph.SR" : "Solar and Stellar Astrophysics",
    "cond-mat.dis-nn" : "Disordered Systems and Neural Networks",
    "cond-mat.mtrl-sci" : "Materials Science",
    "cond-mat.mes-hall" : "Mesoscale and Nanoscale Physics",
    "cond-mat.other" : "Other Condensed Matter",
    "cond-mat.quant-gas" : "Quantum Gases",
    "cond-mat.soft" : "Soft Condensed Matter",
    "cond-mat.stat-mech ": "Statistical Mechanics",
    "cond-mat.str-el" : "Strongly Correlated Electrons",
    "cond-mat.supr-con" : "Superconductivity",
    "physics.acc-ph" : "Accelerator Physics",
    "physics.app-ph" : "Applied Physics",
    "physics.ao-ph" : "Atmospheric and Oceanic Physics",
    "physics.atom-ph" : "Atomic Physics",
    "physics.atm-clus" : "Atomic and Molecular Clusters",
    "physics.bio-ph" : "Biological Physics",
    "physics.chem-ph" : "Chemical Physics",
    "physics.class-ph" : "Classical Physics",
    "physics.comp-ph" : "Computational Physics",
    "physics.data-an" : "Data Analysis, Statistics and Probability",
    "physics.flu-dyn" : "Fluid Dynamics",
    "physics.gen-ph" : "General Physics",
    "physics.geo-ph" : "Geophysics",
    "physics.hist-ph" : "History and Philosophy of Physics",
    "physics.ins-det" : "Instrumentation and Detectors",
    "physics.med-ph" : "Medical Physics",
    "physics.optics" : "Optics",
    "physics.ed-ph" : "Physics Education",
    "physics.soc-ph" : "Physics and Society",
    "physics.plasm-ph" : "Plasma Physics ",
    "physics.pop-ph" : "Popular Physics",
    "physics.space-ph" : "Space Physics",
    "math.AG" : "Algebraic Geometry",
    "math.AT" : "Algebraic Topology ",
    "math.AP" : "Analysis of PDEs",
    "math.CT" : "Category Theory",
    "math.CA" : "Classical Analysis and ODEs",
    "math.CO" : "Combinatorics ",
    "math.AC" : "Commutative Algebra",
    "math.CV" : "Complex Variables",
    "math.DG" : "Differential Geometry",
    "math.DS" : "Dynamical Systems",
    "math.FA" : "Functional Analysis",
    "math.GM" : "General Mathematic",
    "math.GN" : "General Topology",
    "math.GT" : "Geometric Topology",
    "math.GR" : "Group Theory",
    "math.HO" : "History and Overview",
    "math.IT" : "Information Theory",
    "math.KT" : "K-Theory and Homology",
    "math.LO" : "Logic",
    "math.MP" : "Mathematical Physics ",
    "math.MG" : "Metric Geometry",
    "math.NT" : "Number Theory",
    "math.NA" : "Numerical Analysis",
    "math.OA" : "Operator Algebras",
    "math.OC" : "Optimization and Control ",
    "math.PR" : "Probability",
    "math.QA" : "Quantum Algebra",
    "math.RT" : "Representation Theory",
    "math.RA" : "Rings and Algebras",
    "math.SP" : "Spectral Theory",
    "math.ST" : "Statistics Theory",
    "math.SG" : "Symplectic Geometry",
    "nlin.AO" : "Adaptation and Self-Organizing Systems",
    "nlin.CG" : "Cellular Automata and Lattice Gases",
    "nlin.CD" : "Chaotic Dynamics",
    "nlin.SI" : "Exactly Solvable and Integrable Systems",
    "nlin.PS" : "Pattern Formation and Solitons",
    "q-bio.BM" : "Biomolecules",
    "q-bio.CB" : "Cell Behavior",
    "q-bio.GN" : "Genomics",
    "q-bio.MN" : "Molecular Networks",
    "q-bio.NC" : "Neurons and Cognition",
    "q-bio.OT" : "Other Quantitative Biology",
    "q-bio.PE" : "Populations and Evolution",
    "q-bio.QM" : "Quantitative Methods",
    "q-bio.SC" : "Subcellular Processes",
    "q-bio.TO" : "Tissues and Organs",
    "q-fin.CP" : "Computational Finance ",
    "q-fin.EC" : "Economics",
    "q-fin.GN" : "General Finance",
    "q-fin.MF" : "Mathematical Finance",
    "q-fin.PM" : "Portfolio Management",
    "q-fin.PR" : "Pricing of Securities",
    "q-fin.RM" : "Risk Management",
    "q-fin.ST" : "Statistical Finance",
    "q-fin.TR" : "Trading and Market Microstructure",
    "stat.AP" : "Applications",
    "stat.CO" : "Computation" ,
    "stat.ML" : "Machine Learning",
    "stat.ME" : "Methodology",
    "stat.OT" : "Other Statistics",
    "stat.TH" : "Statistics Theory",
    "eess.AS" : "Audio and Speech Processing",
    "eess.IV" : "Image and Video Processing ",
    "eess.SP" : "Signal Processing",
    "econ.EM" : "Econometrics",
    "econ.GN" : "General Economics ",
    "econ.TH" : "Theoretical Economics",
    "cs.AI" : "Artificial Intelligence",
    "cs.CC" : "Computational Complexity",
    "cs.CG" : "Computational Geometry",
    "cs.CE" : "Computational Engineering, Finance, and Science",
    "cs.CL" : "Computation and Language (Computational Linguistics and Natural Language and Speech Processing) ",
    "cs.CV" : "Computer Vision and Pattern Recognition ",
    "cs.CY" : "Computers and Society",
    "cs.CR" : "Cryptography and Security",
    "cs.DB" : "Databases",
    "cs.DS" : "Data Structures and Algorithms",
    "cs.DL" : "Digital Libraries ",
    "cs.DM" : "Discrete Mathematics",
    "cs.DC" : "Distributed, Parallel, and Cluster Computing ",
    "cs.ET" : "Emerging Technologies",
    "cs.FL" : "Formal Languages and Automata Theory",
    "cs.GT" : "Computer Science and Game Theory",
    "cs.GL" : "General Literature",
    "cs.GR" : "Graphics",
    "cs.AR" : "Hardware Architecture ",
    "cs.HC" : "Human-Computer Interaction",
    "cs.IR" : "Information Retrieval",
    "cs.IT" : "Information Theory",
    "cs.LG" : "Machine Learning ",
    "cs.LO" : "Logic in Computer Science",
    "cs.MS" : "Mathematical Software ",
    "cs.MA" : "Multiagent Systems",
    "cs.MM" : "Multimedia ",
    "cs.NI" : "Networking and Internet Architecture",
    "cs.NE" : "Neural and Evolutionary Computation",
    "cs.NA" : "Numerical Analysis ",
    "cs.OS" : "Operating Systems",
    "cs.OH" : "Other",
    "cs.PF" : "Performance" ,
    "cs.PL" : "Programming Languages",
    "cs.RO" : "Robotics" ,
    "cs.SI" : "Social and Information Networks ",
    "cs.SE" : "Software Engineering",
    "cs.SD" : "Sound ",
    "cs.SC" : "Symbolic Computation",
    "cs.SY" : "Systems and Control "
}

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
    print("num_categories:", len(categories_list))
    print("Authors:", authors)
    print("Abstract:", abstract)
    print("Title:", title)
    
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


def save_out(df: pd.DataFrame, base_filename, pickle=True, hdf=True):
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

if __name__ == "__main__":
    print("Executing test sequence!")
    filelist = os.listdir(os.getcwd())
    number_files = len(filelist)
    print(number_files, " to process!")
    
    meta_df, categories_df, reduced_categories_df, expanded_categories_df, text_df = construct_initial_dfs()
    
    idx = 1
    all_files = [f for f in os.listdir(os.getcwd()) if f.endswith('.txt')]
    
    all_chunks = list(divide_chunks(all_files, 100)) 
    
    for filename in [f for f in os.listdir(os.getcwd()) if f.endswith('.txt')]:
        print("On file", idx , filename)
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
        #time.sleep(3) # We don't want to hammer arxiv, so wait 3 seconds between each retrieval
        
        # TODO redo categories 
        
        idx = idx + 1
    save_out(meta_df, "meta_df_test")
    save_out(categories_df, "categories_df_test")
    save_out(reduced_categories_df, "reduced_categories_df_test")
    save_out(expanded_categories_df, "expanded_categories_df_test")
    save_out(text_df, "text_df_test")

