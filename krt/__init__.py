class Graph():
    def __init__(self,label=None):
        if label is  None:
            label = "__UNDEF_"
        self.__edges__ = set([]) 
        self.__nodes__ = set([]) 
        self.__adjacency_list__ =  {} 
        self.__label__ = label 
        
    def __str__(self):
        return "<label=%s,nodes=%s,edges=%s>" % (self.__label__, len(self.__nodes__),len(self.__edges__))
    def add_node(self,v):
        if v not in self.__nodes__:
            self.__nodes__.add(v)
        if v not in self.__adjacency_list__:
            self.__adjacency_list__[v] = set([])
    
    def update(self,other_graph):
        self.__nodes__ =  self.__nodes__.union(other_graph.__nodes__)
        for e in other_graph.__edges__:
            self.add_edge(e[0],e[1]) 

    def union(self,other):
        g = Graph()
        edges = self.__edges__.union( other.__edges__ ) 
        nodes = self.__nodes__.union( other.__nodes__ ) 
        for e in edges:
            g.add_edge(e[0],e[1]) 
        for n in nodes:
            g.add_node(n) 

        return g 
    def add_edge(self,a,b):
        # Add new nodes to Nodes 
        [self.__nodes__.add(v)  for v in  (a,b) if v not in self.__nodes__]
        self.__edges__.add((a,b))
        
        #Add new entries into adjacency list 
        new_entries = [(v,set([]))  for v in  (a,b) if v not in self.__adjacency_list__]
        self.__adjacency_list__.update(dict(new_entries))
        
        if (a,b) not in self.__adjacency_list__[a]:
            self.__adjacency_list__[a].add(b)
        
    @staticmethod 
    def from_tuples(edges):
        g =  Graph() 
        for e in  edges:
            a =  e[0]
            b =  e[1]
            g.add_edge(a,b)
        return g 


class Traverser():
    DEPTH = "__depth__"
    NEIGHBOURS = "neighbours"
    def __init__(self):
        self.__component_groupers__ = {}

    def grouper_add(self,name,fn):
        self.__component_groupers__ [name] = fn


    def update_components(self):
        self.component_start_depths = {} 
        for name in self.__components__:
            self.__components__[name].append(None)

            c =  Graph("%s_%s" %  (name,len(self.__components__[name])) )
            self.__components__[name][-1]= c 

    def bfs(self,g):

        self.__components__ = {}
        self.__visited__ = set([])

        for node  in  list(g.__nodes__):
            if node in self.__visited__:
                continue
            self.update_components()  #  create a new iteration slot for the traversal
            self.__traversal_visited__ = set([])
            self.alg_bfs(g,node)

    def dfs(self,g):

        self.__components__ = {}
        self.__visited__ = set([])
        self.__iteration__ = 0 
        for node  in  list(g.__nodes__):
            if node in self.__visited__:
                continue
            self.update_components()  #  create a new iteration slot for the traversal
            self.__traversal_visited__ = set([])
            self.alg_dfs(g,node)

            self.component_start_depths = {} 
            self.__iteraton__ = self.__iteration__ + 1 


    def alg_dfs(self,g,node=None,depth=0):
        self.__visited__.add(node)
        self.__traversal_visited__.add(node)
        # context:  neighbours, depth
        neighbours = g.__adjacency_list__[node]

        if depth==0:
            self.update_components() 
        context = self.context( {"graph":g,Traverser.DEPTH:depth, "neighbours": neighbours}  )
        self.apply_component_lambdas(g,node=node,edge=None,context=context)
        for n in neighbours:


            context = self.context( {"graph":g,Traverser.DEPTH:depth, "neighbours": neighbours}  )
            self.apply_component_lambdas(g,node,(node,n),context)
            #self.apply_component_lambdas(g,node,(node,n),{"graph":g,Traverser.DEPTH:depth, "neighbours": neighbours})

            if n in self.__traversal_visited__:
                print self.__traversal_visited__  
                raise Exception("Cylce Detected  (%s,%s)" % (node,n))
            self.alg_dfs(g,node=n,depth=depth+1)


    def context(self,c):
        traversal_context = {"iteration": self.__iteration__  }
        traversal_context.update(c)
        return  traversal_context
    def alg_bfs(self,g,node=None,depth=0):

        self.__visited__.add(node)
        self.__traversal_visited__.add(node)


        # context:  neighbours, depth
        neighbours = g.__adjacency_list__[node]

        context = self.context( {"graph":g,Traverser.DEPTH:depth, "neighbours": neighbours}  )
        self.apply_component_lambdas(g,node=node,edge=None,context=context)
        for n in neighbours:


            self.apply_component_lambdas(g,node,(node,n),{"graph":g,Traverser.DEPTH:depth, "neighbours": neighbours})

            if n in self.__traversal_visited__:
                raise Exception("Cylce Detected  (%s,%s)" % (node,n))

        for n in neighbours:
            if n in self.__traversal_visited__:
                raise Exception("Cylce Detected  (%s,%s)" % (node,n))
            self.alg_bfs(g,node=n,depth=depth+1)


    def groups(self):
        return self.__components__

    
    def apply_component_lambdas(self,g,node,edge,context):

        for name in  self.__component_groupers__:
            if name not in self.component_start_depths:
                self.component_start_depths[name] = context[Traverser.DEPTH] 


            #iif self.__component_depth__
            fn = self.__component_groupers__[name]

            if (name in self.__components__) == False:
                self.__components__[name] = []
                c =  Graph("%s_%s" %  (name,0) )
                self.__components__[name].append(c) 
 
            elif self.component_start_depths[name] ==  context[Traverser.DEPTH]:
                c =  Graph("%s_%s" %  (name,len(self.__components__[name]) ))
                self.__components__[name].append(c) 


            c = self.__components__[name][-1]
            (n,e) = fn(node,edge,context)
            if e is not None:
                    c.add_edge(e[0],e[1])

            if n is not None:
                c.add_node(n)


