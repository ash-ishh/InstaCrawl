# InstaCrawl
quick and dirty python + shell script to scrape instagram pictures (public and private).

InstaCrawl.py uses selenium.It refreshes instagram profile untill all pictures are loaded.
then it saves the sources code to file.

InstaCrawl.sh pulls all the links of pictures from source code file and downloads using wget.
