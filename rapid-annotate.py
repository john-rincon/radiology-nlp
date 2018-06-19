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
annotation_offset=288
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
print inputFile

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
    def __init__(self,cui_to_morphological_variants_dic=None,label_to_cui_dic=None,cui_network=None,negation_cuis=None,qualifier_cuis=None,subject_cuis=None,container_type=None,ancestor_mappings=0):
        self.container_type=container_type
        self.cui_to_morphological_variants_dic = cui_to_morphological_variants_dic
        self.label_to_cui_dic = label_to_cui_dic
        self.cui_network= cui_network
        self.negation_cuis=negation_cuis
        self.qualifier_cuis=qualifier_cuis
        self.subject_cuis=subject_cuis
        self.ancestor_mappings=ancestor_mappings

        @property
        def ancestor_mappings(self):
            return self._ancestor_mappings

        @ancestor_mappings.setter
        def activity_terms(self, value):
            if self._ancestor_mappings:
                from util import merge_dicts
                self._ancestor_mappings = merge_dicts(self._ancestor_mappings,value)
            else:
                self._ancestor_mappings=value


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
            for variant in cui_to_morphological_variants_dic[cui]:
                # found_phrase = re.findall(r'([a-z\-A-Z]*?' + variant + '[a-zA-Z\-]*?)', str(sentence))
                if cui != 'C1298908':
                    found_phrase = re.findall(r'[^0-9a-zA-Z]*([A-Za-z\-]*' + variant + r'[A-Za-z\-]*)[^0-9a-zA-Z]*', str(sentence),flags=re.IGNORECASE)
                else: #special case for dealing with 'no'
                    found_phrase=re.findall(r'[\.\s]('+variant+r')[\.\s]',str(sentence),flags=re.IGNORECASE)
                ### expand phrase to caputure full word in which shorted term is found
                if found_phrase:
                    stop_index = 0
                    for phrase in found_phrase:
                        ###CONVERT THIS TO THE SPACY WAY
                        start_index = sentence[stop_index:].index(phrase)
                        stop_index = start_index + len(phrase)
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


def do_quickumls(containers,full_input_path,note_offset=0):
    ### TO-DO: have this take in the path to quickumls, don't iterate directly here (do spacy style folder thing)
    ### ideally woudl alter this to handle other cuis
    from QuickUMLS.quickumls import QuickUMLS

    quickumls_fp = '/usr/local/lib/python2.7/dist-packages/QuickUMLS/quickUMLS-install'
    matcher = QuickUMLS(quickumls_fp=quickumls_fp, overlapping_criteria='length', threshold=.7,
                        similarity_name='cosine')
    if type(containers) is not list:
        containers=[containers]

    thisFile = list(csv.reader(open(full_input_path, 'rU'), delimiter=','))
    file_text = thisFile[0][-1]
    file_labels=thisFile[0][:-1]
    file_label_string=','.join(file_labels)
    annotation_offset= len(file_label_string)+2 #+2 accounts for " and \n after labels

    ### 1. RUN QUICK UMLS ON FILE ####
    found_entities,parsed_doc = matcher.match(text=file_text, best_match=True, ignore_syntax=False)

    # for entity in found_entities:
    #     print entity
    subject_entities = []
    negation_entities = []
    qualifier_entities = []
    ancestor_mappings={}
    from util import merge_dicts
    for cui_container in containers:
        if cui_container.ancestor_mappings:
            if len(ancestor_mappings) > 0:
                ancestor_mappings = merge_dicts(ancestor_mappings,cui_container.ancestor_mappings)
            else:
                ancestor_mappings=cui_container.ancestor_mappings
        subject_cuis = cui_container.subject_cuis
        qualifier_cuis = cui_container.qualifier_cuis
        negation_cuis = cui_container.negation_cuis
        for findings in found_entities:
            while type(findings) ==list:
                findings = findings [0]

        ### 2. Compare CUIs to CUI tree ####
            ## TO - DO - add in complication and such (custom job)

            if findings['cui'] in subject_cuis:
                subject_entities.append(findings)
            elif findings['cui'] in negation_cuis and findings['similarity'] > .9: ## need higher similarity to avoid lots of false positives (e.g. inflammatory as negation for noninflammatory)
                negation_entities.append(findings)
            elif findings['cui'] in qualifier_cuis:
                qualifier_entities.append(findings)

        if cui_container.cui_to_morphological_variants_dic:
            regex_subject_findings=regex_matcher(parsed_doc=parsed_doc,cui_to_morphological_variants_dic=cui_container.cui_to_morphological_variants_dic,
                          annotation_offset=annotation_offset)
        else:
            regex_subject_findings=None
        if regex_subject_findings:
            subject_entities+=regex_subject_findings
    regex_negation_finding = regex_matcher(parsed_doc=parsed_doc,cui_to_morphological_variants_dic={'C1298908':['No']},annotation_offset=annotation_offset)
    negation_entities+= regex_negation_finding

    for finding in subject_entities:
        finding['concept_type'] = 'subject'
        finding['priority'] = 1
    for finding in negation_entities:
        finding['concept_type'] = 'negation'
        finding['priority'] = 2
    for finding in qualifier_entities:
        finding['concept_type'] = 'qualifier'
        finding['priority'] = 2
    from operator import itemgetter
    all_findings = subject_entities + negation_entities + qualifier_entities

    all_findings = removeOverlappingPhrases(all_findings)
    relevant_findings=[]
    all_findings.sort(key=itemgetter('priority', 'sentence'))
    count=1

    #### WEED OUT UNNECESSARY TERMS. MAKE KEY VALUE OBJECTS ####
    from keyValue import keyValue
    key_value_dic={}
    relevant_sentences = []
    for finding in all_findings:
        count+=1
        if finding['priority']==1:
            relevant_findings.append(finding)
            this_sentence=finding['sentence']
            relevant_sentences.append(this_sentence)
            if ancestor_mappings != 0:
                this_kv=keyValue(mapped_term=ancestor_mappings[finding['cui']],concept=finding['cui'],source_document_path=full_input_path,concept_related_terms={'ngram':finding['ngram'],'start':finding['start']+note_offset,'end':finding['end']+note_offset},sentence=this_sentence)
            else:
                this_kv=keyValue(mapped_term=finding['concept_type'],concept=finding['cui'],source_document_path=full_input_path,concept_related_terms={'ngram':finding['ngram'],'start':finding['start']+note_offset,'end':finding['end']+note_offset},sentence=this_sentence)

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
        (concept_ngram,start,stop)=kv.concept_related_terms
        concept_brat=[mapped_term,kv.concept_related_terms['start'],kv.concept_related_terms['end'],kv.concept_related_terms['ngram']]
        finding_list.append(concept_brat)
        if kv.negation:
            for negator in kv.negation:
                this_negator=['negation',negator['start'],negator['end'],negator['ngram']]
                if negator not in finding_list:
                    finding_list.append(this_negator)
        if kv.modifiers:
            for modifier in kv.modifiers:
                this_modifier=['modifiers',modifier['start'],modifier['end'],modifier['ngram']]
                if this_modifier not in finding_list:
                    finding_list.append(this_modifier)
    from operator import itemgetter
    finding_list=sorted(finding_list,key=itemgetter(1))
    i=0
    with open(ann_path,'w') as fp:
        for annotation in finding_list:
            i+=1
            term_count='T'+str(i)
            annotation_type = annotation[0]
            start= annotation[1]
            stop = annotation[2]
            ngram=annotation[3]
            brat_formatted_finding = term_count+'\t'+annotation_type+' '+str(start)+' '+str(stop)+' '+ngram+'\n'
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




