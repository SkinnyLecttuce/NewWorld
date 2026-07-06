import Node

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
    def __init__(self, hours:int, nobj:list, sorted_:bool, selected=None):
        if len(nobj)==0:
            raise ValueError("nobj cant be empty!")

        self.nobj=nobj
        self.selected=selected if selected is not None else []
        self.not_selected=[]
        self.slack=0

        if not sorted_:
            import MergeSort 
            self.nobj = MergeSort.merge_sort(self.nobj)

        for e in self.selected:
            self.slack+=e.duration

        if self.slack>hours:
            raise ValueError("slack must be less than hours")

        self.slack=hours-self.slack

        for e in self.nobj:
            if not e.selected:
                self.not_selected.append(e)
        
    def select(self, nx):
         self.selected.append(nx)
         nx.selected = True

         if nx in self.not_selected:
             self.not_selected.remove(nx)
             self.slack -= nx.duration if nx.duration else 0 #check for none
            
         for node in self.not_selected:
             node_duration = node.duration if node.duration else 0 #check for none
             if self.slack >= node_duration:
                 node.active = True
             else:
                 node.active=False

    def deselect(self,r_index):
        try:
            self.selected[r_index].selected=False
            self.selected[r_index].active=False
            self.slack+=self.selected[r_index].duration

            self.not_selected.append(self.selected[r_index])
            self.selected.pop(r_index)

            for node in self.not_selected:
                node_duration = node.duration if node.duration else 0 #check for none
                if self.slack >= node_duration:
                    node.active = True
                else:
                    node.active=False
                     
        except IndexError:
            pass
        
            
