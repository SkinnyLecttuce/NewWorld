'''
Core module
Blueprint for nodes
'''

class Node(object):
    '''The fundamental atom holding shite together

    structure
            self.index(int)
            self.title(str)
            self.rating(float)
            self.director(list)
            self.duration(int)
            self.active(bool)
            self.selected(bool)


            #experimentals
            self.deadend(bool)
            self.ascendants(list)
            self.descendants(list)
            self.slack(bool)
    '''
    def __init__(self):
        self.index = None
        self.title = None
        self.rating = None
        self.director = None
        self.duration = None
        self.active = None
        self.selected = None
        self.adult = None
        self.original_language = None
        self.release_date = None
        self.popularity = None
        self.rating_count = None
        self.genre = []
        self.overview = None

        self.deadend = None  # experimentals
        self.ascendants = []  # experimentals
        self.descendants = []  # experimentals
        self.slack = None  # experimentals
                    
    def out(self, fancify=False):
        if fancify:
            return {
                "index": self.index,
                "title": self.title,
                "rating": self.rating,
                "director": self.director,
                "duration": self.duration,
                "active":self.active,
                "selected":self.selected,
                "adult":self.adult,
                "original_language":self.original_language,
                "release_date":self.release_date,
                "popularity":self.popularity,
                "rating_count":self.rating_count,
                "genre":self.genre,
                "overview":self.overview,

                # experimental
                "deadend": self.deadend,
                "ascendants": [e.index for e in self.ascendants],
                "descendants": [e.index for e in self.descendants],
                "slack": self.slack
            }
        else:
            return [self.index, self.title, self.rating, self.director, self.adult,
                    self.original_language, self.release_date, self.popularity, self.rating_count, self.genre, self.overview,

                    # experimental
                    self.duration, self.active, self.selected, self.deadend, self.ascendants]
    '''
    ***Experimental functions***

    def add_ascendants(self, acc: list): 
        if not isinstance(acc, list): 
            raise TypeError("add_ascendants expects a list type parameter")
        
        for e in acc:
            if e not in self.ascendants:
                self.ascendants.append(e) # update self ascendants object array
                e.add_descendants([self]) # update connected descendants object array

    def delete_ascendants(self, target_nodes: list):
        if not isinstance(target_nodes, list):
            raise TypeError("target_nodes must be a list")
        if len(target_nodes) == 0:
            raise ValueError("target_nodes list cannot be empty")
        
        remaining_ascendants = []
        for e in self.ascendants:
            if e in target_nodes:
                self.ascendants = [x for x in self.ascendants if x != e] # remove e from self ascendants array before calling connected descendants to delete connection, stop recursive loop
                e.delete_descendants([self])
            else:
                remaining_ascendants.append(e)
                
        self.ascendants = remaining_ascendants

    def add_descendants(self, desc: list):
        if not isinstance(desc, list):
            raise TypeError("add_descendants expects a list type parameter")
        
        for e in desc:
            if e not in self.descendants:
                self.descendants.append(e) # same comment as line 17 but for descendants
                e.add_ascendants([self])   # same comment as line 18 but for ascendants

    def delete_descendants(self, target_nodes: list):
        if not isinstance(target_nodes, list):
            raise TypeError("target_nodes must be a list")
        if len(target_nodes) == 0:
            raise ValueError("target_nodes list cannot be empty")
        
        remaining_descendants = []
        for e in self.descendants:
            if e in target_nodes:
                self.descendants = [x for x in self.descendants if x != e] # same comment as line 29 but descendant and ascendants
                e.delete_ascendants([self])
            else:
                remaining_descendants.append(e)
                
        self.descendants = remaining_descendants
        '''
