##### 1. Find parent Concept in MRCONSO.RRF
##Gastrointesintal tract = C0017189

class node(object):
######################################################################
#node is pointer that points both up to ancestor and down to descendants. Contains functions for traversing tree,
    ## for confirming ancestry, and for outputting graph of tree
    def __init__(self):
        self.name=None
        self.children=[]
        self.parent=[]
        self.term = None
    def child(self,child):
        "Gets a node by number"
        return self.children[child]
    def parent(self):
        return self.prev

    def goto(self,data):
        "Gets immediate child by name (use find_node for finding any node in tree)"
        for child in range(0,len(self.children)):
            if(self.children[child].name==data):
                return self.children[child]
    def add(self):
        node1=node()
        node1.parent.append(self)
        self.children.append(node1)
        node1.parent=self
        return node1

    def is_ancestor(self,term=0,cui=0):
    ###INPUT = self + ancestors term OR cui
    ###OUTPUT = boolean T/F. For use with mapping hierarchies
        current_node = self
        while current_node.parent:
            if current_node.term == term or current_node.name == cui:
                return True
            else:
                current_node=current_node.parent
        if current_node.term == term or current_node.name == cui:
            return True
        else:
            return False

    def find_node(self, name,visited=[],found=[]):
        "Finds any node by name within the tree. Transverses ENTIRE tree since synonymous names are possible"
    ####INPUT = name to find (cui)
    ####OUTPUT = list of matching nodes found (may return more than one to account for multiple parents)
        root = self
        while root.parent:
            root=root.parent
        child_list = root.children
        i = 0
        if root.name == name:
            found.append(root)
            return found
        while child_list:
            new_child_list=[]
            for child in child_list:
                if child in visited:
                    continue
                else:
                    new_child_list+=(child.children)
                    visited.append(child)
                if child.name == name:
                    found.append(child)
                    child_list = []
                    break
                i += 1
            child_list=new_child_list

        return found


    def draw_tree(self,filename,layout='dot',root='top'):
        "Creats .dot and .png files of given file name visually depicting structure of the tree"
        #### INPUT-  filename, layout type (which algorithm to draw tree with from pygraph viz), and root (default =
        ###          top root node). *Note - root can be ANY NODE in tree which includes node used in call
        ###  OUTPUT - .dot of graph information and .png file of the tree, both starting at indicated root

        import pygraphviz as pgv
        this_graph = pgv.AGraph(directed=True)
        if root == 'top':
            while self.parent:
                self = self.parent
        else:
            self= self.find_node(root)[0]
        def make_edges(self):
            for child_node in self.children:
                this_graph.add_edge(self.term, child_node.term)
                make_edges(child_node)
        make_edges(self)
        this_graph.write(filename+'.dot')
        this_graph.layout(prog=layout)
        this_graph.draw(filename+'.png')




    def pickle_tree(self,filename=0):
        "Pickles entire tree, starting from any node within that tree"
        #### INPUT - filename of the resulting .pkl document
        #### OUTPUT - .pkl document that contains a list of all nodes in the tree.

        ### Get to top root ###
        while self.parent:
            self = self.parent
        print 'start - ' + self.term
        nodes_list=[self]
        visited=[]
        child_list=self.children
        nodes_list+=child_list
        children_of_child_list=[]

        ### Build list of all child nodes
        while child_list:
            children_of_child_list=[]
            for child in child_list:
                if child in visited: 
                    continue
                else:
                    children_of_child_list+=child.children
            child_list = children_of_child_list
            nodes_list+=child_list

        ### writes object out to .pkl #########
        import cPickle as pickle
        with open(filename+'.pkl', 'wb') as output:  # Will overwrite existing files
            pickle.dump(nodes_list, output, pickle.HIGHEST_PROTOCOL)