########################## START RUN QUICKUMLS STYLE ANNOTATIONS ###############################
# import util
# import json
# with open('umls_container_json_input_examples/anatomy-mappings.json') as fp:
#     anatomy_mappings= json.load(fp)
# with open('umls_container_json_input_examples/negation_mappings.json') as fp:
#     negation_mappings= json.load(fp)
# with open('umls_container_json_input_examples/qualifier_mappings.json') as fp:
#     qualifier_mappings= json.load(fp)
# with open ('umls_container_json_input_examples/morphological_variant_mappings.json') as fp:
#     variant_mappings=json.load(fp)
# with open('umls_container_json_input_examples/surgery_mappings.json') as fp:
#     surgery_mappings=json.load(fp)
# with open ('umls_container_json_input_examples/surgical_suffixes.json') as fp:
#     surgical_variants = json.load(fp)
# with open ('umls_container_json_input_examples/complication_mappings.json') as fp:
#     complication_mappings=json.load(fp)
# with open('umls_container_json_input_examples/anatomy_ancestor_mapping.json') as fp:
#     anatomy_ancestor_mappings=json.load(fp)
# surgery_ancestors={}
#
# for cui in surgery_mappings:
#     surgery_ancestors[cui]='Surgery'
#
# complication_ancestors={}
# for cui in complication_mappings:
#     complication_ancestors[cui]=complication_mappings[cui][0]
#
# anatomy_cui_container= cuiContainer(ancestor_mappings=anatomy_ancestor_mappings,container_type='anatomy',cui_to_morphological_variants_dic=variant_mappings,negation_cuis=[cui for cui in negation_mappings],qualifier_cuis=[cui for cui in qualifier_mappings], subject_cuis=[cui for cui in anatomy_mappings])
# surgical_cui_container= cuiContainer(ancestor_mappings=surgery_ancestors,container_type='surgery',cui_to_morphological_variants_dic=surgical_variants,negation_cuis=[cui for cui in negation_mappings],qualifier_cuis=[cui for cui in qualifier_mappings], subject_cuis=[cui for cui in surgery_mappings])
# complication_cui_container = cuiContainer(ancestor_mappings=complication_ancestors,container_type='complications',cui_to_morphological_variants_dic=None,negation_cuis=[cui for cui in negation_mappings],qualifier_cuis=[cui for cui in qualifier_mappings], subject_cuis=[cui for cui in complication_mappings])
#
# fileNums = range(2500)
# for number in fileNums:
#     folderPath = '/home/john/Desktop/nlp_work/test-annotations/'
#     full_input_path = folderPath + str(number) + "-classified.txt"
#     key_values = do_quickumls(containers=[anatomy_cui_container,surgical_cui_container,complication_cui_container],full_input_path=full_input_path)
#     make_brat_annotations(key_values)
################################## STOP SAMPLE CODE ###################################

