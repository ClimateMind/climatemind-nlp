#convert OWL file into networkx object

#also code to convert networkx object to OWL file

#and code to integrate OWL file with already existing networkx object

#goals of these scripts are to provide tools to be able to allow annotators use protege or webprotege to organize heirarchy of bases that way that heirarchy can then be imported back with python to the networkx represenation of the ontology.


from owlready2 import *
import networkx as nx
import pandas as pd






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
onto.save(file = "/Users/kameronr/Documents/personal/climate change outreach/new uploads/NLP_ontology_standardized_bases_only.rdfxml", format = "rdfxml")



#if I run this script 3 times in a row I get a weird error about '1599844502_base' [climate change] not being a Class (so it fails because it's a subclass and not a class so can't get added to '1925045096_full_base' [human-caused_climate_change])... suggests need more error catching and if then else statements to avoid redoing work already done... and if doing work already done then it should catch itself and skip that work


#problem with '1599844502_base' and 'Thing'
#     neighbors=nx.neighbors(G, node)

#list(onto.classes())


#TO DO:
#add in all the other ontology information into the owl object

#TO DO:
#load in the modified base heirarchy file and then process it and integrate the information into the old networkx object to form a new updated improved networkx object



#side note: there should be different types of networkx node objects. one for classes. one for individuals.
































































