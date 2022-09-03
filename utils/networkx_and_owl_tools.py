#convert OWL file into networkx object

#also code to convert networkx object to OWL file

#and code to integrate OWL file with already existing networkx object

#goals of these scripts are to provide tools to be able to allow annotators use protege or webprotege to organize heirarchy of bases that way that heirarchy can then be imported back with python to the networkx represenation of the ontology.


from owlready2 import *
import networkx as nx
import pandas as pd


#function that finds all the is_a parents when given a possible is_a child node and a graph to check (fullbase is_a base ) (child is_a parent)
def get_is_a_parents(single_node, graph):
    to_check = graph.nodes()
    #get is_a parents of the single_node
    #get neighbors
    neighbors = G.neighbors(single_node)
    #check which of these neighbors are is_a relation
    is_a_parent_neighbors = []
    for neighbor in neighbors:
        if G.has_edge(single_node, neighbor, "is_a"):
            is_a_parent_neighbors.append(neighbor)
    return(is_a_parent_neighbors)

#function that fins all the is_a children when given a possible is_A parent node and a graph to check (fullbase is_a base ) (child is_a parent)
def get_is_a_children(single_node, graph):
    #to_check = graph.nodes()
    neighbors = nx.all_neighbors(graph, single_node)
    #check which neighbors are is_a edges
    true_children = []
    for neighbor in neighbors:
        if graph.has_edge(neighbor, single_node, "is_a"):
            true_children.append(neighbor)
    return(true_children)

#add node to ontology
def add_node_to_ontology_with_is_a(node_to_add, is_a_node, ontology, nx_graph):
    #TO DO: check to make sure is_a_node is already in the ontology, else throw an error!
    #if not ontology[is_a_node]:
    #    throw()
    
    #check if node_to_add is already in ontology
    node_if_already_in_ontology = ontology[node_to_add]
    if node_if_already_in_ontology:
        #capture class information already existing and add to it... 
        #if not already in the list!
        parent_nodes = node_if_already_in_ontology.is_a
        if is_a_node not in parent_nodes: 
            parent_nodes.append(is_a_node)
            ontology[node_to_add].is_a = parent_nodes
    else: 
        with ontology:
            if node_to_add != is_a_node:
                new_class = types.new_class(node_to_add, (ontology[is_a_node],))
                #add annotation label as node["string"]
                new_class.label = nx_graph.nodes[node_to_add]['string']

    return(ontology)


    #'1599844502_base' and '1925045096_full_base' cause problem... trying to append '1599844502_base' to list of nodes
    #that are is_a for '1925045096_full_base'

    #add all children of a node (all the subclasses of a node in regards to is_a relations)
def recursive_add_is_a_to_ontology(node, ontology, graph):
    #if no child of the node to add then stop
    children = get_is_a_children(node, graph)
    if not children:
        #stop
        return(ontology)
    else:
        #recursively add children
        for child in children:
            ontology = add_node_to_ontology_with_is_a(child, node, ontology, graph)
            ontology = recursive_add_is_a_to_ontology(child, ontology, graph)
        return(ontology)

    #is this best way to implement the recursion? or is it arms length recursion?





#read in bases and climate change concepts and cause effect information from csv file

standardized_data = pd.read_csv("/Users/kameronr/Documents/personal/climate change outreach/new uploads/NLP data/main_3_per_cluster_outputs/node standardization data processed v1.csv")

standardized_causal_relations_head_and_child_concepts = pd.read_csv("/Users/kameronr/Documents/personal/climate change outreach/new uploads/NLP data/main_3_per_cluster_outputs/standardized_causal_relations_v1.csv")

deduplicated_standardized_causal_relations_concepts_simple = pd.read_csv("/Users/kameronr/Documents/personal/climate change outreach/new uploads/NLP data/main_3_per_cluster_outputs/deduplicated_standardized_causal_relations_climate_concepts_simple_v1.csv")





#make networkx object to fill with bases to organize in protege
#G = nx.DiGraph()
G = nx.MultiDiGraph() #May not be needed and could probably just use DiGraph, but just in case let's use MultiDiGraph so multiple edges can exist between the same 2 nodes. because there could be some 2 nodes that are is_a and cause each other?
#However, you can assign to attributes in e.g. G.edges[1, 2, 0]. Thus, use 2 sets of brackets to add/change data attributes: G.edges[1, 2, 0]['weight'] = 4 (for multigraphs the edge key is required: MG.edges[u, v, key][name] = value).
#otherwise if want to use DiGraph then just have to have multiple sets of attributes possible on edges so that multiple types of edges can overlap in attributes using the same edge that's identified by the 2 nodes
#https://wikidiff.com/digraph/multidigraph
#https://en.wikipedia.org/wiki/Multigraph


#edge ids
# is_a = 0
# hasBase=1
# hasChangeDirection=2
# hasAspectChanging=3
# contributesTo = 4


#fill the networkx object with the appropriate information from deduplicated_standardized_causal_relations_concepts_simple

#there should be a separate class node for each climate change concept
#for each climate change concept, there should be separate class node's for its assoicated type_of+base, change_direction, aspect_changing (might even need to assign unique identifiers for new ones not yet seen or have an id yet... do this by assigning the concept id to be included as a piece of the identifier for the base, aspect_changing, change_direction, etc.)
#to read more info on how networkx nodes and edges are organized, see: https://miro.com/app/board/o9J_lacVyGQ=/?share_link_id=716458085593

#for each row in the table, parse the information into the networkx object

#the evidence for existence of entities and relations should be appended also (and if multiple evidences/sources then multiple should be added too)... this can be done later by joining the concepts to the original csv file ('standardized_causal_relations_head_and_child_concepts')

increase_id = "1"
decrease_id = "2"

deduplicated_standardized_causal_relations_concepts_simple = deduplicated_standardized_causal_relations_concepts_simple.reset_index()

