class Graph:
    def __init__(self, directed=False):
        self.directed = directed
        self.graph = {}          # uzel -> seznam sousedu
        self.weights = {}        # (u,v) -> vaha (volitelne)

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = []

    def add_edge(self, u, v, weight=None):
        self.add_node(u)
        self.add_node(v)
        self.graph[u].append(v)
        if not self.directed:
            self.graph[v].append(u)
        if weight is not None:
            self.weights[(u, v)] = weight
            if not self.directed:
                self.weights[(v, u)] = weight

    def has_loops(self):
        for node in self.graph:
            if node in self.graph[node]:
                return True
        return False

    def is_weighted(self):
        return len(self.weights) > 0

    def print_graph(self):
        print("Graf vypada takhle:")
        for node in self.graph:
            print(node, "->", self.graph[node])
        if self.is_weighted():
            print("Vahy:", self.weights)

    def analyze(self):
        print("=== Analyza grafu ===")
        self.print_graph()
        print()
        print("Orientovany:", self.directed)
        print("Ohodnoceny:", self.is_weighted())
        print("Ma smycky:", self.has_loops())
        print("Pocet uzlu:", len(self.graph))
        
        edges = 0
        for node in self.graph:
            edges += len(self.graph[node])
        if not self.directed:
            edges //= 2
        print("Pocet hran:", edges)

        # planarita? (totalne blby check)
        if len(self.graph) <= 4:
            print("Planarni: asi jo (malej graf)")
        else:
            print("Planarni: nevim, to je moc tezky")

        # chromaticky cislo (jeste blbejsi)
        print("Chromaticke cislo: neco mezi 1 a", len(self.graph))
        print("=====================")


# rychly test
g = Graph(directed=False)
g.add_edge(1, 2)
g.add_edge(2, 3, weight=5)
g.add_edge(1, 1)   # smycka
g.analyze()