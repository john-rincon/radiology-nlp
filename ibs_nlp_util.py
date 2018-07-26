def findPhraseAndIndex(phrase,inputText,annotation_offset):
    ###########FINDS index of phrase within a doc############

    import re
    foundPhrase = re.findall(r'[^0-9a-zA-Z]*([A-Za-z\-]*'+phrase+r'[A-Za-z\-]*)[^0-9a-zA-Z]*', inputText)
    phraseAndIndex=[]
    if foundPhrase:
        # print foundPhrase
        stopIndex=0
        for phrase in foundPhrase:
            ###CONVERT THIS TO THE SPACY WAY
            startIndex=inputText[stopIndex:].index(phrase)
            stopIndex=startIndex+len(phrase)
            phraseAndIndex.append([phrase,startIndex+annotation_offset,stopIndex+annotation_offset])
            # print phraseAndIndex

    return phraseAndIndex[0] ##returns [phrase,startInex,stopIndex]

def get_object_attributes(input_object):
    activity_terms= input_object.activity_terms
    if activity_terms:
        if type(activity_terms[0]) != list:
            activity_terms=[activity_terms]
        for activity in activity_terms:
            activity.insert(0,'activity-terms')
    else:
        activity_terms=[]

    negation = input_object.negation
    if negation:
        if type(negation[0]) !=list:
            negation=[negation]
        for negator in negation:
            negator.insert(0,'negation')
    else:
        negation=[]
    concept_type_and_terms = input_object.concept_related_terms
    if concept_type_and_terms:
        concept_type_and_terms.insert(0,input_object.concept)
    else: concept_type_and_terms = None

    annotation_list=[]
    annotation_list+=negation
    annotation_list+= activity_terms
    if concept_type_and_terms: annotation_list+=[concept_type_and_terms]

    return annotation_list



###EITHER RETURNS NONE AND UPDATES INPUT OBJECT, OR COPIES OBJECT WHEN THERE ARE MULTIPLE SIMILAR THINGS
def copy_or_create_KV_concept(input_kv_pointer,this_concept,this_concept_type,this_phrase,sent,
                              annotation_offset,sent_count):
    kv_list=[]
    # print 'input-values'
    # print 'input phrase '+ this_phrase
    x=input_kv_pointer
    if type (input_kv_pointer) != list:
        x=[input_kv_pointer]
    # for item in x:
    #     print item.concept_related_terms
    ###Pretty sure this method is causing the issues
    ### see if there is already a concept there
    ###make a new one
    # get_object_attributes(input_kv)
    import copy
    from keyValue import keyValue
    forced_list=0
    if type(input_kv_pointer) != list:
        input_kv_pointer=[input_kv_pointer]
        forced_list=1
    last_item=[input_kv_pointer[-1]]
    for input_kv in last_item:
        ####OUTCOMES####
        #1. Make new object when appropriate
        #2. Copy when appropriate
        #3.
        indexed_phrase = findPhraseAndIndex(this_phrase, str(sent), annotation_offset)
        if input_kv == None: print "SHIT"
        if this_concept_type =='complication':
            if input_kv.concept_type == '' and input_kv.activity_terms == '': ##if empty object, add complication
                input_kv.concept = this_concept
                input_kv.concept_type = this_concept_type
                input_kv.concept_related_terms = indexed_phrase
                return
            else: ###make new object, but don't mess with old
                this_kv=keyValue(sentence=sent_count)
        ###different locations may have the same location indicators, so need to keep them in sync, will also need them to
        ### somehow both track the changes....
        elif this_concept_type == 'location' and input_kv.concept_type == this_concept_type: ###see if they're both locations
            this_kv=copy.deepcopy(input_kv)  ##keep info about locations etc...
        elif this_concept_type == 'location' and input_kv.activity_terms !='':  ###if no previous location, alter in place
            input_kv.concept = this_concept
            input_kv.concept_type = this_concept_type
            input_kv.concept_related_terms = indexed_phrase
            return
        ###if previous was location/complication, and this is opposite, just make a new object
        else:  ##if a new complication, or different type
            this_kv = keyValue(sentence=sent_count)
        this_kv.concept=this_concept
        this_kv.concept_type=this_concept_type
        this_kv.concept_related_terms=indexed_phrase
        # print "NEW KV**"
        # get_object_attributes(this_kv)
        if this_kv != None:
         kv_list.append(this_kv)
        # return this_kv
        ####
        ####Problem seems to be below here
        ####
    input_kv_pointer += kv_list
    if type(input_kv_pointer) !=list:
        input_kv_pointer=list(input_kv_pointer)
    # for this_object in input_kv_pointer:
    #     print this_object.concept_related_terms
    #     # print input_kv_pointer[0].concept_type
    #     # print input_kv_pointer[-1].concept_type
    # print input_kv_pointer


    return input_kv_pointer

