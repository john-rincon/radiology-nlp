####TO-DO####
##1. Fix hierarchical annotations and simplify to more base level things (maybe infer later up to a point)
    ### looks like small bowel and umbrella terms are not mapping well which is a major problem, need to change approach
    ### to map these down to ALL their kids. It's currently only mapping to one, which is likely why there's such an
    #A. this is particularly bad with small bowel --> jejunum
    #B. Also is over annotating the shit out of things that have 'colon' in them
        ##a. cut out all these upper-level terms for now
        ##b. then annotate them, and map them to children
        ##c. only include top-level term in visual?
##2. Either use UMLS and match to FMA database OR make your own simstring implementation with FMA
    #A. Make a fit to use function

import csv,re
inputPath='/home/john/Desktop/nlp_work/full-key-value_stidham.csv'
inputFile = list(csv.reader(open(inputPath, 'rU'), delimiter=','))
# annotation_offset=288
#
# def annotate(fileToAnnotate):
#     for line in inputFile:
#         annotationList=[]
#         for phrase in line[1:]:
#             #find spelling variants of phrase (Gerry's stuff)g
#             #search annotation file for this phrase
#             #find start/stop index
#             #create T1 Term index str for annotation file
#             #append string to list of annotations
#         #write out annotations to file
#             x=1
#         x=1
#     x=1
def findLocations (fileToAnnotate):
    #find location present/absent & index
    #watch for negations
    x=1

def findComplications (fileToAnnotate):
    #find complication present/absent & index
    #watch for negations
    x=1

def findSeverity (fileToAnnotate,locations,complications):
    #using previously found locations and complications, find severity data related to each
    x=1
# print inputFile

modifiers=[]
activityTerms=[]
locationTerms=[]
locationDic={} #figure out how to handle many terms. 'Higher' terms return a list?
complicationDic={} #list of complication phrase


# s mapped to specific terms
complicationList=[] #list of complication related phrases

negator=[]
headerDic={}
reverseHeaderDic={}

negation_dic={}
general_modifier_dic={}
modifiers_inflammation_list=[]
modifiers_stricture_list=[]
clinical_modifiers_dic={}
complicationHeaders=['surgery', 'fistula', 'pouch', 'dilation', 'stricture', 'abscess']
locationHeaders=['ileum', 'duodenum', 'jejunum', 'ascending', 'transverse', 'descending', 'sigmoid', 'rectum', 'stomach', 'esophagus']

def buildList(inputFile):
    x=0  ##row
    for line in inputFile:
        y=0 ## column
        if x==0:
            for word in line:  #makes dictionary header index
                if word != '':
                    headerDic[y]=word.lower()
                y+=1
            x+=1
            continue
        y=0 ##column
        for phrase in line:
            if len(phrase)>0:
                thisHeading=headerDic[y]  #find heading for term
                if thisHeading in complicationHeaders:  #is it a complication?
                    complicationDic[phrase.lower()]=thisHeading
                elif thisHeading.lower() in locationHeaders:  ##is it a location?
                    locationDic [phrase.lower()]=thisHeading
                    # if phrase == 'surgical':  #probably trying to weed out something
                    #     print y
                    #     print line

                    # print phrase
                elif thisHeading.lower() == 'negator':
                    negation_dic[phrase.lower()]=thisHeading
                elif thisHeading == 'modifiers_severity':
                    general_modifier_dic[phrase.lower()]=thisHeading
                elif thisHeading =='modifiers_inflammation_features':
                    # modifiers_inflammation_list.append(phrase.lower())
                    clinical_modifiers_dic[phrase.lower()]=thisHeading
                elif thisHeading == 'modifiers_stricture_features':
                    modifiers_stricture_list.append(phrase.lower())
                    clinical_modifiers_dic[phrase.lower()]=thisHeading
            y+=1
    x+=1

    ##The order of this return is currently hard-coded and important make an object to make this more flexible, as
    ####otherwise this will create issues in the future
    print headerDic
    from clinicalAnnotation import clinicalAnnotation
    clinical_annotation_obj = clinicalAnnotation(location_dic=locationDic,clinical_modifier_dic=clinical_modifiers_dic,complication_dic=complicationDic,negation_list=negation_dic,general_modifier_list=general_modifier_dic)
    print clinical_annotation_obj.complication_dic
    return clinical_annotation_obj
    # print clinical_modifiers_dic
    # return [['clinical_modifiers',clinical_modifiers_dic],['complication',complicationDic], ['location',locationDic], ['modifier',modifiersList], ['negator',negatorList]]

        ###add statements to lists
        ###add statements to dictionary
        ###
        # print headerDic
