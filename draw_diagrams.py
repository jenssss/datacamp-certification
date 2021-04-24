from graphviz import Digraph, Graph
from itertools import combinations

def data_model1():
    dot = Digraph(comment="First data model")
    dot.node("m", "mileage")
    dot.node("p", "price")
    dot.edges(["mp"])
    dot.graph_attr["rankdir"] = "LR"
    return dot


def draw_new_and_usage_clusters(dot):
    new_car_config = ["model", "transmission", "fuelType", "engineSize", "year"]
    with dot.subgraph(name="clusterA") as c:
        c.attr(style="filled", color="lightgrey", shape="egg")
        for node in new_car_config:
            c.node(node)
        c.node_attr.update(style="filled", color="white")
        # for pair in combinations('mtfey', r=2):
        #    c.edge(*pair)
        # c.edges([('a0', 'a1'), ('a1', 'a2'), ('a2', 'a3')])
        c.attr(label="New car configuration")

    with dot.subgraph(name="clusterB") as c:
        c.attr(style="filled", color="lightgrey")
        c.node_attr.update(style="filled", color="white")
        c.node("mileage")
        c.attr(label="Usage")

    
def data_model2():

    dot = Graph(comment="Data model 2", engine="fdp")

    draw_new_and_usage_clusters(dot)

    features = ["price", "tax", "mpg"]
    short = "pag"

    with dot.subgraph(name="clusterC") as c:
        c.attr(style="filled", color="lightgrey")
        c.node_attr.update(style="filled", color="white")
        for node in features:
            c.node(node)
        c.attr(label="Predictables")

    # for s, feature in zip(short, features):
    #    dot.node(s, feature)

    dot.edge("clusterA", "mpg", dir="forward")
    dot.edge("clusterA", "tax", dir="forward", splines="ortho")
    dot.edge("clusterA", "price", dir="forward")
    dot.edge("clusterB", "price", dir="forward", splines="curved")
    # dot.edge('clusterA', 'clusterC', dir='forward')
    # dot.edge('clusterB', 'clusterC', dir='forward')
    dot.graph_attr["rankdir"] = "LR"
    # dot.unflatten()
    return dot

    
def data_model3():

    dot = Graph(
        comment="Data model 3",
        engine="fdp",
    )

    draw_new_and_usage_clusters(dot)

    features = ["price", "tax", "mpg"]
    short = "pag"

    with dot.subgraph(name="clusterC") as c:
        c.attr(style="filled", color="lightgrey")
        c.node_attr.update(style="filled", color="white")
        for node in ["tax", "mpg"]:
            c.node(node)
        c.attr(label="Others")


    dot.edge("clusterA", "price", dir="forward")
    dot.edge("clusterB", "price", dir="forward")
    dot.edge(
        "clusterC",
        "price",
        dir="forward",
        color="grey",
    )
    # dot.edge('clusterA', 'clusterC', dir='forward')
    # dot.edge('clusterB', 'clusterC', dir='forward')
    # dot.graph_attr['rankdir'] = 'LR'

    return dot
