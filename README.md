# radiology-nlp
Project for importing IBD related radiology documents, automatically annotating them, and creating visual interface and classifier

## Project Goal
Create a tool that can classify radiology documents based on the location of IBD related activity, and the presence of complications.
Accomplish this in a way that is designed to be portable across hospital systems, and allows for explainability, expert review and collaboration. 

## Tasks accomplished by this project
- Cleans and imports radiology notes found in large csv file
- Separates each report into individual .txt files (which contain labels) for visualization in Brat annotation tool
  - Creates related .ann files related for visualization of concepts and relations in Brat
- Uses formal publication pertaining to stricture related activity terms, curated dictionary, and UMLS anatomy features to automatically annotate radiology reports
  - Leverages and expands funcitonality of QuickUMLS package in locating UMLS terms (and in the future more rigorously determining dependencies)
- Uses the generated annotations as part of a feature set for use in a classifier to automatically classify notes based on location and the presence of complicaitons