for index, row in deduplicated_standardized_causal_relations_concepts_simple.iterrows():

    head_concept_id = str(int(row['climate_concept_id_HEAD_CLIMATE_CONCEPT']))
    head_concept_string = row['climate_concept_string_representation_HEAD_CLIMATE_CONCEPT']
    
    head_base = row['base (standardized v1)_HEAD_CLIMATE_CONCEPT']
    head_base_id = head_concept_id+"_base"
    
    head_type_of = row['type_of (standardized v1)_HEAD_CLIMATE_CONCEPT']
    head_type_of_id = head_concept_id+"_type_of"

    #convert type_of+base to full_base for networkx object
    if head_type_of == '[]' or not head_type_of:
        head_full_base = head_base
        head_full_base_id = head_base_id
        # breakpoint()
    else:
        head_full_base = head_type_of+"_"+head_base
        head_full_base_id = head_concept_id+"_full_base"
    
    head_change_direction = row['change_direction (standardized v1)_HEAD_CLIMATE_CONCEPT'] 
    if head_change_direction == "increase":
        head_change_direction_id = increase_id
    if head_change_direction == "decrease":
        head_change_direction_id = decrease_id
    #else throw an error (TO DO)
    #head_change_direction_id = head_concept_id+"_change_direction" #change_direction shouldn't have an id because there should only be either up or down if the data has already been standardized
    
    head_aspect_changing = row['aspect_changing (standardized v1)_HEAD_CLIMATE_CONCEPT']
    head_aspect_changing_id = head_concept_id+"_aspect_changing"


    relation_type = row['relation_type']


    child_concept_id = str(int(row['climate_concept_id_CHILD_CLIMATE_CONCEPT']))
    child_concept_string = row['climate_concept_string_representation_CHILD_CLIMATE_CONCEPT']
    
    child_base = row['base (standardized v1)_CHILD_CLIMATE_CONCEPT']
    child_base_id = child_concept_id+"_base"
    
    child_type_of = row['type_of (standardized v1)_CHILD_CLIMATE_CONCEPT']
    child_type_of_id = child_concept_id+"_type_of"
    
    if child_type_of == '[]' or not child_type_of:
        child_full_base = child_base
        child_full_base_id = child_base_id
    else:
        child_full_base = child_type_of+"_"+child_base
        child_full_base_id = child_concept_id+"_full_base"
    
    child_change_direction = row['change_direction (standardized v1)_CHILD_CLIMATE_CONCEPT'] 
    if child_change_direction == "increase":
        child_change_direction_id = increase_id
    if child_change_direction == "decrease":
        child_change_direction_id = decrease_id
    #child_change_direction_id = child_concept_id+"_change_direction" #change_direction shouldn't have an id because there should only be either up or down if the data has already been standardized
    
    child_aspect_changing = row['aspect_changing (standardized v1)_CHILD_CLIMATE_CONCEPT'] 
    child_aspect_changing_id = child_concept_id+"_aspect_changing"


    #add in source for the relationship
    # standardized_data.loc[standardized_data['climate_concept_id'] == head_concept_id]
    # standardized_data.loc[standardized_data['climate_concept_id'] == child_concept_id]
    # standardized_causal_relations_head_and_child_concepts.loc[standardized_causal_relations_head_and_child_concepts['climate_concept_id'] == head_concept_id]
    # standardized_causal_relations_head_and_child_concepts.loc[standardized_causal_relations_head_and_child_concepts['climate_concept_id_CHILD_CLIMATE_CONCEPT'] == child_concept_id]
    source_row = standardized_causal_relations_head_and_child_concepts.loc[ (standardized_causal_relations_head_and_child_concepts['climate_concept_id'] == float(head_concept_id)) & (standardized_causal_relations_head_and_child_concepts['climate_concept_id_CHILD_CLIMATE_CONCEPT'] == float(child_concept_id)) ]
    original_text = source_row['original_text'].tolist()[0]
    sentence_source = source_row['source'].tolist()[0]
    document_id = source_row['document_id'].tolist()[0]
    sentence_id = source_row['sentence_id'].tolist()[0]


    source_dict = {"original_text":original_text, "sentence_source_url":sentence_source, "document_id":document_id, "sentence_id":sentence_id}


    #make networkx nodes and then connect them up appropriately
    # breakpoint()

    #be sure to realize that some entities may be blank! so don't try using their ids if the assoicated value is NULL!


    #add head concept
    #but before do so check make sure it's not already represented (shouildn't be because all concepts have been deduplicated)
    existing_concept_id = [n for n in G if G.nodes[n]["string"] == head_concept_string]
    if not existing_concept_id:
        G.add_node(head_concept_id, string=head_concept_string, class_type="climate_concept")#, original_text=[original_text], sentence_source=sentence_source, document_id=document_id, sentence_id=sentence_id)
    else:
        head_concept_id = existing_concept_id[0]

    #add head concept components as nodes
    #there should always be a base, change_direction, and aspect_changing (if not then should throw an error [TO DO])
    
    #check that no node already exists with the head_base... if it does, then use that one instead! (no need to append another identifier to it... really just want single id per node)
    existing_base_id = [n for n in G if G.nodes[n]["string"] == head_base]
    if not existing_base_id:
        G.add_node(head_base_id, string=head_base, class_type="base")#, original_text=original_text, sentence_source=sentence_source, document_id=document_id, sentence_id=sentence_id)
        # breakpoint()
    else:
        head_base_id = existing_base_id[0]

    existing_full_base_id = [n for n in G if G.nodes[n]["string"] == head_full_base]
    if not existing_full_base_id:
        G.add_node(head_full_base_id, string=head_full_base, class_type="base")#, original_text=original_text, sentence_source=sentence_source, document_id=document_id, sentence_id=sentence_id)
        # breakpoint()
    else:
        head_full_base_id = existing_full_base_id[0]


    existing_change_direction_id = [n for n in G if G.nodes[n]["string"] == head_change_direction]
    if not existing_change_direction_id:
        G.add_node(head_change_direction_id, string=head_change_direction, class_type="change_direction")#, original_text=original_text, sentence_source=sentence_source, document_id=document_id, sentence_id=sentence_id)
        # breakpoint()
    else:
        head_change_direction_id = existing_change_direction_id[0]


    existing_aspect_changing_id = [n for n in G if G.nodes[n]["string"] == head_aspect_changing]
    if not existing_aspect_changing_id:
        G.add_node(head_aspect_changing_id, string=head_aspect_changing, class_type="aspect_changing")#, original_text=original_text, sentence_source=sentence_source, document_id=document_id, sentence_id=sentence_id)
        # breakpoint()
    else:
        head_aspect_changing_id = existing_aspect_changing_id[0]






    #add is_a relation: base is_a full_base (if they are not the same!) (AND if does not already exist!)
    if head_full_base != head_base:
        #if (head_base_id, head_full_base_id, "is_a") not in G.edges:
        #if "sources" not in G.edges[head_base_id, head_full_base_id, "is_a"]:
        #if not G.edges[head_base_id, head_full_base_id, "is_a"]
        if not G.has_edge(head_base_id, head_full_base_id, "is_a"):

            #should have "sources" in the edge attributes if the edge exists! but TO DO to throw error if not "sources" in the edge? It could be that annotators add is_a info into the KB without sources for it (common sense is the source!)
        #G.edges[head_base_id,head_full_base_id,"is_a"]
            #G.add_edge(head_base_id, head_full_base_id, "is_a", original_text=[original_text], sentence_source=[sentence_source], document_id_sentence_id=[(document_id, sentence_id)]) #is this structure the best?
           G.add_edge(head_full_base_id, head_base_id, "is_a", sources=[source_dict]) #is this structure the best? Yes.
            # breakpoint()
        else:
            #add to it!
            sources_list = G.edges[head_base_id, head_full_base_id, "is_a"]["sources"] #https://networkx.org/documentation/stable/reference/classes/multidigraph.html
            if sources_list:
                # new_sources_list = sources_list.append(source_dict)
                sources_list.append(source_dict)
            else:            
                G.add_edge(head_base_id, head_full_base_id, "is_a", sources=[source_dict])
            # breakpoint()




    #it's the edges that should store all the source information!
    #if node already exists, then use it instead of adding new one!
    #if edge already exists, then add to the edge attribute instead of making a new edge!! 


    #add other entity edges: hasBase, hasChangeDirection, hasAspectChanging... can do all at once https://networkx.org/documentation/stable/reference/classes/generated/ BUT shouldn't because need to check first if the edge already exists, and if it does already exist then need to append the source to its sources list instead of making new blank edge! networkx.MultiDiGraph.add_edges_from.html#networkx.MultiDiGraph.add_edges_from
    #G.add_edges_from([(head_concept_id, head_full_base_id, "hasBase"), (head_concept_id, head_change_direction_id, "hasChangeDirection"), (head_concept_id, head_aspect_changing_id, "hasAspectChanging")], original_text=original_text, sentence_source=sentence_source, document_id=document_id, sentence_id=sentence_id)


    if not G.has_edge(head_concept_id, head_full_base_id, "hasBase"):
    #if not G.edges[head_concept_id, head_full_base_id, "hasBase"]:
        G.add_edge(head_concept_id, head_full_base_id, "hasBase", sources=[source_dict]) 
    else:
        sources_list = [G.edges[head_concept_id, head_full_base_id, "hasBase"]["sources"]] #https://networkx.org/documentation/stable/reference/classes/multidigraph.html
        if sources_list:
            sources_list.append(source_dict)
        else:
            G.add_edge(head_concept_id, head_full_base_id, "hasBase", sources=[source_dict])


    if not G.has_edge(head_concept_id, head_change_direction_id, "hasChangeDirection"):
    #if not G.edges[head_concept_id, head_full_base_id, "hasBase"]:
        G.add_edge(head_concept_id, head_change_direction_id, "hasChangeDirection", sources=[source_dict]) 
    else:
        sources_list = G.edges[head_concept_id, head_change_direction_id, "hasChangeDirection"]["sources"] #https://networkx.org/documentation/stable/reference/classes/multidigraph.html
        if sources_list:
            sources_list.append(source_dict)
        else:
            G.add_edge(head_concept_id, head_change_direction_id, "hasChangeDirection", sources=[source_dict])


    if not G.has_edge(head_concept_id, head_aspect_changing_id, "hasAspectChanging"):
    #if not G.edges[head_concept_id, head_full_base_id, "hasBase"]:
        G.add_edge(head_concept_id, head_aspect_changing_id, "hasAspectChanging", sources=[source_dict]) 
    else:
        sources_list = G.edges[head_concept_id, head_aspect_changing_id, "hasAspectChanging"]["sources"] #https://networkx.org/documentation/stable/reference/classes/multidigraph.html
        if sources_list:
            sources_list.append(source_dict)
        else:
            G.add_edge(head_concept_id, head_aspect_changing_id, "hasAspectChanging", sources=[source_dict])





    #add child concept

