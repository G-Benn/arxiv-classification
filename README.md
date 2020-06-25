# arxiv-classification
This repository is intended to serve as a holding place for exploratory analysis on large amounts of text data. This text data consists of all papers from arXiv from June 2017 - March 2019, approximately 220 000. 

## Data Collection:
    1. Pull down from .tar files from s3, as per [arXiv recommendations](https://arxiv.org/help/bulk_data_s3)  
    2. Convert raw LaTeX files to text. This utilizes [opendetex](https://github.com/pkubowicz/opendetex) to convert LaTeX files into text files and then names and stores them accordingly.  
    3. Tie each text file to the relevant metadata. This method involved numerous stop-and-retry methods due to the [metadata API](https://arxiv.org/help/oa/index) going down often. These metadata-tied files were pickled and saved.
    4. Combine Pickles in notebooks for usage as necessary
    5. Start experimentation!
    
   
## Project possibilities
Broadly speaking, the goal of this is to experiment with various NLP techniques and technologies like word and document embeddings, article generation, etc.  
Some initial ideas:  
    - Summary / abstract generation from full article text.  
    - Generate new arXiv articles using [GPT-2](https://openai.com/blog/better-language-models/).  
        - Initial results can be found in Article_Generation.  
    - Clustering analysis and relation graph of each paper category  
    -Paper category / subcategory classification given full text. Subcategories examined would have to be relatively limited due to potential to scale to every possible subcategory.  
    - Sentiment analysis (unsupervised) of a paper as a proxy for if a peper had a positive, negative, or neutral conclusion.  