# print complicationDic
def rapidAnnotate(activityList):   ###deprecated???
    collectionDic={0:'complication',1:'activity',2:'location',3:'modifier',4:'negator'}
    import re
    import spacy
    from ibs_nlp_util import findPhraseAndIndex
    inputPath = '/home/john/Desktop/nlp_work/to-annotate/1-classified.txt'
    inputFile = list(csv.reader(open(inputPath, 'rU'), delimiter=','))
    inputText= unicode(inputFile[0][21].lower())


    ###throw this into the nlpUtil function to get appropriate area and check for dependencies
    # for token in parsed_sentence:
    #     print token.text
    #     print token.idx
    #print inputText
    # for sent in sents:
    #     print len(sent)
    collectionIndex=0 ###track which collection we're at
    findingIndex=1
    annotationList=[]
    ###Re-do below tokenizing by sentence. Need to figure out negation at a decent level
    ###will need to pass both sentence and doc (find in sentence, then index in doc)
    ####will need to search for entire span to figure out boundaries (has to be easier way)
    ##be smart about order (location 1st --> negation + activity), don't do those if unnecessary
    for collection in activityList:
        for key in collection:
            x=findPhraseAndIndex(key,inputText)
            if x:
                for finding in x:
                    termType=collectionDic[collectionIndex]
                    annotation='T'+str(findingIndex)+'\t'+termType+' '+str(finding[1])+' '+str(finding[2])+'\t'+finding[0]
                    print annotation
                    annotationList.append(annotation)
                    findingIndex+=1

        collectionIndex+=1







from ibs_nlp_util import *

def build_relations(annotations):
    return

def makeAllAnnotations(file_range):
    import json
    j = 0
    fileNums=range(file_range)
    for number in fileNums:
        # if j !=21:
        #     j+=1
        #     continue
        j += 1
        # if number != 27: continue ### visualize interesting doc
        # folderPath='/home/john/Desktop/brat-v1.3_Crunchy_Frog/data/rapid-annotated/'
        folderPath = '/home/john/Desktop/nlp_work/test-annotations/'
        full_input_path=folderPath+str(number)+"-classified.txt"
        thisFile=list(csv.reader(open(full_input_path, 'rU'), delimiter=','))
        thisFile=thisFile[0][21]
        ### TO-DO
          ###Change this back from t to a real thing
        foundList=parseFindPhraseAndIndex(thisFile,annotation_obj)

        # for item in foundList[0]:  ##print out all words and indexes where found
        #     print item
        import keyValue
        from ibs_nlp_util import get_object_attributes
        thisCount=0
        unaltered_annotations=[]
        annotation_list=[]
        for kv in foundList[1]:
            if type(kv)==list:
                for value in kv:
                    thisCount+=1
                    if type(value)== keyValue.keyValue:
                        values=get_object_attributes(value)
                        annotation_list+=values
                        unaltered_annotations.append(values)
                        if len(values) > 1:
                            relation = build_relations(values)
            elif kv!=0:
                if type(kv) == keyValue.keyValue:
                    values = get_object_attributes(kv)
                    annotation_list+=values
                    thisCount+=1
                    if len(values) >1 :
                        relation=build_relations(values)
        i=1
        ###def function remove all duplicates
        annotation_list = set(tuple(row) for row in annotation_list)
        annotation_list = list(list(row) for row in annotation_list)
        annotation_list = removeOverlappingPhrases(annotation_list)

        ##### CONVERT OBJECT ANNOTATIONS TO BRAT FORMAT $$$$$$$$
        for annotation in annotation_list:
            term_number='T'+str(i)
            temp = annotation[1]
            # annotation += [temp]
            annotation_formatted=[annotation[0]+' '+str(annotation[2])+' '+str(annotation[3])]
            del annotation[0:]
            annotation+=[term_number]+annotation_formatted+[temp]
            i+=1


        ##### MAKE ANNOTATION LIST OF DICTIONARY FOR USE BY CLASSIFIER ####
        annotations_list_of_dics=[]
        for annotation in unaltered_annotations:
            this_dic={}
            for this_slot in annotation:
                if this_slot[0] in locationHeaders:
                    this_dic['location']=this_slot[0]
                elif this_slot[0] in complicationHeaders:
                    this_dic['complication']=this_slot[0]
                else:
                    this_dic[this_slot[0]]=this_slot[1]
            annotations_list_of_dics.append(this_dic)


        print annotation_list
        #### WRITE OUT BRAT ANNOTATION FILES#####
        brat_annotation_outpath=folderPath+str(number)+"-classified.ann"
        csv_file = csv.writer(open(brat_annotation_outpath, 'wb'), delimiter='\t')
        csv_file.writerows(annotation_list)
        #### WRITE OUT CLASSIFIER ANNOTATION FILES####
        classifier_annotation_outpath=folderPath+str(number)+"-classified.ftr"
        with open(classifier_annotation_outpath,'wb') as classifier_file:
            json.dump(annotations_list_of_dics,classifier_file)
        print j
    print "LAST GOOD FILE"