#add child concept
    #but before do so check make sure it's not already represented (shouildn't be because all concepts have been deduplicated)
    existing_concept_id = [n for n in G if G.nodes[n]["string"] == child_concept_string]
    if not existing_concept_id:
        G.add_node(child_concept_id, string=child_concept_string, class_type="climate_concept")#, original_text=[original_text], sentence_source=sentence_source, document_id=document_id, sentence_id=sentence_id)
    else:
        child_concept_id = existing_concept_id[0]

    #add child concept components as nodes
    #there should always be a base, change_direction, and aspect_changing (if not then should throw an error [TO DO])
    
    #check that no node already exists with the child_base... if it does, then use that one instead! (no need to append another identifier to it... really just want single id per node)
    existing_base_id = [n for n in G if G.nodes[n]["string"] == child_base]
    if not existing_base_id:
        G.add_node(child_base_id, string=child_base, class_type="base")#, original_text=original_text, sentence_source=sentence_source, document_id=document_id, sentence_id=sentence_id)
        # breakpoint()
    else:
        child_base_id = existing_base_id[0]

    existing_full_base_id = [n for n in G if G.nodes[n]["string"] == child_full_base]
    if not existing_full_base_id:
        G.add_node(child_full_base_id, string=child_full_base, class_type="base")#, original_text=original_text, sentence_source=sentence_source, document_id=document_id, sentence_id=sentence_id)
        # breakpoint()
    else:
        child_full_base_id = existing_full_base_id[0]


    existing_change_direction_id = [n for n in G if G.nodes[n]["string"] == child_change_direction]
    if not existing_change_direction_id:
        G.add_node(child_change_direction_id, string=child_change_direction, class_type="change_direction")#, original_text=original_text, sentence_source=sentence_source, document_id=document_id, sentence_id=sentence_id)
        # breakpoint()
    else:
        child_change_direction_id = existing_change_direction_id[0]


    existing_aspect_changing_id = [n for n in G if G.nodes[n]["string"] == child_aspect_changing]
    if not existing_aspect_changing_id:
        G.add_node(child_aspect_changing_id, string=child_aspect_changing, class_type="aspect_changing")#, original_text=original_text, sentence_source=sentence_source, document_id=document_id, sentence_id=sentence_id)
        # breakpoint()
    else:
        child_aspect_changing_id = existing_aspect_changing_id[0]





    #add is_a relation: base is_a full_base (if they are not the same!) (AND if does not already exist!)
    if child_full_base != child_base:
        #if (child_base_id, child_full_base_id, "is_a") not in G.edges:
        #if "sources" not in G.edges[child_base_id, child_full_base_id, "is_a"]:
        #if not G.edges[child_base_id, child_full_base_id, "is_a"]
        if not G.has_edge(child_base_id, child_full_base_id, "is_a"):

            #should have "sources" in the edge attributes if the edge exists! but TO DO to throw error if not "sources" in the edge? It could be that annotators add is_a info into the KB without sources for it (common sense is the source!)
        #G.edges[child_base_id,child_full_base_id,"is_a"]
            #G.add_edge(child_base_id, child_full_base_id, "is_a", original_text=[original_text], sentence_source=[sentence_source], document_id_sentence_id=[(document_id, sentence_id)]) #is this structure the best?
           G.add_edge(child_full_base_id, child_base_id, "is_a", sources=[source_dict]) #is this structure the best? Yes.
            # breakpoint()
        else:
            #add to it!
            sources_list = G.edges[child_base_id, child_full_base_id, "is_a"]["sources"] #https://networkx.org/documentation/stable/reference/classes/multidigraph.html
            if sources_list:
                sources_list.append(source_dict)
            else:
                G.add_edge(child_base_id, child_full_base_id, "is_a", sources=[source_dict])
            # breakpoint()




    #it's the edges that should store all the source information!
    #if node already exists, then use it instead of adding new one!
    #if edge already exists, then add to the edge attribute instead of making a new edge!! 


    #add other entity edges: hasBase, hasChangeDirection, hasAspectChanging... can do all at once https://networkx.org/documentation/stable/reference/classes/generated/ BUT shouldn't because need to check first if the edge already exists, and if it does already exist then need to append the source to its sources list instead of making new blank edge! networkx.MultiDiGraph.add_edges_from.html#networkx.MultiDiGraph.add_edges_from
    #G.add_edges_from([(child_concept_id, child_full_base_id, "hasBase"), (child_concept_id, child_change_direction_id, "hasChangeDirection"), (child_concept_id, child_aspect_changing_id, "hasAspectChanging")], original_text=original_text, sentence_source=sentence_source, document_id=document_id, sentence_id=sentence_id)
    
    source_dict = {"original_text":original_text, "sentence_source_url":sentence_source, "document_id":document_id, "sentence_id":sentence_id}

    if not G.has_edge(child_concept_id, child_full_base_id, "hasBase"):
    #if not G.edges[child_concept_id, child_full_base_id, "hasBase"]:
        G.add_edge(child_concept_id, child_full_base_id, "hasBase", sources=[source_dict]) 
    else:
        sources_list = G.edges[child_concept_id, child_full_base_id, "hasBase"]["sources"] #https://networkx.org/documentation/stable/reference/classes/multidigraph.html
        if sources_list:
            sources_list.append(source_dict)
        else:
            G.add_edge(child_concept_id, child_full_base_id, "hasBase", sources=[source_dict])


    if not G.has_edge(child_concept_id, child_change_direction_id, "hasChangeDirection"):
    #if not G.edges[child_concept_id, child_full_base_id, "hasBase"]:
        G.add_edge(child_concept_id, child_change_direction_id, "hasChangeDirection", sources=[source_dict]) 
    else:
        sources_list = G.edges[child_concept_id, child_change_direction_id, "hasChangeDirection"]["sources"] #https://networkx.org/documentation/stable/reference/classes/multidigraph.html
        if sources_list:
            sources_list.append(source_dict)
        else:
            G.add_edge(child_concept_id, child_change_direction_id, "hasChangeDirection", sources=[source_dict])


    if not G.has_edge(child_concept_id, child_aspect_changing_id, "hasAspectChanging"):
    #if not G.edges[child_concept_id, child_full_base_id, "hasBase"]:
        G.add_edge(child_concept_id, child_aspect_changing_id, "hasAspectChanging", sources=[source_dict]) 
    else:
        sources_list = G.edges[child_concept_id, child_aspect_changing_id, "hasAspectChanging"]["sources"] #https://networkx.org/documentation/stable/reference/classes/multidigraph.html
        if sources_list:
            sources_list.append(source_dict)
        else:
            G.add_edge(child_concept_id, child_aspect_changing_id, "hasAspectChanging", sources=[source_dict])