class snomedNavigator(object):
    '''snomed builds dictionary from snomed files for ontologies and relationships of interests.
        and contains functions to navigate and save those files'''
    def __init__(self,description_full_path=None,stated_relationship_path=None):
        self.description_full_path=description_full_path  ## path to UMLS MRCONSO.RRF file
        self.stated_relationship_path=stated_relationship_path  ## path to UMLS MRREL.RRF file
        self.term_dictionary={} ##dict of dicts that holds MRCONSO data for relevant ontologies
                                    #format: {ontology name: {cui : term}}
        self.relationship_dictionary={} #dict that holds relationships between subject cui and pertinent object
                                            #format: {subject_cui: [relationship, object_cui]}
        # import node

    # def find_term


    def get_terms_and_cuis(self):
        "gets all terms for given ontologies"
        with open(self.description_full_path) as description_and_id_list:
            for line in description_and_id_list:
                line = line.split('|')
                cui = line[0]
                lang = line[1]
                source = line[11]
                term_name = line[14]
                if source not in self.ontologies:
                    continue
                else:
                    if cui in self.term_dictionary[source]:
                        current_terms= self.term_dictionary[source][cui]
                        current_terms.append(term_name)
                        self.term_dictionary[source][cui]=current_terms
                    else:
                        self.term_dictionary[source][cui]=[term_name]

    def get_synonyms(self,target_cui,language='ENG',ontologies=0):
        "Get all synonyms for a cui with given language and ontolgoy (optional)"
        #NOTE - synonyms from CHV include the adjectival and other forms of important antamoical nouns
        synonym_list=[]  #list to hold all mappings of target cui
        if ontologies !=0:
            if type(ontologies) != list:
                ontologies=[ontologies]
        print ontologies
        with open(self.mrconso_path) as umls_cui_list:
            for line in umls_cui_list:
                line = line.split('|')
                cui = line[0]
                lang = line[1]
                source = line[11]
                term_name = line[14]

                if ontologies !=0:
                    if source not in ontologies:
                        continue
                if lang != language:
                    continue
                if cui != target_cui:
                    continue
                else:
                    synonym_list.append(term_name.lower())
        synonym_list=list(set(synonym_list))
        return (target_cui,synonym_list)






    def get_relationships(self,relationship_name=0):
        "Gets relationsihps for terms in a given ontology (optionally with a given relationship)"
        ### INPUT = self.ontologies, relationship name optional (e.g. has_regional_part)
        ### OUTPUT = All the relationships between CUIS in target ontology
        with open(self.mrrel_path) as umls_relationships:
            for line in umls_relationships:
                line = line.split('|')
                object_source=line[10]
                subject_source= line[11]
                if subject_source not in self.ontologies:
                    continue
                relationship=line[7]
                if relationship_name != 0 and relationship != relationship_name:
                    continue
                rui = line[8]
                subject = line[4]
                object = line[0]
                if subject == object:
                    continue
                if subject in self.relationship_dictionary:
                    current_relations=self.relationship_dictionary[subject]
                    current_relations.append([relationship,object])
                else:
                    self.relationship_dictionary[subject]=[[relationship,object]]


    def get_related_cuis(self,subject_cui,target_relation=0,ontology=0,current_list=[],cui_obj_mapping={},
                         tree=0,first_call=0):
        "Returns all cuis related to an input cui, and having a specific relationship (if specified)"
        ###INPUT = self.relationship_dict, subject_cui, relationship (optional)
        ###OUTPUT = all cuis related to that subject (optionally with a given relationship)
        if ontology != 0:
            ontology_list = [ontology]
        else:
            ontology_list = self.ontologies
        if first_call==1:
            tree=node()
            tree.name=subject_cui
            cui_obj_mapping[subject_cui]=tree
            for ontology in ontology_list:
                if subject_cui in self.term_dictionary[ontology]:
                    tree.term= self.term_dictionary[ontology][subject_cui][0]
        related_cuis=[]
        relationship_list=[]
        if subject_cui in self.relationship_dictionary:
            relationship_list=self.relationship_dictionary[subject_cui]
        if target_relation != 0:
            for relationship in relationship_list:
                relation = relationship[0]
                object_cui = relationship[1]
                if relation == target_relation:
                    related_cuis.append(object_cui)
        first_level=[]

        ### SET MECHANISM TO REUTURN AT END OF RECURSION ####
        if first_call==1:
            first_level=related_cuis
            related_cuis.append('*last item')
            print first_level

        if related_cuis:
            if type(related_cuis) != list:
                related_cuis = [related_cuis]
            current_list += related_cuis

        for object_cui in related_cuis:
            ### RETURN AT THE END
            if object_cui == '*last item':
                del related_cuis[-1] ##remove tracker
                return cui_obj_mapping
            if object_cui == 'C4240456': continue ## gets rid of improper dental relationship for GI tract
            ### Loops through ontologies in dictionary to find cui's. Breaks after first hit. This could be changed
            ### to handle synonymous terms within the ontology in a less subjective way
            for ontology in ontology_list:
                onto_term_dictionary=self.term_dictionary[ontology]
                if subject_cui in onto_term_dictionary:
                    parent_term = self.term_dictionary[ontology][subject_cui][0]
                if parent_term:
                    break
            for ontology in ontology_list:
                onto_term_dictionary=self.term_dictionary[ontology]
                if object_cui in onto_term_dictionary:
                    child_term = self.term_dictionary[ontology][object_cui][0]
                if child_term:
                    break
            #################################################
            tree = cui_obj_mapping[subject_cui]
            tree=tree.add()
            tree.name=subject_cui
            tree.term=child_term
            cui_obj_mapping[object_cui]= tree


            self.get_related_cuis(subject_cui=object_cui,target_relation=target_relation,current_list=current_list,
                                  cui_obj_mapping=cui_obj_mapping,tree=tree)

    def term_to_cui(self,ontology,term):
        for cui in self.term_dictionary[ontology]:
            for term_string in self.term_dictionary[ontology][cui]:
                term_string = term_string.lower()
                if term_string == term:
                    return (cui,term)