dependencyList=[0,0,1,1,1]
annotation_obj=buildList(inputFile)
# for line in annotation_obj:
#     print "thisListName == "+"'"+str(line[0])+"':"
#     if line[0] == 'complication':
#         thisCA.complication_list=line[1]
x=annotation_obj.negation_list

for list_name in x:
    print list_name
# makeAllAnnotations(20)

class umlsNavigator(object):
    pass

#### To-Do: make mulitple cui containers (one for each types of object), and pass them all to the do_quick_umls as a list
class cuiContainer(object):
    def __init__(self,cui_to_morphological_variants_dic=None,label_to_cui_dic=None,cui_network=None,negation_cuis=None,qualifier_cuis=None,subject_cuis=None,concept_type="General",ancestor_mappings=0):
        self._concept_type=[concept_type]
        self._cui_to_morphological_variants_dic = {concept_type:cui_to_morphological_variants_dic}
        self._subject_cuis={concept_type:subject_cuis}
        self._ancestor_mappings={concept_type:ancestor_mappings}

   

    @property
    def concept_type(self):
        if type(self._concept_type) != list:
            self._concept_type = [self._concept_type]
        return self._concept_type

    @concept_type.setter
    def concept_type(self, value):
        if self._concept_type == None:
            self._concept_type = [value]
        else:
            if type(self._concept_type) != list:
                self._concept_type=[self._concept_type]
            self._concept_type.append(value)

    @property
    def cui_to_morphological_variants_dic(self):
        return self._cui_to_morphological_variants_dic

    @cui_to_morphological_variants_dic.setter
    ### assumes that new labels and new variants added simultaneously
    def cui_to_morphological_variants_dic(self, value):
        self._cui_to_morphological_variants_dic[self._concept_type[-1]]=value

    @property
    def subject_cuis(self):
        return self._subject_cuis

    @subject_cuis.setter
    ### assumes that new labels and new variants added simultaneously
    def subject_cuis(self, value):
        self._subject_cuis[self._concept_type[-1]] = value

    @property
    def ancestor_mappings(self):
        return self._ancestor_mappings

    @ancestor_mappings.setter
    ### assumes that new labels and new variants added simultaneously
    def ancestor_mappings(self, value):
        self._ancestor_mappings[self._concept_type[-1]] = value





def make_quickumls_annotations(file_range):
    "make quickumls annotation will allow for quickly running annotation code using current parameters "
    import json,copy
    j = 0
    cui_list=[]
    from extract_pertinent_terms import umlsNavigator, node
    import util
    ##################BUILD umlsNavigation object #############
    umls_obj = umlsNavigator(mrconso_path='/usr/share/2017AB-full/2017AB/META/MRCONSO.RRF',
                   mrrel_path='/usr/share/2017AB-full/2017AB/META/MRREL.RRF', ontologies=['FMA'])
    umls_obj.get_terms_and_cuis()
    umls_obj.get_relationships(relationship_name='has_regional_part')
    cui_network=umls_obj.get_related_cuis(subject_cui='C0017189',target_relation='has_regional_part',first_call=1)
        # network has all important umls object
    ################# Handle Important Terms ###############################
    location_list=['ileum','duodenum','jejunum','ascending colon','transverse colon','descending colon','sigmoid colon','rectum','stomach','esophagus']
    label_to_cui_dic={} ## maps location labels to related cui
    for location in location_list:
        term_and_cui=umls_obj.term_to_cui('FMA',location)
        cui=term_and_cui[0]
        label_to_cui_dic[location]=cui

    ###### USE THIS FOR CUI MAPPING ################
    cui_to_morphological_variants_dic={}  ## maps label cuis to mophological variants that need to be regexed
    for label in label_to_cui_dic:
        cui = label_to_cui_dic[label]
        morphos=umls_obj.get_synonyms(target_cui=cui,ontologies='CHV')
        variants=morphos[1]
        cui_to_morphological_variants_dic[cui]=variants

    ############################

    return umls_obj,cui_to_morphological_variants_dic,label_to_cui_dic,cui_network