# add contributesTo relation
    if relation_type == "Contributes_To":
        relation_type = "contributesTo"
    if not G.has_edge(head_concept_id, child_concept_id, relation_type):
    #if not G.edges[child_concept_id, child_full_base_id, "hasBase"]:
        G.add_edge(head_concept_id, child_concept_id, relation_type, sources=[source_dict]) 
    else:
        sources_list = G.edges[head_concept_id, child_concept_id, relation_type]["sources"] #https://networkx.org/documentation/stable/reference/classes/multidigraph.html
        if sources_list:
            sources_list.append(source_dict)
        else:
            G.add_edge(head_concept_id, child_concept_id, relation_type, sources=[source_dict])




# breakpoint()


import matplotlib.pyplot as plt
# nx.draw(G)

# plt.savefig("/Users/kameronr/Documents/personal/climate change outreach/new uploads/networkx_graph_ontology.png")

# plt.show()


#draw just the is_a edges of bases
#https://networkx.org/documentation/stable/reference/drawing.html
edges_to_draw = [edge for edge in G.edges if edge[2]=="is_a"]
# edges_to_draw = []
# for edge in G.edges:
#     breakpoint()

subgraph_to_draw = G.edge_subgraph(edges_to_draw)

# nx.draw(subgraph_to_draw)

