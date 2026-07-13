'''
Core module
Manage TMDB API communication
'''

import shutil
import requests
import datetime as dt
import json
import gzip
import io
import asyncio
import aiohttp
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

api_key_file_path = os.path.join(CURRENT_DIR, "api_key.txt")
download_log_file_path = os.path.join(CURRENT_DIR, "log.txt")

api_key = ''

wordlist={} #holds a map of keywords and their ids

def dummy_call():
    '''Test api calls'''
    dummy_url=f"https://api.themoviedb.org/3/search/movie?query=Star+Wars"
    res=req(dummy_url)
    print(res)

def req(url):
    '''
    Template for any non-async requests
    '''
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    try:
        response = requests.get(url, headers=headers) #see if success
        response_json = response.json()             #jsonify
        return response_json
    except:
        raise Exception("connection error, most probable")

def auth_token():
    '''
    Authenticate with TMDB API
    '''
    global api_key
    global api_key_file_path
    global CURRENT_DIR

    url_auth_check = "https://api.themoviedb.org/3/authentication"

    keyfile = open(api_key_file_path, "r")

    api_key = keyfile.read().strip()               #get api_key from file

    if(len(api_key) == 0):
        raise Exception(f"API key not provided, edit {api_key_file_path}")

    response=req(url_auth_check)    #get the response

    if(not response["success"]):
        raise Exception(f"invalid API key, see {os.path.join(CURRENT_DIR, 'api_key.txt')}")

    return True


def download(url: str, outfile: str) -> bool:
    '''
    Download .gz from url and extract file from gz
    expects outfile to be the .json destination
    '''
    global CURRENT_DIR

    if(outfile.find(".json") == -1):
        raise TypeError("outfile must be a json file")

    print(f"downloading[{url}]...")

    outgz=os.path.join(CURRENT_DIR,f"{outfile.split('.')[0]}.gz") #outfile.gz is gonna be the original .gz

    with requests.get(url, stream=True) as response: #download
        response.raise_for_status()                  #raise for http errors

        with open(outgz, 'wb') as file: #write chunk by chunk
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

    print(f"extracting[{outgz} to {outfile}]...")
    with gzip.open(outgz, 'rb') as file: #extract
        #the download .gz format file's content isn't in .json format
        #this part converts it to valid .json format
        fk=io.BytesIO(file.read().replace(b'\n',b','))

        file_content = io.BytesIO(b'['+fk.read()) #create a file object in memory with edits

        file_content.seek(-2, 2)  # pointer to last 2 bytes of the io object
        file_content.write(b'}] ') #replace last 2 bytes
        file_content.seek(0)      #reset pointer to file beginning

        with open(outfile, 'wb') as out:
            shutil.copyfileobj(file_content, out) #write file object to outfile

    return True

def spawn_wordlist():
    '''
    Get dem words in heir in .json format
    '''
    global wordlist
    global download_log_file_path

    outfile="wordlist.json"
    outfile = os.path.join(CURRENT_DIR, outfile)

    try:
        with open(download_log_file_path, "r") as log:
            last_download_date=log.read().strip()[14:]

    except FileNotFoundError:
        with open(download_log_file_path, "w") as log:
            log.write('')

    yesterday = dt.datetime.today()-dt.timedelta(days=1)    #retrive yesterday's keyword list
    current_date=f"{yesterday.strftime('%m')}_{yesterday.strftime('%d')}_{yesterday.strftime('%Y')}" #convert to correct format

    wordlist_gz_url = f"https://files.tmdb.org/p/exports/keyword_ids_{current_date}.json.gz"

    if(current_date.strip() != last_download_date.strip()): #skip download if log says already downloaded
        if(download(wordlist_gz_url, outfile)): #download yesterday's keyword list
            print("got wordlist")
            try:
                with open(download_log_file_path, "w") as log:
                    log.write(f"last_download:{yesterday.strftime('%m')}_{yesterday.strftime('%d')}_{yesterday.strftime('%Y')}")

            except: #some unhandled error
                return False

    try:
        with open(outfile, 'r', encoding='utf-8') as file: #downloaded or not open the latest outfile
            for record in json.load(file):  # create wordlist dict {keyword:id}
                wordlist[record['name']] = record['id']

    except FileNotFoundError: #no outfile
        return False

    return True