def regex_matcher(parsed_doc,cui_to_morphological_variants_dic,annotation_offset=0):
    import re
    import spacy
    sent_count=-1
    sentences = list(parsed_doc.sents)
    found_and_indexed_phrases=[]
    for sentence in sentences:
        sent_count+=1
        # print sentence
        sentence_offset= sentence[0].idx+annotation_offset
        sentence=str(sentence)
        for cui in cui_to_morphological_variants_dic:
            if type(cui_to_morphological_variants_dic[cui]) != list:
                cui_to_morphological_variants_dic[cui]=[cui_to_morphological_variants_dic[cui]]
            for variant in cui_to_morphological_variants_dic[cui]:
                # found_phrase = re.findall(r'([a-z\-A-Z]*?' + variant + '[a-zA-Z\-]*?)', str(sentence))
                # if cui != 'C1298908':
                short_found_phrase=False
                variant = variant.strip('*')
                variant = variant.strip('+')
                if len(variant)>3: #find any word/phrases containing variant if long enough (good for affixes esp.)
                    found_phrase = re.findall(r'[^0-9a-zA-Z]*([A-Za-z\-]*' + variant + r'[A-Za-z\-]*)[^0-9a-zA-Z]*', str(sentence),flags=re.IGNORECASE)
                else:
                    #only take whole word matches if short variant is used (good for short negators and qualifiers)
                    short_found_phrase=re.findall(r'([\.\s]('+variant+r')[\.\s])',str(sentence),flags=re.IGNORECASE)
                ### expand phrase to caputure full word in which shorted term is found
                if found_phrase:
                    stop_index = 0
                    for phrase in found_phrase:
                        ###CONVERT THIS TO THE SPACY WAY
                        start_index = sentence[stop_index:].index(phrase)
                        stop_index = start_index + len(phrase)
                        found_and_indexed_phrases.append({'cui':cui,'ngram':phrase, 'start':start_index + sentence_offset, 'end':stop_index + sentence_offset,'sentence':sent_count})
                        # print phraseAndIndex
                if short_found_phrase:
                    stop_index = 0
                    for phrase in short_found_phrase:
                        searchable_form = phrase[0]
                        true_phrase=phrase[1]
                        ###CONVERT THIS TO THE SPACY WAY
                        start_index = sentence[stop_index:].index(searchable_form)

                        this_start= sentence.index(searchable_form)
                        stop_index = start_index + len(searchable_form)

                        start_index += sentence[start_index-1:].index(true_phrase) - 1
                        stop_index=start_index+len(true_phrase)
                        phrase=true_phrase
                        found_and_indexed_phrases.append({'cui':cui,'ngram':phrase, 'start':start_index + sentence_offset, 'end':stop_index + sentence_offset,'sentence':sent_count})
                        # print phraseAndIndex
    return found_and_indexed_phrases



def make_ancestry_mappings(umls_navigator):
    term_mappings = umls_navigator.target_term_mappings

    cui_to_ancestor = {}
    for cui in umls_navigator.concept_network_dictionary:
        found_ancestor = 0
        cui_node = umls_navigator.concept_network_dictionary[cui]
        for term in term_mappings:
            is_ancestor = cui_node.is_ancestor(cui=term_mappings[term])
            if is_ancestor:
                cui_to_ancestor[cui] = term

                found_ancestor = 1
                break
        if found_ancestor != 1:
            cui_to_ancestor[cui] = cui_node.term
    return cui_to_ancestor