#plt.savefig("/Users/kameronr/Documents/personal/climate change outreach/new uploads/networkx_graph_ontology.png")

# plt.show()




#load owl/rdf/turtle file
ontology_path = "/Users/kameronr/Documents/personal/climate change outreach/new uploads/NLP ontology with entities_corrected5.owl"

#onto = get_ontology(ontology_path)
experimental_onto = get_ontology(ontology_path).load()

onto = get_ontology("Climate_Mind_ontology")






import types


#build up the blank owl object to include the bases from the networkx object (have the networkx nodes be classes iin the owl object)
#add bases first...?
#then add the full bases...?

#use annotation 'label' to add in the string for each class.  https://owlready2.readthedocs.io/en/latest/annotations.html

#find all the nodes to be classes that don't have any (the top level) and keep track of nodes already done
#add all networkx nodes that don't have any is_a children
#for each node in networkx graph add to list if do not have is_a edge relation with another node.
#only search the base nodes for now
top_level_classes = []
for node in G.nodes:
    #if it has no is_a relations 
    is_a_parents = get_is_a_parents(node, G) 
    if not is_a_parents:
        #if it's a base
        if G.nodes[node]['class_type']=="base":
            top_level_classes.append(node)


#add top_level_classes to owl object
for node in top_level_classes:
    with onto:
        new_class = types.new_class(node, (Thing,))
        #add annotation label as node["string"]
        new_class.label = G.nodes[node]['string']

        #if the node has child, add them... and when adding each one, first check it doesn't exist then add it. if it does exist be sure to add it again and extend it's is_a relations to include the old and the new!
        onto = recursive_add_is_a_to_ontology(node, onto, G)
        pass


#export the ontology as an .owl file to import into Protege.
# onto.save(file = "/Users/kameronr/Documents/personal/climate change outreach/new uploads/NLP_ontology_standardized_bases_only.rdfxml", format = "rdfxml")



#if I run this script 3 times in a row I get a weird error about '1599844502_base' [climate change] not being a Class (so it fails because it's a subclass and not a class so can't get added to '1925045096_full_base' [human-caused_climate_change])... suggests need more error catching and if then else statements to avoid redoing work already done... and if doing work already done then it should catch itself and skip that work


#problem with '1599844502_base' and 'Thing'
#     neighbors=nx.neighbors(G, node)

#list(onto.classes())


#TO DO:
#add in all the other ontology information into the owl object

#TO DO:
#load in the modified base heirarchy file and then process it and integrate the information into the old networkx object to form a new updated improved networkx object
#for a new networkx object with cause_effect relations propagated (inherited) by parent nodes.



#read in the modified owl file and integrate the changes (both removal and addition) in the is_a relations to the networkx object.
updated_ontology_path = "/Users/kameronr/Documents/personal/climate change outreach/new uploads/Climate_Mind_ontology_updated.owl"
updated_onto = get_ontology(updated_ontology_path).load()

#For all the nodes in the networkx object that are represented in the updated_onto, strip away all the is_a relations that are shared between the node and any other node that corresponds to any class in the updated_onto.
#then, add in all the is_a relations from the updated_onto to the networkx object

for node_name in G.nodes:
    if updated_onto[node_name]:
        #remove all is_a relations to any nodes corresponding to any class in updated_onto
         for parent_node_name in get_is_a_parents(node_name, G):
            #if child_node present as a class in updated_onto, then remove this is_a relation from the networkx object
            if updated_onto[parent_node_name] and parent_node_name != 'Thing':
                #delete this node_name is_a parent_name relation from the networkx graph (what about the sources for is_a relation if there were any?!? they would get lost later if the is_a relation is added back to the networkx graph through the owl object?)
                G.remove_edge(node_name, parent_node_name, key='is_a')

#for each class in updated_onto, add it's is_a relations to the networkx graph
for class_obj in updated_onto.classes():
    #short_class_name = class_name.name
    #get is_a relations
    parents_classes = class_obj.is_a
    for parent_class in parents_classes:
        if parent_class.name != 'Thing':
            #then add it to the networkx graph (what about adding the sources for the is_a relation if there are any?)
            G.add_edge(class_obj.name, parent_class.name, "is_a")
            #for any new nodes added to networkx object from the ontology that were manually added to the ontology and added to networkx object through is_a relations, add their string field to the networkx object
            #ex: node for viruses is 'RCcf2ZkKWMy4D623Qj6RY0e' in networkx object and it came from being manually added to the ontology using Protege
            #updated_onto.search(iri="*RCcf2ZkKWMy4D623Qj6RY0e")[0].label
            if not "string" in G.nodes[class_obj.name]:
                #add it
                G.nodes[class_obj.name]['string'] = class_obj.label
                G.nodes[class_obj.name]['class_type'] = 'base'
            if not "string" in  G.nodes[parent_class.name]:
                #add it
                G.nodes[parent_class.name]['string'] = parent_class.label
                G.nodes[parent_class.name]['class_type'] = 'base'