def update_key_value(kv_object,concept_type,phrase,sent,annotation_offset):  ##update object values when no need to create new one
    # get_object_attributes(kv_object)
    if type(kv_object) == list:
        for kv in kv_object:
            indexed_phrase = findPhraseAndIndex(phrase, str(sent), annotation_offset)

            if concept_type == 'negator':
                kv.negation=indexed_phrase
            if kv.concept_type != 'complication':
                if concept_type =='modifier':
                    kv.modifiers=indexed_phrase
                if concept_type == 'activity':
                    kv.activity_terms=indexed_phrase
    else:
        indexed_phrase = findPhraseAndIndex(phrase, str(sent), annotation_offset)
        if concept_type == 'negator':
            kv_object.negation = indexed_phrase
        if kv_object.concept_type != 'complication':

            if concept_type == 'modifier':
                kv_object.modifiers = indexed_phrase
            elif concept_type == 'activity':
                kv_object.activity_terms = indexed_phrase
            # else: print "WTF!!!"

def parseFindPhraseAndIndex (document,annotation_obj,displayDeps=0):
# def parseFindPhraseAndIndex (document,annotationList,dependencyList=0,displayDeps=0):
    ############ parases doc, and finds phrases within sentence: ###################
    ############ used for context specific tasks where colocation is important #####
    annotation_offset=288 ###HARD-CODED OFFSET FOR RAD DOCS###
    import spacy
    import re
    document = unicode(document)
    nlp=spacy.load('en')
    doc=nlp(document)
    ####
    ###########THINK ABOUT MESSING WITH THIS TO FOCUS ON NOUN CHUNKS AT THIS POINT#######
    ##
    ###########show parse tree for debugging and tuning#############
    if displayDeps !=0:
        from spacy import displacy
        options={'compact': True, 'bg': '#09a3d5',
               'color': 'white', 'font': 'Source Sans Pro'}
        displacy.serve(doc, style='dep',options=options)

    sents=list(doc.sents)
    termsFoundList=[] ##holds all terms found
    startIndices=[]
    firstCount=0
    from keyValue import keyValue
    pertinentSentence=[0]*len(sents) ###tracks whether there was a key hit at a sentence, and if so, what they key(s) were
    indexed_key_value_list=[0]*len(sents) ###holds key value objects indexed to the sentence in which they were found
    KVList = [0] * len(sents)
    ###flip this with sentences
    sentCount=0
    findingDic={}
    annotation_order = annotation_obj.access_specification
    for sent in sents:### broke when flipped order of sentences and everything else
        listCounter=0
        sent_index = sent[0].idx
        full_offset = sent_index + annotation_offset

        ### TO -DO #####
        ###1.Figure out how to parse thing in spacy to add dependencies etc...
        ###1.1 Look into creating a simstring matcher dictionary for locations, I think this could be really helpful
        ###1.5 Parse and search within noun chunks themselves
        ###2. Add word/location found reference to 'pertinent index'
        ###3. Keep location search first, but don't actually pass on annotation unless location
            ###finding levels = no loaction, location, super location w/ activity, location w/ activity
        ###4. Perform searches by token rather than index

        activity_findings=[] #store all activity findings to add later
        modifier_findings=[] #store all modifiers to add later
        negation_findings=[] #store all negators to add later
        findingDic={} #sub dictionary of findings, could be used to create an object all at once at end?
        for list_name in annotation_order:
            basestring='annotation_obj.'
            fullstring=basestring+list_name
            thisList = eval(fullstring)
            thisListName = list_name
            thisFoundList = []   ###current list of found items
            if pertinentSentence[sentCount]==1 or annotation_order[list_name] == 0:
                # phrasesFound=[]   ###phrases that are found
                # startIndices.append(sent[0].idx)  ###sentence start index
                for key in thisList:
                    if thisListName == 'negation_list':  ###make sure you don't grab unpertinent no's
                        foundPhrase = re.findall(r'[^0-9a-zA-Z]('+key+r')[^0-9a-zA-Z]', str(sent)) #was old note about changing this, but seems unnecessary
                    else:
                        foundPhrase = re.findall(r'([a-z\-A-Z]*?'+key+'[a-zA-Z\-]*?)', str(sent))
                        ###TO-DO
                            #1. alter above to do an oppostie of negator search (i.e. return everything up to spaces or
                            ### punctuation to caputer full surgical or location words

                    if foundPhrase:
                        ##TO-Do:
                            #1. need to only make new objects at appropirate time, and to handle lists of objects
                        pertinentSentence[sentCount]=1
                        if indexed_key_value_list[sentCount] == 0 and annotation_order[list_name]==0:  #if no object here, make one
                            current_kv=keyValue(sentence=sentCount)
                            indexed_key_value_list[sentCount] = current_kv
                            # print('YOU ARE HERE*********** \n '+str(sentCount))

                        elif type(indexed_key_value_list[sentCount]) !=list and indexed_key_value_list[sentCount] !=0:
                            current_kv=indexed_key_value_list[sentCount]
                            indexed_key_value_list[sentCount]=current_kv

                        ### Below should never be triggered, but just in case
                        else:
                            # print "KVLIST"
                            current_kv = indexed_key_value_list[sentCount]
                            indexed_key_value_list[sentCount] = current_kv
                            # continue