def do_quickumls(container,full_input_path,snomed_description_path,snomed_relationship_path,mrconso_path,note_offset=0,negation=1,modifiers='qualifier_minimal'):

    ### TO-DO: have this take in the path to quickumls, don't iterate directly here (do sklearn style folder thing)
        ## make SNOMED things (qualifiers and negators), be an auto-run type deal, unless they something is passed
        ## use container just to hold fancy things
    ### ideally woudl alter this to handle other cuis

    ############### AUTO-NEGATION HANDLING ##################
    # if negation ==1:
    import os.path,json
    from extract_pertinent_terms import snomedNavigator,umlsNavigator,node

    if os.path.isfile('negation_mappings.json'):
        with open('negation_mappings.json') as fp:
            negation_mappings = json.load(fp)
    else:
        snowy = snomedNavigator(description_full_path=snomed_description_path, stated_relationship_path=snomed_relationship_path)
        snowy.get_concept_terms(concept_type='negation')
        snowy.make_snomed_umls_navigator(mrconso_path=mrconso_path)
        snowy.get_cui_mappings()
        cui_to_term_dict = {}
        for mapping in snowy.cui_mappings:
            cui_to_term_dict[mapping] = snowy.cui_mappings[mapping].term
        cui_to_term_dict['C1298908']='No' # allows for better regex searching
        with open('negation_mappings.json','wb') as negation_file:
            json.dump(cui_to_term_dict,negation_file)
        negation_mappings=cui_to_term_dict

    ################ AUTO-QUALIFIER HANDLING ###############
    if modifiers == 'qualifier_minimal':
        if os.path.isfile('qualifier_minimal_mappings.json'):
            with open('qualifier_minimal_mappings.json') as fp:
                qualifier_mappings = json.load(fp)
        else:
            snowy = snomedNavigator(description_full_path=snomed_description_path, stated_relationship_path=snomed_relationship_path)
            snowy.get_concept_terms(concept_type='qualifier_minimal')
            snowy.make_snomed_umls_navigator(mrconso_path=mrconso_path)
            snowy.get_cui_mappings()
            cui_to_term_dict={}
            for mapping in snowy.cui_mappings:
                cui_to_term_dict[mapping] = snowy.cui_mappings[mapping].term
            with open('qualifier_minimal_mappings.json','wb') as modifier_file:
                json.dump(cui_to_term_dict,modifier_file)
            qualifier_mappings = cui_to_term_dict

    elif modifiers == 'qualifier':
        if os.path.isfile('qualifier_mappings.json'):
            with open('qualifier_mappings.json','wb') as fp:
                qualifier_mappings = json.load(fp)
        else:
            snowy = snomedNavigator(description_full_path=snomed_description_path,
                                    stated_relationship_path=snomed_relationship_path)
            snowy.get_concept_terms(concept_type='qualifier')
            snowy.make_snomed_umls_navigator(mrconso_path=mrconso_path)
            snowy.get_cui_mappings()
            cui_to_term_dict = {}
            for mapping in snowy.cui_mappings:
                cui_to_term_dict[mapping] = snowy.cui_mappings[mapping].term
            with open('qualifier_mappings.json') as modifier_file:
                json.dump(cui_to_term_dict, modifier_file)
            qualifier_mappings = cui_to_term_dict

    ##########################################################




    ### AUTO QUALIFIER HANDLING ####
    from QuickUMLS.quickumls import QuickUMLS

    quickumls_fp = '/usr/local/lib/python2.7/dist-packages/QuickUMLS/quickUMLS-install'
    matcher = QuickUMLS(quickumls_fp=quickumls_fp, overlapping_criteria='length', threshold=.7,
                        similarity_name='cosine')


    thisFile = list(csv.reader(open(full_input_path, 'rU'), delimiter=','))
    file_text = thisFile[0][-1]
    file_labels=thisFile[0][:-1]
    file_label_string=','.join(file_labels)
    annotation_offset= len(file_label_string)+2 #+2 accounts for " and \n after labels

    ### 1. RUN QUICK UMLS ON FILE ####
    found_entities,parsed_doc = matcher.match(text=file_text, best_match=True, ignore_syntax=False)
    for found_entity in found_entities:
        while type(found_entity)==list:
            found_entity = found_entity[0]
        found_entity['end'] += annotation_offset
        found_entity['start'] += annotation_offset

    # for entity in found_entities:
    #     print entity
    subject_entities = []
    negation_entities = []
    qualifier_entities = []
    ancestor_mappings={}
    from util import merge_dicts
    # for concept_type in container.concept_type:
    # for cui_container in container:

    #### FIND SUBJECT CUIS #########
    for concept_type in container.concept_type:
        if len(ancestor_mappings)>0:
            ancestor_mappings=merge_dicts(ancestor_mappings,container.ancestor_mappings[concept_type])
        else:
            ancestor_mappings=container.ancestor_mappings[concept_type]

        subject_cuis=container.subject_cuis[concept_type]
        for findings in found_entities:
            while type(findings) ==list:
                findings = findings [0] ###navigates down to the best finding

        ### 2. Compare CUIs to CUI tree ####
            ## TO - DO - add in complication and such (custom job)

            if findings['cui'] in subject_cuis:
                subject_entities.append(findings)
                if 'concept_type' not in findings:
                    findings['concept_type'] = concept_type

            if findings['cui'] in qualifier_mappings:
                qualifier_entities.append(findings)
                if 'concept_type' not in findings:
                    findings['concept_type'] = 'qualifier'

            if findings['cui'] in negation_mappings:
                if findings['similarity']>.9 :## accounts for similarity between negation and non-negation
                    negation_entities.append(findings)
                if 'concept_type' not in findings:
                    findings['concept_type'] = 'negation'


        if container.cui_to_morphological_variants_dic[concept_type]:
            regex_subject_findings=regex_matcher(parsed_doc=parsed_doc,cui_to_morphological_variants_dic=container.cui_to_morphological_variants_dic[concept_type],
                          annotation_offset=annotation_offset)
        else:
            regex_subject_findings=None
        if regex_subject_findings:
            for finding in regex_subject_findings:
                finding['concept_type']=concept_type
            subject_entities+=regex_subject_findings

    regex_negation_finding = regex_matcher(parsed_doc=parsed_doc,cui_to_morphological_variants_dic=negation_mappings,annotation_offset=annotation_offset)
    negation_entities+= regex_negation_finding
    # regex_qualifier_findings = regex_matcher(parsed_doc=parsed_doc,cui_to_morphological_variants_dic=qualifier_mappings,annotation_offset=annotation_offset)
    # qualifier_entities+=regex_qualifier_findings

    ##### THROW IN QUALIFIER AND NEGATION WITH PRIORITY VALUES HERE #######

    # for finding in subject_entities:
    #     # finding['concept_type']= 'subject'
    #     finding['priority'] = 1
    # for finding in negation_entities:
    #     finding['concept_type'] = 'negation'
    #     finding['priority'] = 2
    # for finding in qualifier_entities:
    #     finding['concept_type'] = 'qualifier'
    #     finding['priority'] = 2
    from operator import itemgetter
    for finding in subject_entities:
        finding['priority']=1
    for finding in negation_entities:
        finding['priority']=2
        finding['concept_type']='negation'
    for finding in qualifier_entities:
        finding['priority']=2
        finding['concept_type']='qualifier'
    all_findings = subject_entities + negation_entities + qualifier_entities



    all_findings = removeOverlappingPhrases(all_findings)
    relevant_findings=[]
    all_findings.sort(key=itemgetter('priority', 'sentence'))
    count=1

    #### WEED OUT UNNECESSARY TERMS. MAKE KEY VALUE OBJECTS ####
    from keyValue import keyValue
    key_value_dic={}
    relevant_sentences = []
    # print 'ALL FINDINGS BELOW:'
    # print all_findings
    for finding in all_findings:
        count+=1
        if finding['priority']==1:
            relevant_findings.append(finding)
            this_sentence=finding['sentence']
            relevant_sentences.append(this_sentence)
            if ancestor_mappings != 0:
                this_kv=keyValue(concept_type=finding['concept_type'],mapped_term=ancestor_mappings[finding['cui']],concept=finding['cui'],source_document_path=full_input_path,concept_related_terms={'cui':finding['cui'],'ngram':finding['ngram'],'start':finding['start']+note_offset,'end':finding['end']+note_offset},sentence=this_sentence)
            else:
                this_kv=keyValue(concept_type=finding['concept_type'],mapped_term=finding['concept_type'],concept=finding['cui'],source_document_path=full_input_path,concept_related_terms={'cui':finding['cui'],'ngram':finding['ngram'],'start':finding['start']+note_offset,'end':finding['end']+note_offset},sentence=this_sentence)

            if this_sentence in key_value_dic:
                current_kvs=key_value_dic[this_sentence]
                current_kvs.append(this_kv)
                key_value_dic[this_sentence]=current_kvs
            else:
                key_value_dic[this_sentence]=[this_kv]
        ### currently done crudely (add negation/qualifer to ALL subjects. Could leverage spacy dependencies) ###
        elif finding['priority'] !=1:
            this_sentence = finding['sentence']
            if this_sentence in relevant_sentences:
                relevant_findings.append(finding)
                if finding['concept_type'] == 'qualifier':
                    for kv in key_value_dic[this_sentence]:
                        kv.modifiers={'cui':finding['cui'],'ngram':finding['ngram'],'start':finding['start']+note_offset,'end':finding['end']+note_offset}

                elif finding['concept_type'] == 'negation':
                    for kv in key_value_dic[this_sentence]:
                        kv.negation={'cui':finding['cui'],'ngram':finding['ngram'],'start':finding['start']+note_offset,'end':finding['end']+note_offset}

    ##############################################################
    kv_list=[]
    for sentence in key_value_dic:
        for kv in key_value_dic[sentence]:
            kv_list.append(kv)
    return kv_list