#propagate/project the cause_effect relations from child to parent nodes (project all the climate change concepts upwards (in the abstract generalizing direction) then only task left if just need to consolidate/resolve/decide/merge equivalent climate change concepts in the graph/heirarchy)
#many concepts should project into semantically equivalent (but rather abstract) concept (or it could become chaos or possibly even misinformation?)
#only really want to leverage how the propagation/projection/inference/reasoning result in cause-effect chains that are valuable and non redundant (those cause effect relationship chains that connect global warming concept to concepts associated with personal values... they need to originate with being caused by global warming though!

#for every child base of a climate change concept with cause_effect relationships, add those cause_effect relationships to the is_a of that base. Do this recursively and iteratively until there's no more left to add?
def get_edges_to_add(graph):
    edges_to_add=[]
    #make sure only to query the base nodes! (for example, not aspect_changing or climate concept nodes, etc). query 'class_type': 'base' only
    for node in list(graph.nodes()):
        #TO DO: if node is 'Thing' throw an error


        if 'class_type' in graph.nodes[node] and 'base' in graph.nodes[node]['class_type']:
            #some nodes won't have any causal relations! because they are base nodes
            #only the climate concepts would have the cause_effect relationship, so go to the associated climate concept for the base
            
            is_a_parents = get_is_a_parents(node, graph)
            if is_a_parents:

                #get climate concepts
                #just for the parent of the node? or climate concepts of the child node?
                neighbors = nx.all_neighbors(graph, node)
                potential_causal_climate_concepts = []
                for neighbor in neighbors:
                    #if neighbor is a climate_concept, add it to climate_concept list because a base node can be the base for many different climate concepts!
                    if graph.has_edge(neighbor, node, "hasBase"):
                        potential_causal_climate_concepts.append(neighbor) #this isn't guarenteed to have cause-effect relationship so have to check later.
                        #now create a new concept by following iteratively/recursively the is_a to next base and associate the child_change_direction and child_aspect_changing and is_a_base to that new concept and make it is_a to the child_concept ?
                        #recursively? not sure if recursion is needed here.
                        #for each parent base by is_a make new cause concept for parent if doesn't yet exist.
                        for parent in is_a_parents:
                            #TO DO: if parent is 'Thing' throw an error

                            #check if new cause concept exists, if not, make one (this will make new concepts some that never have cause_effect relations, that's ok)
                            new_concept = make_new_concept(neighbor, node, parent, graph)
                            
                            surrounding_concepts = nx.all_neighbors(graph, neighbor)
                            cause_concept_neighbors = [node for node in surrounding_concepts if graph.has_edge(node, neighbor, "contributesTo")]
                            effect_concept_neighbors = [node for node in surrounding_concepts if graph.has_edge(neighbor, node, "contributesTo")]
                            #graph.has_edge(list(nx.all_neighbors(graph, neighbor))[0], neighbor, "contributesTo")
                            #iteratively add to list of edges the new contributesTo relations to add to this new concept (include source information to add to it too!)
                            #get the effect_concepts for the neighbor concept (if any cause effect relations exist!)
                            #get outgoing contributesTo edges from the concept
                            #effect_edges = [edge for edge in graph.edges(neighbor, keys=True) if edge[2]=='contributesTo'] #or if any other concept contributesTo it?
                            #get incoming contributesTo edge into the concept

                            #propagate the appropriate contributesTo relations out from the new concept node
                            for effect_concept_neighbor in effect_concept_neighbors:
                                causal_concept = neighbor
                                effect_concept = effect_concept_neighbor
                                new_causal_concept = new_concept
                                #TO DO: if 'sources' not in the contributesTo relation, then throw an error!
                                edge_source_list_of_dictionaries = graph.get_edge_data(causal_concept, effect_concept)['contributesTo']['sources']
                                #should only be adding the new edge if it doesnt' exist yet! and if it does exist, only adding the source if the source is missing. checking needs to happen before it gets added to the edges_to_add list so that the function can terminate eventually.
                                if not graph.has_edge(new_causal_concept, effect_concept, "contributesTo"):
                                    edges_to_add.append((new_causal_concept, effect_concept, edge_source_list_of_dictionaries))  
                                else:
                                    current_sources = graph.get_edge_data(new_causal_concept, effect_concept)['contributesTo']['sources']
                                    missing_sources = []
                                    for source in edge_source_list_of_dictionaries:
                                        if not source in current_sources:
                                            missing_sources.append(source)
                                    if missing_sources:
                                        edges_to_add.append((new_causal_concept, effect_concept, missing_sources))

                            #propagate the appropriate contributeTo relations into the new concept node
                            for cause_concept_neighbor in cause_concept_neighbors:
                                causal_concept = cause_concept_neighbor
                                effect_concept = neighbor
                                new_effect_concept = new_concept
                                edge_source_list_of_dictionaries = graph.get_edge_data(causal_concept, effect_concept)['contributesTo']['sources']
                                #should only be adding the new edge if it doesnt' exist yet! and if it does exist, only adding the source if the source is missing. checking needs to happen before it gets added to the edges_to_add list so that the function can terminate eventually.
                                if not graph.has_edge(causal_concept, new_effect_concept, "contributesTo"):
                                    edges_to_add.append((causal_concept, new_effect_concept, edge_source_list_of_dictionaries))  
                                else:
                                    current_sources = graph.get_edge_data(causal_concept, new_effect_concept)['contributesTo']['sources']
                                    missing_sources = []
                                    for source in edge_source_list_of_dictionaries:
                                        #if missing any sources then add the edge source list so that the missing sources get added later
                                        if not source in current_sources:
                                            missing_sources.append(source)
                                    if missing_sources:
                                        edges_to_add.append((causal_concept, new_effect_concept, missing_sources))

                        #if edge not yet present in graph:
                            #add to graph (parent, effect) edges + sources to edges_to_add
    return edges_to_add