class umlsNavigator(object):
    '''umlsNavigator builds dictionary from UMLS files for ontologies and relationships of interests.
        and contains functions to navigate and save those files'''
    def __init__(self,mrconso_path=None,ontologies=None,mrrel_path=None):
        self.mrconso_path=mrconso_path  ## path to UMLS MRCONSO.RRF file
        self.ontologies=ontologies  ## ontology UMLS 3 letter abbreviations, will be used for later functions
        self.mrrel_path=mrrel_path  ## path to UMLS MRREL.RRF file
        self.term_dictionary={} ##dict of dicts that holds MRCONSO data for relevant ontologies
                                    #format: {ontology name: {cui : term}}
        self.relationship_dictionary={} #dict that holds relationships between subject cui and pertinent object
                                            #format: {subject_cui: [relationship, object_cui]}
        # import node

    # def find_term


    def get_terms_and_cuis(self):
        "gets all terms for given ontologies"
        for ontology in self.ontologies:
            if ontology not in self.term_dictionary:
                self.term_dictionary[ontology]={}
        with open(self.mrconso_path) as umls_cui_list:
            for line in umls_cui_list:
                line = line.split('|')
                cui = line[0]
                lang = line[1]
                source = line[11]
                term_name = line[14]
                if source not in self.ontologies:
                    continue
                else:
                    if cui in self.term_dictionary[source]:
                        current_terms= self.term_dictionary[source][cui]
                        current_terms.append(term_name)
                        self.term_dictionary[source][cui]=current_terms
                    else:
                        self.term_dictionary[source][cui]=[term_name]

    def get_synonyms(self,target_cui,language='ENG',ontologies=0):
        "Get all synonyms for a cui with given language and ontolgoy (optional)"
        #NOTE - synonyms from CHV include the adjectival and other forms of important antamoical nouns
        synonym_list=[]  #list to hold all mappings of target cui
        if ontologies !=0:
            if type(ontologies) != list:
                ontologies=[ontologies]
        print ontologies
        with open(self.mrconso_path) as umls_cui_list:
            for line in umls_cui_list:
                line = line.split('|')
                cui = line[0]
                lang = line[1]
                source = line[11]
                term_name = line[14]

                if ontologies !=0:
                    if source not in ontologies:
                        continue
                if lang != language:
                    continue
                if cui != target_cui:
                    continue
                else:
                    synonym_list.append(term_name.lower())
        synonym_list=list(set(synonym_list))
        return (target_cui,synonym_list)






    def get_relationships(self,relationship_name=0):
        "Gets relationsihps for terms in a given ontology (optionally with a given relationship)"
        ### INPUT = self.ontologies, relationship name optional (e.g. has_regional_part)
        ### OUTPUT = All the relationships between CUIS in target ontology
        with open(self.mrrel_path) as umls_relationships:
            for line in umls_relationships:
                line = line.split('|')
                object_source=line[10]
                subject_source= line[11]
                if subject_source not in self.ontologies:
                    continue
                relationship=line[7]
                if relationship_name != 0 and relationship != relationship_name:
                    continue
                rui = line[8]
                subject = line[4]
                object = line[0]
                if subject == object:
                    continue
                if subject in self.relationship_dictionary:
                    current_relations=self.relationship_dictionary[subject]
                    current_relations.append([relationship,object])
                else:
                    self.relationship_dictionary[subject]=[[relationship,object]]


    def get_related_cuis(self,subject_cui,target_relation=0,ontology=0,current_list=[],cui_obj_mapping={},
                         tree=0,first_call=0):
        "Returns all cuis related to an input cui, and having a specific relationship (if specified)"
        ###INPUT = self.relationship_dict, subject_cui, relationship (optional)
        ###OUTPUT = all cuis related to that subject (optionally with a given relationship)
        if ontology != 0:
            ontology_list = [ontology]
        else:
            ontology_list = self.ontologies
        if first_call==1:
            tree=node()
            tree.name=subject_cui
            cui_obj_mapping[subject_cui]=tree
            for ontology in ontology_list:
                if subject_cui in self.term_dictionary[ontology]:
                    tree.term= self.term_dictionary[ontology][subject_cui][0]
        related_cuis=[]
        relationship_list=[]
        if subject_cui in self.relationship_dictionary:
            relationship_list=self.relationship_dictionary[subject_cui]
        if target_relation != 0:
            for relationship in relationship_list:
                relation = relationship[0]
                object_cui = relationship[1]
                if relation == target_relation:
                    related_cuis.append(object_cui)
        first_level=[]

        ### SET MECHANISM TO REUTURN AT END OF RECURSION ####
        if first_call==1:
            first_level=related_cuis
            related_cuis.append('*last item')
            print first_level

        if related_cuis:
            if type(related_cuis) != list:
                related_cuis = [related_cuis]
            current_list += related_cuis

        for object_cui in related_cuis:
            ### RETURN AT THE END
            if object_cui == '*last item':
                del related_cuis[-1] ##remove tracker
                return cui_obj_mapping
            if object_cui == 'C4240456': continue ## gets rid of improper dental relationship for GI tract
            ### Loops through ontologies in dictionary to find cui's. Breaks after first hit. This could be changed
            ### to handle synonymous terms within the ontology in a less subjective way
            for ontology in ontology_list:
                onto_term_dictionary=self.term_dictionary[ontology]
                if subject_cui in onto_term_dictionary:
                    parent_term = self.term_dictionary[ontology][subject_cui][0]
                if parent_term:
                    break
            for ontology in ontology_list:
                onto_term_dictionary=self.term_dictionary[ontology]
                if object_cui in onto_term_dictionary:
                    child_term = self.term_dictionary[ontology][object_cui][0]
                if child_term:
                    break
            #################################################
            tree = cui_obj_mapping[subject_cui]
            tree=tree.add()
            tree.name=subject_cui
            tree.term=child_term
            cui_obj_mapping[object_cui]= tree


            self.get_related_cuis(subject_cui=object_cui,target_relation=target_relation,current_list=current_list,
                                  cui_obj_mapping=cui_obj_mapping,tree=tree)

    def term_to_cui(self,ontology,term):
        for cui in self.term_dictionary[ontology]:
            for term_string in self.term_dictionary[ontology][cui]:
                term_string = term_string.lower()
                if term_string == term:
                    return (cui,term)

    # def verify_tree

