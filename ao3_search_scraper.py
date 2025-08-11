import requests
import time
import random

'''Customization options start here:'''

# MANDATORY. Go to AO3 and make the search you want, then click to page 2.
# Copy the URL of that page and paste it in place of the below example.
# Then write {page} inside the URL in place of the 2 that is there because you went to page 2.
# (As of this writing, the format should be page=2, so you write page={page})
URL = "https://archiveofourown.org/works/search?commit=Search&page={page}&work_search%5Bbookmarks_count%5D=&work_search%5Bcharacter_names%5D=Dr.+Mensah+%28Murderbot+Diaries%29%2CAmena+%28Murderbot+Diaries%29&work_search%5Bcomments_count%5D=&work_search%5Bcomplete%5D=&work_search%5Bcreators%5D=&work_search%5Bcrossover%5D=&work_search%5Bfandom_names%5D=The+Murderbot+Diaries+-+Martha+Wells&work_search%5Bfreeform_names%5D=&work_search%5Bhits%5D=&work_search%5Bkudos_count%5D=&work_search%5Blanguage_id%5D=&work_search%5Bquery%5D=&work_search%5Brating_ids%5D=&work_search%5Brelationship_names%5D=&work_search%5Brevised_at%5D=&work_search%5Bsingle_chapter%5D=0&work_search%5Bsort_column%5D=_score&work_search%5Bsort_direction%5D=asc&work_search%5Btitle%5D=&work_search%5Bword_count%5D="
TOTAL_PAGES = 7 # minimum 1. change this to the total number of pages the search result gives you

# The below options control which field of each work entry the script will extract.
# The defaults given work for an author search but you'll have to experiment for anything else.
# Changing these involves inspecting the HTML ("Inspect Element").
# There are two separate pairs of start/end strings to account for hrefs and the like
# that may vary for each element but which you don't want to include in your end result.
# For instance, the following defaults work when I'm interested in the author "FigOwl" between the tags
# in "<a rel="author" href="/users/FigOwl/pseuds/FigOwl">FigOwl</a>"
TAG_START = '<a rel="author"' # a string that only appears at the beginning of each element you're interested in
TAG_END = '/a>' # a string at the end of each element. Can appear elsewhere in the page but not inside the element
TERM_START = '>' # a string that reliably appears just before the ACTUAL WORDS you want to keep
TERM_END = '<' # a string that reliably appears just AFTER the actual words you want to keep

# optional, these defaults are fine
OUTPUT_FILE = "ao3_search_scraper_output.txt" # desired name of the results file
SLEEP_SECS_ADD = 7 # base number of seconds to wait between pages (avoids ratelimiting)
SLEEP_SECS_COEFF = 5 # some fraction of this number of seconds will be added to the above for randomness

'''Customization options end. Script starts here.'''


found = []

for page in range(1, TOTAL_PAGES+1):

    
    url = URL.format(page=page)
    response = str(requests.get(url).content)

    start_ind = 0
    end_ind = 0

    print("scraping...")
    
    while start_ind >= 0:

        start_ind = response.find(TAG_START, end_ind) # find next instance since the previous entry's ending index
        end_ind = response.find(TAG_END, start_ind) # find index of closing html tag for this instance
        term = response[start_ind:end_ind]
    
        term = term[term.find(TERM_START)+1 : term.find(TERM_END, term.find(TERM_START))]
        found.append(term)

    to_sleep = SLEEP_SECS_COEFF * random.random() + SLEEP_SECS_ADD
    print(f"page {page} out of {TOTAL_PAGES} scraped, waiting {to_sleep:.2f} seconds")
    time.sleep(to_sleep)

print("sorting authors alphabetically...")
found.sort()

print(f"writing {len(found)} authors to {OUTPUT_FILE}...")
with open(OUTPUT_FILE, "w") as file:
        for term in found:
            file.write(term + "\n")

print("done!")