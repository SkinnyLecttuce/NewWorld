class Node(object):
    '''The fundamental atom holding shite together'''
    def __init__(self):
        self.hours = None
        self.index = None
        self.deadend = None   #experimentals 
        self.ascendants = []  #experimentals
        self.descendants = [] #experimentals 
        self.slack = None     #experimentals 
        self.active = None
        self.selected = None
        self.duration = None
                    
    def out(self, fancify=False):
        if fancify:
            return {
                "hours": self.hours, 
                "index": self.index, 
                "deadend": self.deadend, 
                "ascendants": [e.index for e in self.ascendants], 
                "descendants": [e.index for e in self.descendants],
                "slack":self.slack,
                "active":self.active,
                "selected":self.selected,
                "duration":self.duration
            }
        else:
            return [self.hours, self.index, self.deadend, self.ascendants, self.descendants, self.slack, self.active, self.selected, self.duration]

    '''
    ***Experimental functions***

    def add_ascendants(self, acc: list): 
        if not isinstance(acc, list): 
            raise TypeError("add_ascendants expects a list type parameter")
        
        for e in acc:
            if e not in self.ascendants:
                self.ascendants.append(e) #update self ascendants object array
                e.add_descendants([self]) #update connected descendants object array

    def delete_ascendants(self, target_nodes: list):
        if not isinstance(target_nodes, list):
            raise TypeError("target_nodes must be a list")
        if len(target_nodes) == 0:
            raise ValueError("target_nodes list cannot be empty")
        
        remaining_ascendants = []
        for e in self.ascendants:
            if e in target_nodes:
                self.ascendants = [x for x in self.ascendants if x != e] #remove e from self ascendants array before calling connected descendants to delete connection, stop recursive loop
                e.delete_descendants([self])
            else:
                remaining_ascendants.append(e)
                
        self.ascendants = remaining_ascendants

    def add_descendants(self, desc: list):
        if not isinstance(desc, list):
            raise TypeError("add_descendants expects a list type parameter")
        
        for e in desc:
            if e not in self.descendants:
                self.descendants.append(e) #same comment as line 17 but for descendants
                e.add_ascendants([self])   #same comment as line 18 but for ascendants

    def delete_descendants(self, target_nodes: list):
        if not isinstance(target_nodes, list):
            raise TypeError("target_nodes must be a list")
        if len(target_nodes) == 0:
            raise ValueError("target_nodes list cannot be empty")
        
        remaining_descendants = []
        for e in self.descendants:
            if e in target_nodes:
                self.descendants = [x for x in self.descendants if x != e] #same comment as line 29 but descendant and ascendants
                e.delete_ascendants([self])
            else:
                remaining_descendants.append(e)
                
        self.descendants = remaining_descendants
        '''