#################################################

                           # # thisKVObject.
                        phrase_count=0  ##counter for how many phrases have been found in a given sentence
                        for phrase in foundPhrase:
                            if thisListName == 'location_dic':
                                this_concept = thisList[key]  ##maps back to concept type
                                this_phrase = phrase  ##maps to specific location
                                this_concept_type = 'location'  ##maps to list dictionary (concept type)

                                concept_KV=copy_or_create_KV_concept(current_kv,this_concept,this_concept_type,
                                                                     this_phrase,sent,full_offset,sentCount)
                                if concept_KV== None: continue #if function just updates, then no return
                                else:
                                    indexed_key_value_list[sentCount]=concept_KV


        #################ISSUES = CALLING THIS ON EMPTY OBJECT FOR SOME REASON ##############
                            #         'general_modifier_list':1,'location_dic':1,'negation_list':1,'complication_dic':0,'clinical_modifier_dic':0
                            if thisListName == 'clinical_modifier_dic' or thisListName=='general_modifier_list' or thisListName =='negation_list':
                                ##** CONVERT TO FORM USED IN FUNCTION **###
                                if thisListName == 'clinical_modifier_dic': name_to_pass='activity'
                                elif thisListName=='general_modifier_list': name_to_pass= 'modifier'
                                elif thisListName =='negation_list': name_to_pass='negator'
                                ###TO-DO
                                #####1.1 start with negex to try to do better with negations
                                #####1.2 use dependency parsing to get even better

                                update_key_value(current_kv,name_to_pass,phrase,sent,full_offset)
                            elif thisListName == 'complication_dic':
                                this_concept = thisList[key]  ##maps back to concept type
                                this_phrase = phrase  ##maps to specific location
                                this_concept_type = 'complication'  ##maps to list dictionary (concept type)
                                concept_KV = copy_or_create_KV_concept(current_kv, this_concept, this_concept_type,
                                                                          this_phrase,sent,full_offset,sentCount)
                                # print concept_KV
                                if concept_KV == None:
                                    continue
                                else:
                                    indexed_key_value_list[sentCount] = concept_KV

                            ###Check is key exists in dictionary
                            ####DOES THIS TO ANYTHING ANYMORE?????
                            if findingDic.get(thisListName):
                                if type(findingDic[thisListName]) == list:
                                    dicList=findingDic[thisListName]
                                    dicList.append(phrase)
                                    findingDic[thisListName]=dicList
                                else:
                                    dicList=[findingDic[thisListName]]
                                    dicList.append(phrase)
                                    findingDic[thisListName]=dicList
                            else:
                                findingDic[thisListName]=phrase
                            ####MAY NOT NEED ANYMORE??????

                            phrase_count+=1
                if thisFoundList:
                    thisFoundList=removeOverlappingPhrases(thisFoundList)
                    if type(thisFoundList[0])== list:
                        for item in thisFoundList: termsFoundList.append(item)
                    else:
                        termsFoundList.append(thisFoundList)
            ################split above into separate method ##################################

            listCounter += 1
        sentCount+=1
    return termsFoundList,indexed_key_value_list

