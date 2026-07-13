'''
Core module
Blueprint for setbuilder
'''

class SetBuilder(object):
    '''
        Builds and manage the movie sets

        keeps track of selections in order
        
        nobj, selected are ordered lists
        nobj is ordered according to index of node objects
        not_selected is unordered

        index in selected represent order not the node indexes
        selected's elements are tied to their relative positions in list
        selected is expected to be passed to function in order as order is managed in frontend

        slack is duration remaining
    '''
    def __init__(self, minutes:int, nobj:list, sorted_:bool, selected=None): # nobj is a list of Node objects sorted or not
        if len(nobj)==0:
            raise ValueError("nobj cant be empty!")

        self.nobj=nobj
        self.selected=selected if selected is not None else []
        self.not_selected=[]
        self.slack=0

        if not sorted_:
            pass
            '''
            from apps.core import MergeSort 
            self.nobj = MergeSort.merge_sort(self.nobj,"index")
            '''

        for e in self.selected:
            self.slack+=e.duration

        if self.slack>minutes:
            raise ValueError("slack must be less than minutes")

        self.slack=minutes-self.slack

        for e in self.nobj:
            if not e.selected:
                self.not_selected.append(e)

    def select(self, nx):# nx is a Node object present in nobj
         if(nx.duration > self.slack): # select only if duration less than slack
             return False

         self.selected.append(nx)

         nx.selected = True
         nx.active = False

         if nx in self.not_selected:
             self.not_selected.remove(nx)
             self.slack -= nx.duration if nx.duration else 0 # check for none
            
         for node in self.not_selected:
             node_duration = node.duration if node.duration else 0 # check for none
             if self.slack >= node_duration:
                 node.active = True
             else:
                 node.active=False
         return True

    def deselect(self,r_index):# r_index is relative index of the selected Node object in the selected list
        try:
            self.selected[r_index].selected=False
            self.selected[r_index].active=False
            self.slack+=self.selected[r_index].duration

            self.not_selected.append(self.selected[r_index])
            self.selected.pop(r_index)

            for node in self.not_selected:
                node_duration = node.duration if node.duration else 0 # check for none
                if self.slack >= node_duration:
                    node.active = True
                else:
                    node.active=False
            return True

        except IndexError:
            return False
        
'''
# Setbuilder usage example

# set builder running on the collection of nodes
setz = SetBuilder.SetBuilder(1, nodes, False)

# select
print("selected:")
setz.select(setz.nobj[1])

for n in setz.nobj: # output
    print(n.out(fancify=True))

# deselect
setz.deselect(0)

for n in setz.nobj: # output
    print(n.out(fancify=True))        

'''
