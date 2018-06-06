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
complicationDic={} #list of complication phrases mapped to specific terms
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
        fullInputPath=folderPath+str(number)+"-classified.txt"
        thisFile=list(csv.reader(open(fullInputPath, 'rU'), delimiter=','))
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

class umlsContainer(object):
    def __init__(self,cui_to_morphological_variants_dic=None,label_to_cui_dic=None,cui_network=None,target_cuis=None):
        self.cui_to_morphological_variants_dic = cui_to_morphological_variants_dic
        self.label_to_cui_dic = label_to_cui_dic
        self.cui_network= cui_network
        self.target_cuis = target_cuis


def make_quickumls_annotations(file_range):
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
    for sentence in sentences:
        sent_count+=1
        # print sentence
        sentence_offset= sentence[0].idx+annotation_offset
        sentence=str(sentence)
        for cui in cui_to_morphological_variants_dic:
            for variant in cui_to_morphological_variants_dic[cui]:
                # found_phrase = re.findall(r'([a-z\-A-Z]*?' + variant + '[a-zA-Z\-]*?)', str(sentence))
                found_phrase = re.findall(r'[^0-9a-zA-Z]*([A-Za-z\-]*' + variant + r'[A-Za-z\-]*)[^0-9a-zA-Z]*', str(sentence))
                ### expand phrase to caputure full word in which shorted term is found
                if found_phrase:
                    print 'FOUND SOMETHING'
                    print found_phrase
                    print sentence
                    phrase_and_index=[]
                    stop_index = 0
                    for phrase in found_phrase:
                        ###CONVERT THIS TO THE SPACY WAY
                        start_index = sentence[stop_index:].index(phrase)
                        stop_index = start_index + len(phrase)
                        phrase_and_index.append([cui,phrase, start_index + sentence_offset, stop_index + sentence_offset])
                        # print phraseAndIndex
                    print phrase_and_index

# def do_quickumls(umls_obj,cui_to_morphological_variants_dic,label_to_cui_dic,cui_network):
def do_quickumls(umls_container):
    from QuickUMLS.quickumls import QuickUMLS

    quickumls_fp = '/usr/local/lib/python2.7/dist-packages/QuickUMLS/quickUMLS-install'
    matcher = QuickUMLS(quickumls_fp=quickumls_fp, overlapping_criteria='length', threshold=.7,
                        similarity_name='cosine')
    file_range=10
    fileNums = range(1,file_range)
    for number in fileNums:
        # if j !=21:
        #     j+=1
        #     continue
        # j += 1
        # if number != 27: continue ### visualize interesting doc
        # folderPath='/home/john/Desktop/brat-v1.3_Crunchy_Frog/data/rapid-annotated/'
        folderPath = '/home/john/Desktop/nlp_work/test-annotations/'
        fullInputPath = folderPath + str(number) + "-classified.txt"
        thisFile = list(csv.reader(open(fullInputPath, 'rU'), delimiter=','))
        file_text = thisFile[0][21]

        ### 1. RUN QUICK UMLS ON FILE ####
        found_entities,parsed_doc = matcher.match(text=file_text, best_match=True, ignore_syntax=False)
        anatomical_entities = []
        for findings in found_entities:
            while type(findings) ==list:
                findings = findings [0]

        ### 2. Compare CUIs to CUI tree ####
            ## TO - DO - add in complication and such (custom job)
            target_cuis = [cui for cui in umls_container.cui_network]
            if findings['cui'] in target_cuis:
                anatomical_entities.append(findings)
        print anatomical_entities
        # for sentence in parsed_doc:
        #     print "SENT"
        #     print sentence
        print fullInputPath
        regex_matcher(parsed_doc=parsed_doc,cui_to_morphological_variants_dic=umls_container.cui_to_morphological_variants_dic,
                      annotation_offset=288)

        ### 2.5. Make key-value obejcts

        ####### WORKS TO HERE ############
        ### 3.0 - do regex
        #regex_call()
        ### 3. map back up to high term ####
            ### TRY TO DO A .FTR OUTPUT WITH MAPPING BACK, AND ONE WITHOUT

        ### 3.5 HANDLE NEGATIONS AND CONDITIONAL STATEMENTS
        ### 3.8 WORK ON QUALIFIERS AND SUCH
            ### BOTH OF THESE SHOULD WORK WITH CURRENT STRUCTURE, BUT NEED TO FIGURE OUT HOW TO AVOID OVER ANNOTAITON
                # HACK COULD BE LOOKING THROUGH CHARACTER OFFSETS OF LESS THAN ~50
                # REAL WORK COULD BE DONE WITH ALTERING QUICKUMLS
                # COULD GET REALLY FANCY WITH DEPENDENCIES

        ### 4. make annotations ####