#TO-DO: ****************************************************************************************************************
    # - TRY TO DO A .FTR OUTPUT WITH MAPPING BACK, AND ONE WITHOUT
    # - Look into dependency mapping in spacy for qualifiers/negation
    # - Look into redoing QuickUMLS ngram generator with spacy (current strucutre misses negaiton)





def make_brat_annotations(kv_list):
    brat_formatted_finding_list=[] #holds findings after transformed into brat format
    finding_list=[]
    txt_path = kv_list[0].source_document_path
    ann_path=txt_path[:-3]+'ann'
    for kv in kv_list:
        mapped_term = kv.mapped_term
        concept_ngram=kv.concept_related_terms['ngram']
        start = kv.concept_related_terms['start']
        stop = kv.concept_related_terms['end']
        # (concept_ngram,start,stop)=kv.concept_related_terms
        concept_brat=(mapped_term,kv.concept_related_terms['start'],kv.concept_related_terms['end'],kv.concept_related_terms['ngram'])
        finding_list.append(concept_brat)
        if kv.negation:
            for negator in kv.negation:
                this_negator=('negation',negator['start'],negator['end'],negator['ngram'])
                if negator not in finding_list:
                    finding_list.append(this_negator)
        if kv.modifiers:
            for modifier in kv.modifiers:
                this_modifier=('modifiers',modifier['start'],modifier['end'],modifier['ngram'])
                if this_modifier not in finding_list:
                    finding_list.append(this_modifier)
    from operator import itemgetter
    finding_list=set(finding_list)
    finding_list=sorted(finding_list,key=itemgetter(1))
    i=0
    with open(ann_path,'w') as fp:
        for annotation in finding_list:
            i+=1
            term_count='T'+str(i)
            annotation_type = annotation[0]
            annotation_type=annotation_type.replace(' ','_') ##brat will break on spaces
            start= annotation[1]
            stop = annotation[2]
            ngram=annotation[3]
            brat_formatted_finding = term_count+'\t'+annotation_type+' '+str(start)+' '+str(stop)+'\t'+ngram+'\n'
            fp.write(brat_formatted_finding)