def removeOverlappingPhrases(foundList):
    ####functions checks if one phrase is subsumed by other, to avoid double annotation
    # print 'FOUNDLIST'
    lastStartIndex=0
    lastStopIndex=0
    counter=0
    last_item=0
    from operator import itemgetter
    # foundList.sort(key=itemgetter(-2,-1))
    import json
    json_list=[]
    for line in foundList:
        if 'semtypes' in line:
            line['semtypes']=list(line['semtypes'])
    for line in foundList:
        json_version=json.dumps(line,sort_keys=True)
        json_list.append(json_version)
    json_list=set(json_list)
    foundList=[]
    for line in json_list:
        foundList.append(json.loads(line))
    foundList.sort(key=itemgetter('start','end'))
    # for item in foundList: print item #prints findings
    # print foundList
    for item in foundList:
        current_item=item
        if current_item == last_item:
            foundList.remove(current_item)
            print 'REMOVED'
            continue
        starting_list_length=len(foundList)
        thisStartIndex=item['start']
        thisStopIndex=item['end']
        # if thisStartIndex <= lastStopIndex and thisStopIndex<=lastStopIndex and thisStartIndex >= lastStartIndex and counter !=0:
        if thisStartIndex==lastStartIndex and thisStopIndex==lastStartIndex:
            del foundList[counter]
        elif thisStartIndex <=lastStartIndex and thisStopIndex >=lastStartIndex:
            del foundList[counter-1]
        # elif lastStartIndex<= thisStopIndex and lastStopIndex<= thisStopIndex and counter !=0 and lastStartIndex >= thisStartIndex:
        elif lastStartIndex <= thisStartIndex and lastStopIndex >= thisStartIndex:
            del foundList[counter]
        ending_list_length=len(foundList)
        lastStartIndex=thisStartIndex
        lastStopIndex=thisStopIndex
        last_item=current_item
        if starting_list_length == ending_list_length:
            counter+=1
    if len(foundList)==1: foundList=[foundList[0]]
    return foundList

def convertToAnnotations(termList):
    termCounter=1
    term_string_list=[]
    for term in termList:
        term_string="T"+str(termCounter)+'\t'+term[-1]+' '+str(term[1])+' '+str(term[2])+'\t'+term[0]
        termCounter+=1
        term_string_list.append(term_string)
    return term_string_list

def openFileAsString(path):
    with open(path,'r') as myfile:
        data=myfile.read()