class snomedNavigator(object):
    '''snomed builds dictionary from snomed files for ontologies and relationships of interests.
        and contains functions to navigate and save those files'''

    def __init__(self, description_full_path=None, stated_relationship_path=None):
        self.description_full_path = description_full_path  ## path to UMLS MRCONSO.RRF file
        self.stated_relationship_path = stated_relationship_path  ## path to UMLS MRREL.RRF file
        self.term_dictionary = {}  ##dict of dicts that holds MRCONSO data for relevant ontologies
        # format: {ontology name: {cui : term}}
        self.relationship_dictionary = {}  # dict that holds relationships between subject cui and pertinent object
        # format: {source_id: [relationship, destination_id]}
        self.inverse_relationship_dictionary = {}  # dict that hodls the inverse of relationships
        self.umls_navigator = False
        # import node

    # def find_term


    def get_terms_and_cuis(self):
        "gets all terms for given ontologies"
        # term_dictionary = {}
        i = 0
        with open(self.description_full_path) as description_and_id_list:
            for line in description_and_id_list:
                line = line.split('\t')
                cui = line[4]
                term_name = line[7]
                if cui not in self.term_dictionary:
                    self.term_dictionary[cui] = term_name

                    if i < 5: print self.term_dictionary
                    i += 1

    def get_synonyms(self, target_cui, language='ENG', ontologies=0):
        "Get all synonyms for a cui with given language and ontolgoy (optional)"
        # NOTE - synonyms from CHV include the adjectival and other forms of important antamoical nouns
        synonym_list = []  # list to hold all mappings of target cui
        if ontologies != 0:
            if type(ontologies) != list:
                ontologies = [ontologies]
        print ontologies
        with open(self.mrconso_path) as umls_cui_list:
            for line in umls_cui_list:
                line = line.split('|')
                cui = line[0]
                lang = line[1]
                source = line[11]
                term_name = line[14]

                if ontologies != 0:
                    if source not in ontologies:
                        continue
                if lang != language:
                    continue
                if cui != target_cui:
                    continue
                else:
                    synonym_list.append(term_name.lower())
        synonym_list = list(set(synonym_list))
        return (target_cui, synonym_list)

    def get_relationships(self, relationship_name=0):
        "Gets relationsihps for terms in a given ontology (optionally with a given relationship)"
        # unclear whether specifying a relationship is necessary given small size of full set
        ### INPUT = self.ontologies, relationship name optional (e.g. has_regional_part)
        ### OUTPUT = All the relationships between CUIS in target ontology
        with open(self.stated_relationship_path) as snomed_relationships:
            i = 0
            for line in snomed_relationships:
                if i == 0:
                    i += 1
                    continue
                line = line.split('\t')
                source_id = line[
                    4]  ##Structured as source, has relationship to, destination (e.g. change is a finding)
                destination_id = line[5]
                relationship_type_id = line[7]
                #### CHECK CORRECT RELATIONSHIP IS PRESENT ###
                if relationship_name != 0 and relationship_type_id != relationship_name:
                    continue
                #### SKIP IDENTITY RELATIONSHIP ###
                if source_id == destination_id:
                    continue
                ###### BUILD SOURCE DICTIONARY #####
                if source_id in self.relationship_dictionary:
                    current_relations = self.relationship_dictionary[source_id]
                    current_relations.append([relationship_type_id, destination_id])
                else:
                    self.relationship_dictionary[source_id] = [[relationship_type_id, destination_id]]
                #### BUILD REVERSE DICTIONARY #####
                if destination_id in self.inverse_relationship_dictionary:
                    current_relations = self.inverse_relationship_dictionary[destination_id]
                    current_relations.append([relationship_type_id, source_id])
                else:
                    self.inverse_relationship_dictionary[destination_id] = [
                        [relationship_type_id, source_id]]
                    ############ MAY NEED TO RECODE FROM SCRATCH ###################

    def get_related_cuis(self, destination_id, target_relation=0, current_list=[], cui_obj_mapping={},
                         tree=0, first_call=1, inverse=0):
        "Returns all cuis related to an input cui, and having a specific relationship (if specified)"
        ###INPUT = self.relationship_dict, destination_id, relationship (optional)
        ###OUTPUT = all cuis related to that subject (optionally with a given relationship)

        if inverse == 0:
            relationship_dictionary = self.relationship_dictionary
        elif inverse == 1:
            relationship_dictionary = self.inverse_relationship_dictionary
        if first_call == 1:
            tree = node()
            tree.name = destination_id
            cui_obj_mapping[destination_id] = tree
            if destination_id in self.term_dictionary:
                tree.term = self.term_dictionary[destination_id]
        related_cuis = []
        relationship_list = []

        if destination_id in relationship_dictionary:
            relationship_list = relationship_dictionary[destination_id]
        if target_relation != 0:
            for relationship in relationship_list:
                relation = relationship[0]
                source_id = relationship[1]
                # print 'begin'
                # print self.term_dictionary[destination_id]
                # print self.term_dictionary[relation]
                # print self.term_dictionary[source_id]
                # print 'end'
                if relation == target_relation:
                    related_cuis.append(source_id)
        first_level = []

        ### SET MECHANISM TO REUTURN AT END OF RECURSION ####
        if first_call == 1:
            first_level = related_cuis
            related_cuis.append('*last item')

        if related_cuis:
            # print related_cuis

            if type(related_cuis) != list:
                related_cuis = [related_cuis]
            current_list += related_cuis

        for source_id in related_cuis:
            ### RETURN AT THE END

            if source_id == '*last item':
                del related_cuis[-1]  ##remove tracker
                return cui_obj_mapping
            # print source_id
            # print self.term_dictionary[source_id]
            if destination_id in self.term_dictionary:
                parent_term = self.term_dictionary[destination_id]
                # print 'parent'
                # print parent_term
                # if parent_term:
                #     break
            if source_id in self.term_dictionary:
                child_term = self.term_dictionary[source_id]
                # print 'child'
                # print child_term
            # else: child_term = False
            #     # if child_term:
            #     #     break
            #################################################
            tree = cui_obj_mapping[destination_id]
            # if child_term:
            tree = tree.add()
            tree.name = source_id
            tree.term = child_term
            cui_obj_mapping[source_id] = tree

            if inverse == 0:
                self.get_related_cuis(destination_id=source_id, target_relation=target_relation,
                                      current_list=current_list,
                                      cui_obj_mapping=cui_obj_mapping, tree=tree, first_call=0)
            elif inverse == 1:
                self.get_related_cuis(destination_id=source_id, target_relation=target_relation,
                                      current_list=current_list,
                                      cui_obj_mapping=cui_obj_mapping, tree=tree, inverse=1, first_call=0)

    def get_concept_terms(self, concept_type):
        #### INPUT = 'concept type'
        #### OUTPUT = object_tree containing all the snomed node objects
        # NOTE - is used to simplify the call to get_related_cuis, which has more flexibility, but is more complex
        if concept_type.lower() == 'negation':
            object_tree = self.get_related_cuis(destination_id='272519000', target_relation='116680003',
                                                inverse=1)
        elif concept_type.lower() == 'qualifier':
            object_tree = self.get_related_cuis(destination_id='362981000', target_relation='116680003',
                                                inverse=1)
        elif concept_type.lower() == 'qualifier_minimal':
            ## SNOMED counts a LOT (e.g. languages) as qualifiers, so this returns a smaller, more common usage list of
            ## the sub-qualifiers that are most applicable to common language
            ### Look into making a customized qualifer list (try mix of Finding values + Finding status values +

            # General information qualifier, + Result Comments + Ranked categories + Descriptor +
            # Modifier mainly for procedure + special information qualifier)
            gen_info_qual_tree = self.get_related_cuis(destination_id='106227002',
                                                       target_relation='116680003', inverse=1)
            result_comments_tree = self.get_related_cuis(target_relation='116680003',
                                                         destination_id='281296001', inverse=1)
            ranked_categories_tree = self.get_related_cuis(target_relation='116680003',
                                                           destination_id='272396007', inverse=1)
            descriptor_tree = self.get_related_cuis(target_relation='116680003', destination_id='272099008',
                                                    inverse=1)
            modifier_tree = self.get_related_cuis(target_relation='116680003', destination_id='106239005',
                                                  inverse=1)
            special_info_qual_tree = self.get_related_cuis(target_relation='116680003',
                                                           destination_id='106239005', inverse=1)
            from util import merge_dicts
            object_tree = merge_dicts(gen_info_qual_tree, result_comments_tree, ranked_categories_tree,
                                      descriptor_tree, modifier_tree, special_info_qual_tree)
            # object_tree.update(gen_info_qual_tree).update(result)



        else:
            return NameError
        return object_tree


        #### Example call ###
        # this_tree=snowy.get_related_cuis(destination_id='272099008',target_relation='116680003',inverse=1)

    def make_snomed_umls_navigator(self, mrconso_path):
        ontology = ['SNOMEDCT_US']
        self.umls_navigator = umlsNavigator(mrconso_path=mrconso_path, ontologies=ontology)
        self.umls_navigator.get_terms_and_cuis()

    def term_to_umls_cui(self, term):
        # term = term.lower()
        if not self.umls_navigator:
            print 'ERROR - no umls_navigator object variable created'
            return False

        ontology = 'SNOMEDCT_US'
        umls_navigator = self.umls_navigator
        if umls_navigator.inverse_term_dictionary == False:
            reversed_dic = {}
            snomed_reversed_terms_dict = {}
            reversed_dic[ontology] = snomed_reversed_terms_dict
            for cui in umls_navigator.term_dictionary[ontology]:
                for term_string in umls_navigator.term_dictionary[ontology][cui]:
                    snomed_reversed_terms_dict[term_string] = cui
            umls_navigator.reverse_term_dictionary = reversed_dic

        ### BRUTE FORCE SLOW SEARCH
        cui = umls_navigator.inverse_term_dictionary[ontology].get(term, None)
        return (cui, term)
        # for cui in umls_navigator.term_dictionary[ontology]:
        #     for term_string in umls_navigator.term_dictionary[ontology][cui]:
        #         term_string = term_string.lower()
        #         if term_string == term:
        #             return (cui,term)