#################################### Making Mappings #######################################
# from extract_pertinent_terms import umlsNavigator,snomedNavigator,node
# mrrel_path = '/usr/share/2017AB-full/2017AB/META/MRREL.RRF'
# mrconso_path = '/usr/share/2017AB-full/2017AB/META/MRCONSO.RRF'
# locations = ['ileum','duodenum','jejunum','ascending colon','transverse colon','descending colon','sigmoid colon','rectum','stomach','esophagus']
# umls_anatomy_nav=umlsNavigator(mrconso_path=mrconso_path,mrrel_path=mrrel_path,concept_type='anatomy',target_terms=locations)
# term_and_cui=umls_anatomy_nav.term_to_cui('Gastrointestinal tract')
# subject_cui=term_and_cui[0]
# umls_anatomy_nav.get_related_cuis(subject_cui=subject_cui)
# cui_to_ancestor_dic = make_ancestry_mappings(umls_anatomy_nav)
# umls_anatomy_nav.find_target_morphological_variants()
# print umls_anatomy_nav.target_morphological_variants
# print cui_to_ancestor_dic

# umls_surgery_nav=umlsNavigator(mrconso_path=mrconso_path,mrrel_path=mrrel_path,concept_type='surgery')
# term_and_cui=umls_surgery_nav.term_to_cui('Surgery')
# subject_cui=term_and_cui[0]
# umls_surgery_nav.get_related_cuis(subject_cui=subject_cui)
# print umls_surgery_nav.concept_network_dictionary
##############################################################################################

###### Easy Call ######
#UMLS
## target_mappings - DONE
## get synonyms  - DONE
## ancestor mappings to target - DONE

#SNOMED
## easy call term type - DONE
## map to UMLS cuis  - DONE
## build in morphological variant dic - DONE


#BOTH
## make 'fill container' method - DONE
## chanage containers to get rid of negation part and just make it's own containers with names (or change cuis to dics of dics) - DONE
## make quick call from here - To do


###################### TEST OF SIMPLE CODE / DEBUG ###################
# from extract_pertinent_terms import umlsNavigator,snomedNavigator,cuiContainer,node
# from util import save_object,load_object
#
# ibd_containerr=load_object('ibd-container.pkl')
#
# mrrel_path = '/usr/share/2017AB-full/2017AB/META/MRREL.RRF'
# mrconso_path = '/usr/share/2017AB-full/2017AB/META/MRCONSO.RRF'
# description_path='/home/john/Downloads/SnomedCT_USEditionRF2_PRODUCTION_20180301T183000Z/Full/Terminology/sct2_Description_Full-en_US1000124_20180301.txt'
# relationship_path ='/home/john/Downloads/SnomedCT_USEditionRF2_PRODUCTION_20180301T183000Z/Full/Terminology/sct2_StatedRelationship_Full_US1000124_20180301.txt'
# do_quickumls(container=ibd_containerr,full_input_path='/home/john/Desktop/nlp_work/test-annotations/20-classified.txt',snomed_description_path=description_path,snomed_relationship_path=relationship_path,mrconso_path=mrconso_path)


##############################END################################


