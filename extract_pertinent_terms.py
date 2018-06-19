##### 1. Find parent Concept in MRCONSO.RRF
##Gastrointesintal tract = C0017189

class node(object):
######################################################################
#node is pointer that points both up to ancestor and down to descendants. Contains functions for traversing tree,
    ## for confirming ancestry, and for outputting graph of tree
    def __init__(self):
        self.id=None
        self.children=[]
        self.parent=[]
        self.term = None
        self.concept_type=None
    def child(self,child):
        "Gets a node by number"
        return self.children[child]
    def parent(self):
        return self.prev

    def goto(self,data):
        "Gets immediate child by name (use find_node for finding any node in tree)"
        for child in range(0,len(self.children)):
            if(self.children[child].id==data):
                return self.children[child]
    def add(self):
        node1=node()
        node1.parent.append(self)
        self.children.append(node1)
        node1.parent=self
        return node1

    def get_children(self,child_list=[],cuis_only=0,cuis_list=[]):
        ## INPUT = self
        ## OUTPUT = all child nodes
        current_node=self
        while current_node.children:
            child_list+=current_node.children
            child_list=set(child_list)
            child_list=list(child_list)
            for child in current_node.children:
                cuis_list.append(child.id)
                current_node=child
                current_node.get_children(child_list=child_list)
        if cuis_only==1:
            return cuis_list
        else:
            return child_list


    def is_ancestor(self,term=0,cui=0):
    ###INPUT = self + ancestors term OR cui
    ###OUTPUT = boolean T/F. For use with mapping hierarchies
        current_node = self
        while current_node.parent:
            if current_node.term == term or current_node.id == cui:
                return True
            else:
                current_node=current_node.parent
        ### catches top-level term
        if current_node.term == term or current_node.id == cui:
            return True
        else:
            return False

    def find_node(self, id,visited=[],found=[]):
        "Finds any node by name within the tree. Transverses ENTIRE tree since synonymous names/cuis are possible"
    ####INPUT = name to find (cui)
    ####OUTPUT = list of matching nodes found (may return more than one to account for multiple parents)
        root = self
        while root.parent:
            root=root.parent
        child_list = root.children
        i = 0
        if root.id == id:
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
                if child.id == id:
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