###### CODE TO MAKE UMLS OBJECT #########
import util
#
# umls_obj = umlsNavigator(mrconso_path='/usr/share/2017AB-full/2017AB/META/MRCONSO.RRF',
#                   mrrel_path='/usr/share/2017AB-full/2017AB/META/MRREL.RRF', ontologies=['FMA'])
# umls_obj.get_terms_and_cuis()
# umls_obj.get_relationships(relationship_name='has_regional_part')
# util.save_dill_object(umls_obj,'dill-object.pkl')
# # util.save_object(umls_obj,'umls-object.pkl')
# umls_obj = util.load_object('umls-object.pkl')
# umls_obj=util.load_dill_object('dill-object.pkl')
# print umls_obj
# print umls_obj.term_dictionary
# this_tree=umls_obj.get_related_cuis(subject_cui='C0017189',target_relation='has_regional_part',first_call=1)
## tree has all the good cui objects
# x= umls_obj.term_to_cui('FMA','descending colon')
# print x
# for key in this_tree: print key

# print umls_obj.get_synonyms(target_cui=x[0],ontologies='CHV')

#### GET REGEX RELATED TERMS ###
# location_list=['ileum','duodenum','jejunum','ascending colon','transverse colon','descending colon','sigmoid colon','rectum','stomach','esophagus']
# count=0
# for location in location_list:
#     print count
#     print umls_obj.get_synonyms(umls_obj.term_to_cui('FMA',location)[0],ontologies='CHV')
#     count +=1

##### REGEX PART ABOVE ##########################3
#### normal code for running things is below here ####

### TO-DO ####
##1. Separate CUI extraction and term extraction/visualization
##2. Will need to use regex matcher for expanded queries + simstring for normal queries and select filter for double counting
##3. Overall flow
    #A. Get CUIs list to compare against metamap matches (general tool)
        ##Can do this for anatomical areas, negations, and qualifiers (See below)
        ##Should I switch to a NegEx approach to this?
            ###If we can open the QuickUMLS up could do more advanced dependency parsing
    #B. Get terms lists (expanded from cuis) for regex matching and expansion
        ## need this to catch things like ileal-, ileo, ileosigmoid, etc...
    #C. Rectify the above two
    #D. Use spaCy + simstring matching for the activity terms from Ryan
    #E. output .ann & .ftr

###NOTES for adding negation & qualifiers ###
    #>. Chasing down "Finding status values" from SNOMED WILL GET A LIST OF QUALIFIERS
        ### Certainties = C0439543 (parent isn't mapped...)
        ### Change findings =
        ### Degree findings = C0442795
    #>. Chasing down "Findings Values" can get negation findings, degree findings,normality findings
        # (not grouped with negation, so need to add it + it's subclass in)
        ### findings values = C0442719
        ### C0205307 = CUI for normal
        ### absence findings for negation C0442733
    #> ***USE 'inverse_isa' relationship to go to bottom

#######SNOMED is COMPLETELY!!! fucked in UMLS ############


###How to handle annotations?
#### A. Do nothing for now, and handle hierarchies as they come = leave cui in annotation
    ### let's do this for now...
#### B. Make object that handles transition between UMLS & REST?
#### C. Make function that maps annotation levels to cui


#### RANDOM NOTES###
### 'Ileum' FMAID = 7208
    # under "segment of small intestine"
    #MRREL ##parent
                ###has regional part **** (this gets us the goods)
                    #### get rid of anything with '\sof\s' in the name
                    #### exclude identity (every/usr/share/2017AB-full/2017AB/META/MRREL.RRFthing is it's own regional part)

    #MRREL Structure
        # C0014876|A15412397|SCUI|RO|C0017189|A15456853|SCUI|has_regional_part|R167633144||FMA|FMA|||N||
        #  is regional part|        | has_part|              | indicated relation
        # using SIB and CHD or PAR relationships could potentially accomplish same, but seems risky (DIDN'T WORK IN THIS CASE!!)
##### 3. Trace from descendent up to parent
    ### get descendent and all siblings
    ### go to next parent term and get all those siblings
    ### repeat until parent is within siblings


##### 4. Expand query
    ### find all synonymous terms for each cui for each concept

###Should extract all the terms

####ONTOLOGY SELECTION FLOW #####
###1. Extract ontology(ies) of interest from database
    ###a. extract synonyms of desired term from database
    ###b. creating mapping structure from synonyms to desired term and cui
    ###c. need to figure out how to get atoms out as well
        ### MRXNW_ENG.RRF (has list of related lexical variants)

### p. 84 has key words to look for related to stricture