def make_new_concept(child_climate_concept_id, child_base_id, parent_base_id, graph):
    #check first to ensure the new_concept node has not already been created (because if so then should confirm nothing is different and if so then raise an error?...TO DO?)

    #should only have single change direction and single aspect changing! TO DO: if not, throw error!
    child_change_direction_id = [(i, j, k)   for i, j, k in graph.edges(child_climate_concept_id, keys=True) if k == 'hasChangeDirection'][0][1]
    child_aspect_changing_id = [(i, j, k)   for i, j, k in graph.edges(child_climate_concept_id, keys=True) if k == 'hasAspectChanging'][0][1]
    new_concept_id = str(child_change_direction_id) + "_" + str(parent_base_id) + "_" + str(child_aspect_changing_id) #this will be the iri

    #check to see if any node in graph that hasBase parent_base_id, hasChangeDirection child_change_direction_id, hasAspectChanging child_aspect_changing_id . This is expected to be rare, but is possible!
    other_new_concept_id = [node for node in graph.nodes if graph.has_edge(node, parent_base_id, "hasBase") and graph.has_edge(node, child_change_direction_id, "hasChangeDirection") and graph.has_edge(node, child_aspect_changing_id, "hasAspectChanging")] 
    if other_new_concept_id:
        new_concept_id = other_new_concept_id[0]
    #do this by creating concept node id from the appropriate change_direction, base, and aspect_changing ids to ensure unique id and not creating a new one if already exist
    if new_concept_id not in graph.nodes():
        #then concept is not yet made and needs to be made
        #needs to form concept node with unique (but reproducibly unique!) node iri, with a 'string' and 'class_type' field and value.
        child_change_direction_string = graph.nodes[child_change_direction_id]['string']
        parent_base_string = graph.nodes[parent_base_id]['string']
        child_aspect_changing_string = graph.nodes[child_aspect_changing_id]['string']
        #TO DO: if not 'string' in graph.nodes[child_change_direction_id] or graph.nodes[parent_base_id] or graph.nodes[child_aspect_changing_id] then throw an error!

        new_concept_string = str(child_change_direction_string) + "_" + str(parent_base_string) + "_" + child_aspect_changing_string
        graph.add_node(new_concept_id, string=new_concept_string, class_type="climate_concept")
        
        #needs new_concept_id 'hasBase' parent_base
        source_dictionary = graph.get_edge_data(child_climate_concept_id, child_base_id)['hasBase']['sources']
        graph.add_edge(new_concept_id, parent_base_id, "hasBase", sources=source_dictionary)
        #needs new_concept_id 'hasAspectChanging' parent_aspect_changing
        source_dictionary = graph.get_edge_data(child_climate_concept_id, child_change_direction_id)['hasChangeDirection']['sources']
        graph.add_edge(new_concept_id, child_change_direction_id, "hasChangeDirection", sources=source_dictionary)
        #needs new_concept_id 'hasChangeDirection' parent_change_direction
        source_dictionary = graph.get_edge_data(child_climate_concept_id, child_aspect_changing_id)['hasAspectChanging']['sources']
        graph.add_edge(new_concept_id, child_aspect_changing_id, "hasAspectChanging", sources=source_dictionary)

        #should the new concept have the word 'some' in it to be clearer that it's not the universal base that is changing, rather just some part of the universal base? Not for now.
    else:
        #what if they edge already exists, then should possible more sources be added for hasBase, hasChangeDirection, and hasAspectChanging ??? YES!
        #add sources for hasBase, hasChangeDirection, and hasAspectChanging
        #call add_source to add sources for hasBase, hasChangeDirection, and hasAspectChanging
        graph = add_source(new_concept_id, parent_base_id, "hasBase", child_climate_concept_id, child_base_id, graph)
        graph = add_source(new_concept_id, child_change_direction_id, "hasChangeDirection", child_climate_concept_id, child_change_direction_id, graph)
        graph = add_source(new_concept_id, child_aspect_changing_id, "hasAspectChanging", child_climate_concept_id, child_aspect_changing_id, graph)

        #TO DO: if the edge does not exist child_base_id is_a parent_base_id, then throw an error!
    if 'sources' in graph.get_edge_data(child_base_id, parent_base_id)['is_a']:
        is_a_source_dictionary = graph.get_edge_data(child_base_id, parent_base_id)['is_a']['sources']
    else:
        is_a_source_dictionary = []
    #if not yet exist the relation child_climate_concept_id is_a new_concept_id, then add it and try to also include sources if there are any
    if not graph.has_edge(child_climate_concept_id, new_concept_id, "is_a"):
        graph.add_edge(child_climate_concept_id, new_concept_id, "is_a", sources=is_a_source_dictionary)
    else:
        #try to add source to it
        new_concept_is_a_edge_data = graph.get_edge_data(child_climate_concept_id, new_concept_id)['is_a']
        if 'sources' in new_concept_is_a_edge_data:
            current_sources_is_a = new_concept_is_a_edge_data['sources']
            #add source
            missing_sources = []
            for source in is_a_source_dictionary:
                if source not in current_sources_is_a:
                    missing_sources.append(source)
            if missing_sources:
                new_is_a_source_dictionary = current_sources_is_a+missing_sources
            else:
                new_is_a_source_dictionary = current_sources_is_a

            graph[child_climate_concept_id][new_concept_id]["is_a"]['sources']=new_is_a_source_dictionary
            #could have used extend instead but was unsure if it would work as needed
        else:
            #add new source field 
            graph[child_climate_concept_id][new_concept_id]["is_a"]['sources']=is_a_source_dictionary

    #if it is in the graph then need to try to add the is_a source for the child_base_id is_a parent_base_id to the child_climate_concept_id is_a parent_climate_concept_id relation.
    #needs the relationship child_climate_concept 'is_a' new_concept (source not needed for the is_a relationship? or optional? probably best to exclude for now?)

    return new_concept_id