################## PREPARE SUBJECT CUI CONTAINERS ####################################
# ## Build the initial anatomy navigator object
# mrrel_path = '/usr/share/2017AB-full/2017AB/META/MRREL.RRF'
# mrconso_path = '/usr/share/2017AB-full/2017AB/META/MRCONSO.RRF'
#
# ## Anatomy ##
# locations=['ileum','duodenum','jejunum','ascending colon','transverse colon','descending colon','sigmoid colon','rectum','stomach','esophagus']
# anatomy_nav=umlsNavigator(mrconso_path=mrconso_path,mrrel_path=mrrel_path,concept_type='anatomy',target_terms=locations)
# anatomy_parent_cui = anatomy_nav.term_to_cui('Gastrointestinal tract')[0]
# anatomy_nav.get_related_cuis(subject_cui=anatomy_parent_cui)
#
# ## Surgery ##
# surgery_nav = umlsNavigator(mrconso_path=mrconso_path,mrrel_path=mrrel_path,concept_type='surgery',target_terms=['Surgery'])
# surgery_parent_term= surgery_nav.term_to_cui('Surgery')[0]
# surgery_nav.get_related_cuis(subject_cui=surgery_parent_term)
#
# ## Complications ##
# complications=["perianal fistula","abscess", "pouch","enteroenteric fistula", "perianal abscess", "fistula","distention"]
# complications_nav=umlsNavigator(mrconso_path=mrconso_path,mrrel_path=mrrel_path,ontologies='SNOMEDCT_US',target_terms=complications)
#
# ## Pour Containers ##
# cui_container=anatomy_nav.pour_container(concept_type='anatomy')
# cui_container=surgery_nav.pour_container(concept_type='surgery',cui_container=cui_container)
# cui_container=complications_nav.pour_container(concept_type='complications',cui_container=cui_container)
# save_object(obj=cui_container,filename='ibd-container.pkl')

########################END####################################3

# from extract_pertinent_terms import umlsNavigator,snomedNavigator,cuiContainer,node
from util import save_object,load_object
ibd_containerr=load_object('ibd-container.pkl')
mrrel_path = '/usr/share/2017AB-full/2017AB/META/MRREL.RRF'
mrconso_path = '/usr/share/2017AB-full/2017AB/META/MRCONSO.RRF'
description_path='/home/john/Downloads/SnomedCT_USEditionRF2_PRODUCTION_20180301T183000Z/Full/Terminology/sct2_Description_Full-en_US1000124_20180301.txt'
relationship_path ='/home/john/Downloads/SnomedCT_USEditionRF2_PRODUCTION_20180301T183000Z/Full/Terminology/sct2_StatedRelationship_Full_US1000124_20180301.txt'
from util import find_files_in_folder
note_paths=find_files_in_folder(directory='/home/john/Desktop/brat-v1.3_Crunchy_Frog/data/new-method-annotations/',extension='.txt')
i=-1
fp_kv_dict={}
read_lines=[]
with open('completed_files.txt', 'r') as f:
    for line in f:
        read_lines.append(line.strip('\n'))
read_lines=set(read_lines)
### run on all notes ###
for path in note_paths:
    if path in read_lines:continue
    key_values=do_quickumls(container=ibd_containerr,
                 full_input_path=path,
                 snomed_description_path=description_path, snomed_relationship_path=relationship_path,
                 mrconso_path=mrconso_path)
    fp_kv_dict[path]=key_values
    if key_values:
        make_brat_annotations(key_values)
    with open('completed_files.txt','a') as completed_record:
        completed_record.write(path+'\n')
save_object(fp_kv_dict,'file_kvs.pkl')



from keyValue import keyValue
# fp_kv_dict=load_object('file_kvs.pkl')
# print fp_kv_dict
# for path in fp_kv_dict:
#     for kv in fp_kv_dict[path]:
#         print '******************************START***********************************'
#         print 'concept type',kv.concept_type
#         print 'concept terms',kv.concept_related_terms
#         print 'mapped terms =',kv.mapped_term
#         print 'negation',kv.negation
#         print 'activity terms',kv.activity_terms
#         print 'modifiers',kv.modifiers

################################## STOP SAMPLE CODE ###################################



#################### HOW TO MODIFY THE FTR CREATOR ?? #######
### USE KVS
### GROUP THINGS MATRICES BY CONCEPT TYPE
### MAP TO NEGATORS & MODIFIERS (ALL PERMUTATIONS)
### NO CONCEPT, CONCEPT TYPE X
### MODIFIER A ONLY, NEGATION A ONLY, NEGATION + MODIFIER
### ONLY REPRESENT WHAT IS SEEN


### NEGATION, NEGATION + MODIFIER, MODIFIER
### IF NEGATION + MODIFIER IN LIST, ADD 1 THERE
### ELSE: ADD 1 AT END, AND ADD 0 TO END OF ALL OTHER FINDINGS

######### STEPS FOR FTR CREATOR USING ABOVE PRINCIPLES ###########
#1. GO THROUGH KV's and make dictionary (cui to index) of all present concepts, modifiers, and negations
    ## sort mapping by cui/alphabetically (depending on term or cui) for each type, so the same matrix will be generated each time
#2. Make an interpreter of term to cuis (for use in human interpretation) [or just used preferred term?]
#3. Go back through and map each of the findings to the appropriate locale
