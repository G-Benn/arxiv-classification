# arxiv-classification
Experimentation with Word2Vec, embeddings, and NLP using papers downloaded from arXiv
Projects to be attempted with this data:
    Clustering analysis and relation graph of each paper category
    NLP creation of paper abstract from full text of a paper
    Can we predict the category(ies) of a paper (with predicted likliehood) with the text?
    Basic analysis of who (category) uploads the most, has most authors, etc
        Most likely to just import a pdf as their final paper (annoying me)
    Can we predict if a paper had a positive vs negative vs explanatory result (sentiment analysis?)

Infrastructure:
    Pull down from S3 tar files
    run latex_to_txt.sh
    run tie_to_metadata.py
    (current) test and do initial cleaning in ReadCleanData.py/ipynd
        Swap to pure python for full implementation
    Create 2 files for word2vec and other exploration methods for multilabel classification
        Try both simple / extended classification
    Try other experimentations
Current months of files downloaded + preprocessed:
1801-12
1901-1902

Current months of files processed:
