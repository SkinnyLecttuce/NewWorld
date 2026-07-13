'''
Helper module
Tools for stuff
'''

import datetime as dt

from apps.core import MergeSort
from apps.core import Node

# filtering and sorting isn't supported by api's /search/ method
def the_filter(packets:list, filters:dict):
    '''
    Filters raw packets
    can use multiple filters
    filter's explicitly instead of filtering based on intersects
    '''

    filtered_packets = []

    if (len(filters) > 0):
        for packet in packets:
            purity = False
            for filter, value in filters.items():
                if (not type(packet[filter]) == type([1]) and not type(packet[filter]) == type({1})):  # support atomic datatypes
                    if (packet[filter] == value):
                        purity = True
                    else:
                        purity = False
                        break

                elif (type(packet[filter]) == type([1]) or type(packet[filter]) == type({1})):  # support lists and sets
                    k_set = set(packet[filter])  # force to a set
                    v_set = set(value)  # force to a set
                    if (v_set.issubset(k_set)):  # if filtered classes are in packet
                        purity = True
                    else:
                        purity = False
                        break

                else:  # no filter is applied, invalid datatype
                    raise TypeError("datatype for that filter is not supported")

            if (purity):  # pure aryan blood is found
                filtered_packets.append(packet)

        packets = filtered_packets

    return packets

def the_sorter(nodes:list, sorters:dict):
    '''
    Sort nodes
    use only one sorter per time
    if multiple selected, the last sorter will be used
    '''
    for sort_type,way in sorters.items():
        sort_type=sort_type.strip().lower() # making sure the attributes are valid
        way = way.strip().lower()  # making sure the attributes are valid
        try: # check attributes validity
            nodes=MergeSort.merge_sort(nodes,sort_type) # call generic merge sort

            if(way=="desc"): # merge sort output is always ascending
                nodes.reverse()  # flip

        except AttributeError:
            raise TypeError("datatype for that sorter is not supported")

    return nodes

def packets_to_node_objects(packets): # obvious enough
    nodes=[]
    for packet in packets:
        n = Node.Node()
        n.index = int(packet['id'])
        n.title = packet['title']
        n.director = 'batman'
        n.rating = packet['vote_average']
        n.rating_count = packet['vote_count']
        n.adult = packet['adult']
        n.popularity = packet['popularity']
        n.genre = packet['genre_ids']
        n.original_language = packet['original_language']
        n.overview = packet['overview']
        n.selected = False
        n.active = False

        divided = packet['release_date'].strip().split('-')

        for i in range(0,len(divided)): # check if invalid type
            try:
                int(divided[i])

            except ValueError or TypeError:
                n.release_date = 'invalid_type'

        if not n.release_date == 'invalid_type': # only check length if it's not invalid_type
            if(len(divided[0]) == 4 and len(divided[1]) == 2 and len(divided[2]) == 2): # valid datetime format
                n.release_date = dt.date(int(divided[1]),int(divided[1]),int(divided[2])) # convert to datetime object
            else:
                n.release_date = 'invalid_len'

        n.duration = int(packet['runtime'])
        nodes.append(n)

    return nodes

'''
# Filtration usage examples

# packets_in must be in [{'detail_x':x,'detail_y':y, ... ,'detail_n':n}] format, refer TMDB_API_Handler query_search() function return
# filter non-adult, english, animation-sci-fi movies
filtered_packets = the_filter(packets_in,filters={'adult':False, 'original_language':'en', 'genre_ids':[16,878]}) 

# Sortation usage examples

# nodes must be a list of node objects 
nodes = the_sorter(nodes,sorters={'popularity':'asc'}) #sort in popularity ascending order

# Raw packets to node objects usage examples
# packets_in must be in [{'detail_x':x,'detail_y':y, ... ,'detail_n':n}] format, refer TMDB_API_Handler query_search() function return
nodes = packets_to_node_objects(packets_in)
'''