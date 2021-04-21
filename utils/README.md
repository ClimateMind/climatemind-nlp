## Steps to gathering data from pocket

* pocket_extract.py: pocket_data --> pocket_data_metadata

* diffbot_scraping_articles.py: partial pocket_data_metadata (diffbot input) --> diffbot_output

* process_extracted_text.py: diffbot_output + pocket_data_metadata --> complete_data_AND_metadata

* split_sentences.py: complete_data_AND_metadata --> split_complete_data_AND_metadata