#for use only when know that the relation exists already between target_nodeA and target_nodeB, but just want to add sources to it and ensure all is added from some reference relation sources
def add_source(target_nodeA, target_nodeB, relation_type, reference_nodeA, reference_nodeB, graph):
    #assumed edge is in graph between the reference nodes, TO DO: throw error if no edge between reference_nodeA and reference_nodeB
    if 'sources' in graph.get_edge_data(reference_nodeA, reference_nodeB)[relation_type]:
        reference_source_dictionary = graph.get_edge_data(reference_nodeA, reference_nodeB)[relation_type]['sources']
    else:
        reference_source_dictionary = []
    #if not yet exist the relation child_climate_concept_id is_a new_concept_id, then add it and try to also include sources if there are any
    # if not graph.has_edge(target_nodeA, target_nodeB, relation_type):
        # graph.add_edge(target_nodeA, new_concept_id, "is_a", sources=source_dictionary)
    # else:
    #try to add source to it
    target_edge_data = graph.get_edge_data(target_nodeA, target_nodeB)[relation_type]
    if 'sources' in target_edge_data:
        current_sources = target_edge_data['sources']
        #add source
        missing_sources = []
        for source in reference_source_dictionary:
            if source not in current_sources:
                missing_sources.append(source)
        if missing_sources:
            new_source_dictionary = current_sources+missing_sources
        else:
            new_source_dictionary = current_sources

        graph[target_nodeA][target_nodeB][relation_type]['sources']=new_source_dictionary
        #could have used extend instead but was unsure if it would work as needed
    else:
        #add new source field 
        graph[target_nodeA][target_nodeB][relation_type]['sources']=reference_source_dictionary

    return(graph)

def populate_edges(graph):
    new_edges = get_edges_to_add(graph)
    if not new_edges:
        return graph
    else:
        for edge in new_edges:
            cause_concept = edge[0]
            effect_concept = edge[1]
            edge_key = "contributesTo"
            missing_edge_sources = edge[2]
            #add edge and source to graph
            
            #when adding an edge, be sure to check if it already exists first! And if it does already exist, then add to its source dictionary instead of creating a new one.
            if (cause_concept, effect_concept) not in graph.edges():
                graph.add_edge(cause_concept, effect_concept, edge_key, sources=[missing_edge_sources])
            else:
                #add to that already existing edge's source dictionary the new source information (may need to also check that this source information hasn't yet already been added too!?)
                #try to add source to it
                contributes_to_edge_data = graph.get_edge_data(cause_concept, effect_concept)[edge_key]
                if 'sources' in contributes_to_edge_data:
                    current_sources_contributes_to = contributes_to_edge_data['sources']
                    #add source
                    true_missing_sources = []
                    for source in missing_edge_sources:
                        if source not in current_sources_contributes_to:
                            true_missing_sources.append(source)
                    if true_missing_sources:
                        new_contributes_to_source_dictionary = current_sources_contributes_to+true_missing_sources
                    else:
                        new_contributes_to_source_dictionary = current_sources_contributes_to

                    graph[cause_concept][effect_concept][edge_key]['sources']=new_contributes_to_source_dictionary
                    #could have used extend instead but was unsure if it would work as needed

    populate_edges(graph)


#run populate edges program
populate_edges(G)



#side note: there should be different types of networkx node objects. one for classes. one for individuals.


#visualize the connectivity of the graph (visualize the cause-effects relations graph) 

# nx.draw(G)
# plt.savefig("/Users/kameronr/Documents/personal/climate change outreach/new uploads/networkx_graph_ontology.png")
# plt.show()
#draw just the is_a edges of bases
#https://networkx.org/documentation/stable/reference/drawing.html
#edges_to_draw = [edge for edge in G.edges if edge[2]=="is_a"]
edges_to_draw = [edge for edge in G.edges if edge[2]=="contributesTo"]

# edges_to_draw = []
# for edge in G.edges:
# breakpoint()

subgraph_to_draw = G.edge_subgraph(edges_to_draw)

nx.draw(subgraph_to_draw)
# plt.savefig("/Users/kameronr/Documents/personal/climate change outreach/new uploads/networkx_graph_ontology_contributes_to.png")
# plt.show()

# import networkx as nx
import pylab as plt
from networkx.drawing.nx_agraph import graphviz_layout, to_agraph
import pygraphviz as pgv

for (n1, n2, d) in G.edges(data=True):
    d.clear()

breakpoint()
for (n, d) in G.nodes(data=True):
    breakpoint()
    d.clear()

# pos = nx.nx_pydot.graphviz_layout(G, prog="dot")
A = to_agraph(G)


path = '/Users/kameronr/Documents/personal/climate change outreach/new uploads/networkx_graph_ontology_contributes_to_for_graphviz.txt'
with open(path, 'w') as f:
    print(A, file=f)

# A.layout('dot')
# A.draw('/Users/kameronr/Documents/personal/climate change outreach/new uploads/networkx_graph_ontology_contributes_to_graphviz_dot.pdf')

# A.layout('neato')
# A.draw('/Users/kameronr/Documents/personal/climate change outreach/new uploads/networkx_graph_ontology_contributes_to_graphviz_neato.pdf')

# A.layout('sfdp')
# A.draw('/Users/kameronr/Documents/personal/climate change outreach/new uploads/networkx_graph_ontology_contributes_to_graphviz_sfdp.pdf')

# A.layout('fdp')
# A.draw('/Users/kameronr/Documents/personal/climate change outreach/new uploads/networkx_graph_ontology_contributes_to_graphviz_fdp.pdf')
























































