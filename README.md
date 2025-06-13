# PythonNLP
This Python project implements a basic natural language processing (NLP) model that can analyze and classify text samples based on linguistic features. It compares unknown text against two known sources (e.g., Pete Davidson vs. Donald Trump) and predicts which source the unknown text is more likely to resemble.
This program:
- Cleans and preprocesses text
- Extracts linguistic features such as:
  - Word frequency
  - Word length distribution
  - Sentence length
  - Punctuation usage
  - Word stems (basic stemming algorithm)
- Compares new texts to two known sources using **log similarity scores**
- Predicts the more likely author of the new text