def text_to_keyword_id(text: str):
    '''Text is tokenised then transformed to relevant keyword ids'''
    global wordlist
    translated_words=[]
    for t in text.split(' '):
       try:
           translated_words.append(wordlist[t]) #query the wordlist
       except KeyError:   #only accept key errors
           pass
    return translated_words

def keyword_search(keywords:list,max_pages:int):
    '''Get search results based on keywords'''
    if(len(keywords) == 0):
        raise Exception("no valid keywords found")

    list_to_keyword_string = str([key for key in keywords])[1:len(str(keywords)) - 1].replace(",","|")

    res_arr=[]
    for page in range(1,max_pages):
        keyword_search_url = f"https://api.themoviedb.org/3/discover/movie?with_keywords={list_to_keyword_string}&language=en&sort_by=popularity.desc&&page={page}"
        res_arr.append(req(keyword_search_url))

    return res_arr

async def async_req(url, session):
    '''Template for async requests'''

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    session.headers.update(headers)

    try:
        async with session.get(url) as response:
            if response.status == 200:
                response_json = await response.json()
                return response_json.get('runtime') or 1
    except Exception:
        pass
    return 0

async def process_packets(packets):
    '''Manage sessions for async requests'''

    async with aiohttp.ClientSession() as session: #fire several async http sessions
        tasks=[]

        for item in packets:
            url = f"https://api.themoviedb.org/3/movie/{item['id']}"
            tasks.append(async_req(url,session)) #spawn async individual sessions for each url

        runtimes = await asyncio.gather(*tasks) #create main handler for async tasks then wait for full completion

    for item, runtime in zip(packets, runtimes): #zip the items against runtime and create Node objects
        item['runtime'] = int(runtime)

    return packets

def query_search(query:str,max_pages:int):
    '''Get search results based on a query'''
    #filter 'adult', 'genre_ids', 'original_language', 'release_date'
    #sort 'popularity', 'vote_average', 'vote_count', 'release_date'

    keywords=[q for q in query.split(' ') if q]
    query_url = f"https://api.themoviedb.org/3/search/movie?query="

    for keyword in keywords:
        query_url = query_url + keyword + '+'

    query_url.rstrip()
    query_url+='&'

    packets = []

    for page in range(1, max_pages):
        keyword_search_url = query_url+f"&language=en&page={page}"
        packets+=req(keyword_search_url)['results']

    packets = asyncio.run(process_packets(packets)) #async api calls cuz responses are big as fuck

    #dispatchsation
    return packets

'''
# Query search usage example:

from apps.core import SetBuilder
from apps.core import Utils

auth_token() # always auth before anything

# return raw packets for search query
packets=query_search("Star Wars",5)

# filtration
packets = Utils.the_filter(packets,filters={'adult':False, 'original_language':'en', 'genre_ids':[16,878]})

if(len(packets)):# not zero packet length
    # packets to node objects
    nodes = Utils.packets_to_node_objects(packets)

    # sortation
    nodes = Utils.the_sorter(nodes,sorters={'popularity':'asc'}) # sort popularity ascending
    
    for n in nodes: # print the nodes
        print(n.out(fancify=True))
    
else:
    print("no results")

# Keyword based search usage example:

# IMO this feature is bad cuz tmdb's keyword id to movie map is shitty  

auth_token() # always auth before anything

if(spawn_wordlist()):   # retreive wordlist
    keyword_ids = text_to_keyword_id("Star wars")   # text to keyword id 
    print("word ids:",keyword_ids)              
    res_pages = keyword_search(keyword_ids,50)      # retrive 50 pages of results
    #print(res_pages)
    for page in res_pages:  
        for block in page['results']:
            print(block['original_title'])  # print retreived titles
'''