#
# umls_obj, cui_to_morphological_variants_dic, label_to_cui_dic, cui_network = make_quickumls_annotations(10)
# umls_container=umlsContainer(cui_to_morphological_variants_dic=cui_to_morphological_variants_dic,label_to_cui_dic=label_to_cui_dic,cui_network=cui_network,target_cuis=[cui for cui in cui_network])
# cui_network={'a':2,1:'b'}
# umls_container=umlsContainer(cui_to_morphological_variants_dic=5,label_to_cui_dic=4,cui_network=3,target_cuis=[cui for cui in cui_network])

import util
# util.save_object(umls_container,'umls-container.pkl')
umls_container = util.load_object('umls-container.pkl')
do_quickumls(umls_container)

########QUICKUMLS STUFF #################
# from QuickUMLS.quickumls import QuickUMLS
# quickumls_fp='/usr/local/lib/python2.7/dist-packages/QuickUMLS/quickUMLS-install'
# #matcher= QuickUMLS(quickumls_fp,overlapping_criteria,threshold,similarity_name,window,accepted_semtypes)
# matcher= QuickUMLS(quickumls_fp=quickumls_fp,overlapping_criteria='length',threshold=.7,similarity_name='cosine')
#
# text = 'wall thickening of left colon'
# filePath= '/home/john/Desktop/brat-v1.3_Crunchy_Frog/data/rapid-annotated/21-classified.txt'
# def openFileAsString(path): ### COULD PROBABLY MAKE THIS JUMP FORWARD X CHARACTERS TO START
#     with open(path,'r') as myfile:
#         data=myfile.read()
#         return data
# text=openFileAsString(filePath)
# # text= 'My friend has done H a few times over the years. He will get enough for about a week then stop. Last week he got a fair amount. He said it looks like the stuff he usually gets. Always a different source. He said this stuff makes him super tired. He has tried snorting and shooting. He nods off after a few minutes. He said that is what is supposed to happen but he is staying tired afterwards. In the past, the H has given him a lot of energy to get his work done. He is very tired and almost depressed afterwards with this stuff. Any thoughts?'
# x,parsed_doc=matcher.match(text=text,best_match=True,ignore_syntax=False)
# # print x
# j=0
# for line in x:
#     print line
# line_lengths=[]
# for line in x:
#     while type(line)==list:  ##need this for implementation, otherwise get screwed by weird structuring
#         line = line[0]
#     print line['ngram']
#     print line['start']
#     print line['end']
#     print line['cui']
# print len(parsed_doc)
####QUICKUMLS CODE ABOVE###########################3333



##add simstring for approximate string matching (misspellings)
###extract dependenciees

# print annotation_obj.clinical_modifier_dic
# x= annotation_obj.access_specification
# for key in x:
#     # basestring= 'annotation_obj.'
#     # fullstring = basestring+key
#     # print eval(fullstring)
#     print key


####################IDEAS########################
###NOTE - snomed mapping in UMLS is FUCKED!!, so may need to manually curate qualifiers and negation terms
    ### could also try negex
#0 . look into making this all an annotation object, otherwise it's kinda wonky
#1. alter quickumls return to include a sentence, can use this to approximate activity and negation pertinence
#2. repeat similar approach to orginal (pass dependency type tree) -- think abotu changing structure
#3. make umlsContainer to hold stuff of interest that can be passed