class umlsNavigator(object):
    '''umlsNavigator builds dictionary from UMLS files for ontologies and relationships of interests.
        and contains functions to navigate and save those files'''
    def __init__(self,mrconso_path=None,ontologies=None,mrrel_path=None,concept_type=None,target_relationships=[], target_terms=None):
        self.mrconso_path=mrconso_path  ## path to UMLS MRCONSO.RRF file
        self.mrrel_path=mrrel_path  ## path to UMLS MRREL.RRF file

        self._concept_type=concept_type ## used for quick start with known useful relationships & ontologies for
                                        ## particular use cases (e.g. surgeries, anatomical locations)
        self.term_dictionary={} ##dict of dicts that holds MRCONSO data for relevant ontologies
                                    #format: {ontology name: {cui : term}}
        self.relationship_dictionary={} #dict that holds relationships between subject cui and pertinent object
                                            #format: {subject_cui: [relationship, object_cui]}
        self.inverse_term_dictionary={}

        self.ontologies=ontologies  ## ontology UMLS 3 letter abbreviations, will be used for later functions
        self.target_relationships=target_relationships

        self.concept_network_dictionary=False
        self._target_terms=target_terms

        self.target_term_mappings=None
        self.target_morphological_variants={}

        # import node

    # def find_term
    @property
    def ontologies(self):
        return self._ontologies

    @ontologies.setter
    def ontologies(self, value):
        if self._concept_type==None:
            if type(value)==list:
                self._ontologies=value
            else:
                self._ontologies = [value]
        elif self._concept_type.lower() == 'anatomy':
            self._ontologies=['FMA']
            self.get_terms_and_cuis()
        elif self._concept_type.lower() =='surgery':
            self._ontologies=['CPT']
            self.get_terms_and_cuis()

    @property
    def target_relationships(self):
        return self._target_relationships

    @target_relationships.setter
    def target_relationships(self, value):
        if self._concept_type == None:
            if type(value) == list:
                self._target_relationships = value
            else:
                self._target_relationships = [value]
        elif self._concept_type.lower() == 'anatomy':
            self._target_relationships=['has_regional_part']
            self.get_relationships()
        elif self._concept_type.lower() == 'surgery':
            self._target_relationships=['inverse_isa']
            self.get_relationships()
    @property
    def target_term_mappings(self):
        return self._target_term_mappings

    @target_term_mappings.setter
    def target_term_mappings(self,value):
        'setting'
        if self._target_terms == None:
            self._target_terms=value
            print 'target_terms1'
        else:
            print 'target_terms2'
            print self._target_terms
            target_terms_to_cui_dic={}
            for term in self._target_terms:
                mapping=self.term_to_cui(term)
                cui=mapping[0]
                term = mapping[1]
                target_terms_to_cui_dic[term]=cui
            self._target_term_mappings=target_terms_to_cui_dic


    def get_terms_and_cuis(self):
        "gets all terms for given ontologies"
        #*Note - default behavior is to take in all of UMLS if no ontologies are specified
        if self.ontologies:
            for ontology in self.ontologies:
                if ontology not in self.term_dictionary:
                    self.term_dictionary[ontology]={}
                    self.inverse_term_dictionary[ontology]={}
        else:
            if ontology not in self.term_dictionary:
                self.term_dictionary[ontology] = {}
                self.inverse_term_dictionary[ontology] = {}
        with open(self.mrconso_path) as umls_cui_list:
            for line in umls_cui_list:
                line = line.split('|')
                cui = line[0]
                lang = line[1]
                source = line[11]
                term_name = line[14]
                if self.ontologies and source not in self.ontologies:
                    continue
                else:
                    if cui in self.term_dictionary[source]:
                        current_terms= self.term_dictionary[source][cui]
                        current_terms.append(term_name)

                        self.term_dictionary[source][cui]=current_terms
                    else:
                        self.term_dictionary[source][cui]=[term_name]
                    if term_name in self.inverse_term_dictionary[source]:
                        current_cuis=self.inverse_term_dictionary[source][term_name]
                        current_cuis.append(cui)
                        self.inverse_term_dictionary[source][term_name]=current_cuis
                    else:
                        self.inverse_term_dictionary[source][term_name]=[cui]

    def get_synonyms(self,target_cui,language='ENG',ontologies=0):
        "Get all synonyms for a cui with given language and ontolgoy (optional)"
        #NOTE - synonyms from CHV include the adjectival and other forms of important antamoical nouns
        synonym_list=[]  #list to hold all mappings of target cui
        if ontologies !=0:
            if type(ontologies) != list:
                ontologies=[ontologies]
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

    def find_target_morphological_variants(self):
        "Finds all synonyms and variants (UMLS and custom) for target cuis. Useful for regex"
        target_mappings = self.target_term_mappings
        for term in target_mappings:
            cui = target_mappings[term]
            (target_cui, variants) = self.get_synonyms(target_cui=cui)
            self.target_morphological_variants[target_cui] = variants
        if 'Surgery' in self.target_term_mappings:
            surgery_cui = self.target_term_mappings['Surgery']
            current_variants = self.target_morphological_variants[surgery_cui]
            current_variants+=['centesis', 'clasia', 'desis', 'ectomy', 'opsy', 'oscopy', 'stomy', 'tomy', 'pexy', 'plasty', 'rrhaphy']


    def get_relationships(self):
        "Gets relationsihps for terms in a given ontology (optionally with a given relationship)"
        ### INPUT = self.ontologies, relationship name optional (e.g. has_regional_part)
        ### OUTPUT = All the relationships between CUIS in target ontology
        #*NOTE- default behavior is to return all relationships for ontologies of interest (if none specified)
        with open(self.mrrel_path) as umls_relationships:
            for line in umls_relationships:
                line = line.split('|')
                object_source=line[10]
                subject_source= line[11]
                if subject_source not in self.ontologies:
                    continue
                relationship=line[7]
                if self.target_relationships and relationship not in self.target_relationships:
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
                         tree=0,first_call=1):
        "Returns all cuis related to an input cui, and having a specific relationship (if specified)"
        ###INPUT = self.relationship_dict, subject_cui, relationship (optional)
        ###OUTPUT = all cuis related to that subject (optionally with a given relationship)
        if target_relation==0:
            target_relation = self.target_relationships
        elif type(target_relation) != list:
            target_relation=[target_relation]
        if ontology != 0:
            ontology_list = [ontology]
        else:
            ontology_list = self.ontologies
        if first_call==1:
            tree=node()
            tree.id=subject_cui
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
                if relation in target_relation:
                    related_cuis.append(object_cui)
        first_level=[]

        ### SET MECHANISM TO REUTURN AT END OF RECURSION ####
        if first_call==1:
            first_level=related_cuis
            related_cuis.append('*last item')
            print first_level

        if related_cuis:
            print related_cuis
            if type(related_cuis) != list:
                related_cuis = [related_cuis]
            current_list += related_cuis

        for object_cui in related_cuis:
            ### RETURN AT THE END
            if object_cui == '*last item':
                del related_cuis[-1] ##remove tracker
                self.concept_network_dictionary=cui_obj_mapping
                return cui_obj_mapping
            if object_cui == 'C4240456': continue ## gets rid of improper dental relationship for GI tract
            if object_cui in cui_obj_mapping: continue ## helps avoid infite regress with circular definitions
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
            tree.id=subject_cui
            tree.term=child_term
            if self._concept_type:
                tree.concept_type = self._concept_type
            cui_obj_mapping[object_cui]= tree


            self.get_related_cuis(subject_cui=object_cui,target_relation=target_relation,current_list=current_list,
                                  cui_obj_mapping=cui_obj_mapping,tree=tree,first_call=0)

    def term_to_cui(self,term,ontology=0):
        if ontology==0: ## Default to selecting first added ontology (usually only working with 1)
            ontology=self.ontologies[0]
        for cui in self.term_dictionary[ontology]:
            for term_string in self.term_dictionary[ontology][cui]:
                term=term.lower()
                term_string=term_string.lower()
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
        self.concept_network_dictionary = False
        self.cui_mappings = {}
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


    def get_relationships(self, relationship_name=0):
        "Gets relationsihps for terms in SNOMEDCT"
        ### INPUT = self, and optional relationship name
        ### OUTPUT = All the relationships between concepts in SNOMEDCT
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
            tree.id = destination_id
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
            tree.id = source_id
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
            ### Manually add in 'Normal', which isn't in negation finding hierarchy
            normal_node = node()
            normal_node.term='Normal (qualifier value)'
            normal_node.id='17621005'
            object_tree['17621005'] = normal_node

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
        for this_node in object_tree:
            object_tree[this_node].concept_type=concept_type
        self.concept_network_dictionary=object_tree
        # return object_tree


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
    def get_cui_mappings(self):
        if self.concept_network_dictionary == False:
            print 'Error - No concept graph created'
            return self.concept_network_dictionary
        else:
            for item in self.concept_network_dictionary:
                #     print this_tree[item].id
                term = self.concept_network_dictionary[item].term
                mapping= snowy.term_to_umls_cui(term)
                cuis=mapping[0]
                string = mapping[1]
                # if cuis and len(cuis)>1:
                    # print '**start**'
                    # print cuis
                    # print term
                    # print '***'
                if cuis:
                    for cui in cuis:
                        self.cui_mappings[cui]=self.concept_network_dictionary[item]








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



### Look into making a customized qualifer list (try mix of Finding values + Finding status values + General information qualifier, + Result Comments + Ranked categories + Descriptor + Modifiers (see all))
# VERSUS Qualifier value)
    #qualifier value is super class, but has lots of noise (unnecssary sub classes)
## make custom list for negation  (Absence findings + normal)


#### FINAL TO DO
    ### Make above custom lists for easy add in
    ### Pull these into the QuickUMLS annotation workflow
    ### Make pattern matching annotation
    ### Ensure taht no overlaps exists (order by starting index, and iterate through)
    ### Make annotations and push all to wiki