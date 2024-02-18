from neo4j import GraphDatabase

class Interface:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)
        self._driver.verify_connectivity()

    def close(self):
        self._driver.close()

    def bfs(self, start_node, last_node):
        # TODO: Implement this method
        try:
            session = self._driver.session()
            graph_query = f'''
            CALL gds.graph.project("bfsGraph", 
            {{
                Location: {{
                    properties: "name"
                }}
            }}, 
            {{    
                TRIP: {{
                    properties: ["distance", "fare"]
                }}
            }});
            '''
            session.run(graph_query)
            bfs_query = f'''
            MATCH (a:Location{{name:{start_node}}}), (d:Location{{name:{last_node}}})
            WITH id(a) AS source, [id(d)] AS targetNodes
            CALL gds.bfs.stream('bfsGraph', {{
                sourceNode: source,
                targetNodes: targetNodes
            }})
            YIELD path
            RETURN path
            '''
            result = session.run(bfs_query)
            data = result.data()
            return data
        except Exception as e:
            print(e)
            raise NotImplementedError

    def pagerank(self, max_iterations, weight_property):
        # TODO: Implement this method
        try:
            session = self._driver.session()
            damping_factor = 0.85
            graph_query = f'''
            CALL gds.graph.project("pageRankGraph", 
            {{
                Location: {{
                    properties: "name"
                }}
            }}, 
            {{    
                TRIP: {{
                    properties: ["distance", "fare"]
                }}
            }});
            '''
            session.run(graph_query)
            pageRank_query = f"""
                CALL gds.pageRank.stream("pageRankGraph", {{
                maxIterations: {max_iterations},
                dampingFactor: {damping_factor},
                relationshipWeightProperty: "{weight_property}"
                }})
                YIELD nodeId, score
                RETURN gds.util.asNode(nodeId).name AS name, score
                ORDER BY score DESC;
            """            
            pageRank_result = session.run(pageRank_query)
            data = pageRank_result.data()
            results = [data[0]] + [data[-1]]
            return results
                
        except Exception as e:
            print(e)
            raise NotImplementedError

