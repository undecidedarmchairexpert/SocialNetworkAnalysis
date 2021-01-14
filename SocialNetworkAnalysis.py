import sys
import networkx as nx
from pyvis import network as net

# Set variable for edge color
main_edge_color = "#00b4ff"


# This function draws an interactive nx object using Pyvis
# Valid node attributes include: "size", "value", "title", "x", "y", "label", "color".
# Valid edge attributes include: "arrowStrikethrough", "hidden", "physics", "title", "value", "width"
# Args -> show_buttons: Show buttons in saved version of network?
def interactive_graph(graph, prd_mode=False):
    # Create the Pyvis network object
    if prd_mode:
        sna_visualisation = net.Network(height="100%", width="100%")
    else:
        sna_visualisation = net.Network(height="100%", width="65%")
    # Add each node to the Pyvis object along with it's attributes
    for nodes, attributes in graph.nodes(data=True):
        sna_visualisation.add_node(nodes, **attributes)

    # for each edge and its attributes in the networkx graph
    for source, target, attributes in graph.edges(data=True):
        # if value/width not specified directly, and weight is specified, set 'value' to 'weight'
        if 'value' not in attributes and 'width' not in attributes and 'weight' in attributes:
            # place at key 'value' the weight of the edge
            attributes['value'] = attributes['weight']
        # add the edge
        sna_visualisation.add_edge(source, target, **attributes)

    # If not work in production mode, show buttons
    if not prd_mode:
        sna_visualisation.show_buttons()
    if prd_mode:
        # Options are set by exporting them from the non prd mode for the specific graph originally created
        # You may need to change these for your graph
        sna_visualisation.set_options("""
            var options = {
              "nodes": {
                "borderWidth": 3,
                "color": {
                  "border": "rgba(0,0,0,1)",
                  "background": "rgba(103,116,127,1)",
                  "highlight": {
                    "border": "rgba(0,0,0,1)",
                    "background": "rgba(252,255,252,1)"
                  }
                },
                "font": {
                  "size": 16,
                  "strokeWidth": 5
                },
                "size": 10
              },
              "edges": {
                "color": {
                  "inherit": true
                },
                "smooth": false
              },
              "physics": {
                "barnesHut": {
                  "gravitationalConstant": -23350
                },
                "minVelocity": 0.75
              }
            }
        """)

    # Save web page and return graph object
    return sna_visualisation.show("sna.html")


# Creates a friend group in an nx graph from a "core" and an "extended" graph
# The core list are all added with weights of 5 between each other
# The extended list is connected to all nodes, but with a weight of 1
# This function does not return anything
# The graph to which the objects are added is passed to the function and added directly
def create_friend_group(graph, core_list=None, ext_list=None):
    # Mutable object check
    if ext_list is None:
        ext_list = []
    if core_list is None:
        core_list = []
    # Iterate over core list and add links
    for person1 in core_list:
        for person2 in core_list:
            if person1 != person2:
                graph.add_edge(person1, person2, weight=5, color=main_edge_color)
        for person2 in ext_list:
            graph.add_edge(person1, person2, weight=1, color=main_edge_color)
    # Iterate over extended list and add links between each other
    for person1 in ext_list:
        for person2 in ext_list:
            if person1 != person2:
                graph.add_edge(person1, person2, weight=1, color=main_edge_color)


# Start of script
# Determine run mode from arguments passed to the scrips
# Default is to run as production
# If the "notPrd" flag is passed, script will run as testing
if "notPrd" in sys.argv:
    prd = False
else:
    prd = True

# Create nx graph object
sna = nx.Graph()

# Code containing graph data is kept in a separate folder
# Add data to graph here
exec(open("Data/graph_data.py").read())

# Draw interactive graph
# Check if running in production mode otherwise show buttons
interactive_graph(sna, prd)
