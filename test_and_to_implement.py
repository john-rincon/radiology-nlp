# # # # modifiers=[]
# # # # activityTerms=[]
# # # # locationTerms=[]
# # # # locationDic={} #figure out how to handle many terms. 'Higher' terms return a list?
# # # # complicationDic={} #list of complication phrases mapped to specific terms
# # # # complicationList=[] #list of complication related phrases
# # # #
# # # # negator=[]
# # # # headerDic={}
# # # # reverseHeaderDic={}
# # # #
# # # # negatorList=[]
# # # # modifiersList=[]
# # # # activityList=[]
# # # # complicationHeaders=['surgery', 'fistula', 'pouch', 'dilation', 'stricture', 'abscess']
# # # # locationHeaders=['ileum', 'duodenum', 'jejunum', 'ascending', 'transverse', 'descending', 'sigmoid', 'rectum', 'stomach', 'esophagus']
# # # #
# # # # def buildList(inputFile):
# # # #     x=0
# # # #     for line in inputFile:
# # # #         y=0
# # # #         if x==0:
# # # #             for word in line:  #makes dictionary header index
# # # #                 headerDic[y]=word.lower()
# # # #                 y+=1
# # # #         y=0
# # # #         for phrase in line:
# # # #             if len(phrase)>0:
# # # #                 thisHeading=headerDic[y]
# # # #                 if thisHeading in complicationHeaders:
# # # #                     complicationDic[phrase.lower()]=thisHeading
# # # #                 elif thisHeading in locationHeaders:
# # # #                     locationDic [phrase.lower()]=thisHeading
# # # #                     if phrase == 'surgical':
# # # #                         print y
# # # #                         print line
# # # #
# # # #                     # print phrase
# # # #                 elif thisHeading == 'negator':
# # # #                     negatorList.append(phrase.lower())
# # # #                 elif thisHeading == 'modifier':
# # # #                     modifiersList.append(phrase.lower())
# # # #                 elif thisHeading =='activity':
# # # #                     activityList.append(phrase.lower())
# # # #             y+=1
# # # #
# # # #         x += 1
# # # #     return [['location',locationDic],['activity',activityList],['complication',complicationDic],  ['modifier',modifiersList], ['negator',negatorList]]
# # # #
# # # #
# # # #
# # # # def fillSlots(input_list):
# # # #     slotDic={"negator":"null", "activity":"null", "modifier":"null", "location-ileum":"null",
# # # #              "location-duodenum":"null", "location-jejunum":"null", "location-ascending":"null",
# # # #              "location-transverse":"null", "location-descending":"null", "location-sigmoid":"null",
# # # #              "location-rectum":"null", "location-stomach":"null", "location-esophagus":"null",
# # # #              "complication-pouch":"null", "complication-fistula":"null", "complication-surgery":"null",
# # # #              "complication-abscess":"null", "complication-stricture":"null", "complication-dilation":"null"}
# # # #     keyList=[]
# # # #     for key in slotDic:
# # # #         keyList.append(key)
# # # #     for item in input_list:
# # # #         if item[-1] in keyList:
# # # #             if slotDic[item[-1]]=='null':
# # # #                 slotDic[item[-1]]=item[0]
# # # #                 print item[0]
# # # #             else:
# # # #                 print item[0]
# # # #                 slotDic[item[-1]]=slotDic[item[-1]]+","+item[0]
# # # #
# # # #     return slotDic
# # # #
# # # #
# # # # from NLTK_book.nlpUtil import *
# # # # import csv
# # # # folderPath = '/home/john/Desktop/brat-v1.3_Crunchy_Frog/data/rapid-annotated/1-classified.txt'
# # # # thisFile = list(csv.reader(open(folderPath, 'rU'), delimiter=','))
# # # # thisFile = thisFile[0][21]
# # # # inputPath='/home/john/Desktop/nlp_work/full-key-value.csv'
# # # # inputFile = list(csv.reader(open(inputPath, 'rU'), delimiter=','))
# # # # dependencyList=[0,0,0,1,1]
# # # # t=buildList(inputFile)
# # # # print t
# # # # foundList = parseFindPhraseAndIndex(thisFile, t, dependencyList)
# # # # print fillSlots(foundList)
# # #
# # #
# # # #####################################################
# # # ########### DISPLACY TEST CODE ##################
# # # ##################################################
# # import spacy
# # # from spacy import displacy
# #
# # nlp = spacy.load('en')
# # doc = nlp(u'This is bad. Fucking tests. The boy ran over the big house of shit. There is active inflammation and mesenteric vascular enhancement in the ileum and sigmoid, but there are no signs of IBD in the rectum.')
# # sents =list(doc.sents)
# # for sent in sents:
# #     print sent
# #     print sent[0].idx
# # # #
# # # # options={'compact': True, 'bg': '#09a3d5',
# # # #            'color': 'white', 'font': 'Source Sans Pro'}
# # # # displacy.serve(doc, style='dep',options=options)
# # #
# # # ################################################################
# # # ############ POS, DEPENDENCY, LOCATION TEST ###################
# # # import spacy
# # # from spacy.matcher import Matcher
# # # nlp = spacy.load('en')
# # # doc = nlp(u'There is active inflammation and mesenteric vascular enhancement in the ileum and sigmoid, but there are no signs of IBD in the rectum.')
# # # matcher=Matcher()
# # # matcher.add(
# # # for chunk in doc.noun_chunks:
# # #     print chunk
# # #     print chunk[1].text
# # #     print "ROOT - " + str(chunk.root)
# # #     print "head - " + str(chunk.root.head)
#
# # from annotate.keyValue import keyValue
# #
# # this=keyValue(sentence=8)
# # this=keyValue(fake=8)
# # from annotate.nlpUtil import get_object_attributes
# # def dump(obj):
# #   for attr in dir(obj):
# #     print("obj.%s = %r" % (attr, getattr(obj, attr)))
# #
# # dump(this)
# #
# # x='CUI,LANG,TS,LUI,STT,SUI,ISPREF,AUI,SAUI,SCUI,SDUI,SOURCE,TTY,CODE,STRING,SRL,SUPPRESS,CVF'
# #
# # x=x.split(',')
# # for line in x:
# #     print line+" TEXT, "
# # print ['?']*18
# # [?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?]
#
# import csv
# types={
# 'T023':  'Body Part, Organ, or Organ Component',
# 'T031':  'Body Substance',
# 'T060':  'Diagnostic Procedure',
# 'T047':  'Disease or Syndrome',
# 'T200':  'Clinical Drug',
# 'T203':  'Drug Delivery Device',
# 'T033':  'Finding',
# 'T184':  'Sign or Symptom',
# 'T034':  'Laboratory or Test Result',
# 'T037':  'Injury or Poisoning',
# 'T061':  'Therapeutic or Preventive Procedure',
# 'T048':  'Mental or Behavioral Dysfunction',
# 'T046':  'Pathologic Function',
# 'T121':  'Pharmacologic Substance',
# 'T201': 'Clinical Attribute'}
#
# locationHeaders=['ileum', 'duodenum', 'jejunum', 'ascending', 'transverse', 'descending', 'sigmoid', 'rectum', 'stomach', 'esophagus']
#
# def make_annotation_feature_array(complication_mapping,activity_mapping):
#     import json
#     path = '/home/john/Desktop/brat-v1.3_Crunchy_Frog/data/rapid-annotated/'
#     all_location_arrays=[]
#     all_complication_arrays=[]
#     for i in range(10):
#         this_path = path + str(i)+'-classified.ftr'
#         activity_indices_to_augment=[] ##list of indices to add +1 to in array for this file given found terms
#         location_findings=[0]*(len(activity_mapping)) # +1 is to save space for activity with no location
#         location_findings=[location_findings]*(len(locationHeaders)+1)
#         complication_findings = [0]*(len(complication_mapping))
#         with open(this_path,'rb') as input_file:
#             x=json.load(input_file)
#             for dic in x:
#                 found_location_indices=[] #what are the row indices of locations found
#                 found_complication_indices=[]
#                 negation_present=0
#                 location_present=0
#                 if 'negation' in dic: negation_present=1
#                 ###TO-DO:
#                     ### handle locations
#                     ### handle multiple for each line locations
#                     ### handle activities without locations
#                     ### build array of location location x activity index + complications indices
#                 if 'location' in dic:
#                     location_present=1
#                     if type(dic['location']) != list: dic['location']=[dic['location']]
#                     for location in dic['location']:
#                         found_location_indices.append(locationHeaders.index(location))
#                 if 'complication' in dic:
#                     if type(dic['complication'])!= list: dic['complication']=[dic['complication']]
#                     for term in dic['complication']:
#                         if negation_present==1:
#                             complication_findings[complication_mapping['negated-'+term]]+=1
#                             # complication_indices_to_augment.append(complication_mapping['negated-'+term])
#                         else:
#                             complication_findings[complication_mapping[term]]+=1
#
#                 if 'activity-terms' in dic:
#                     if type (dic['activity-terms']) != list: dic['activity-terms'] = [dic['activity-terms']]
#                     for term in dic['activity-terms']:
#                         if negation_present==1:
#                             # activity_indices_to_augment.append(activity_mapping['negated-'+term])
#                             activity_index=activity_mapping['negated-'+term]
#                         else:
#                             # activity_indices_to_augment.append(activity_mapping[term])
#                             activity_index=activity_mapping[term]
#                         if found_location_indices:
#                             for location_index in found_location_indices:
#                                 location_findings[location_index][activity_index]+=1
#                         else:   ###handles when you see activity without location
#                             location_findings[-1][activity_index]+=1
#         flat_location_findings = [item for sublist in location_findings for item in sublist]
#         all_location_arrays.append(flat_location_findings) #### all np location arrays
#         all_complication_arrays.append(complication_findings)  ### all np compliaction arrays
#         import numpy as np
#     print all_location_arrays
#     print all_location_arrays[0]
#     print all_complication_arrays
#     all_location_arrays= np.asarray(all_location_arrays)
#     return all_location_arrays
#
#
#
# def get_annotation_indices(annotation_reference_file):
#     input_file = list(csv.reader(open(annotation_reference_file, 'rU'), delimiter=','))
#     # print inputFile[0]
#     complication_index_dic = {}
#     activity_index_dic = {'none':0}
#     activity_indices=[]
#     header_line = input_file[0]
#     header_line=[item.lower() for item in header_line]
#     activity_indices.append(header_line.index('modifiers_inflammation_features'))
#     activity_indices.append(header_line.index('modifiers_stricture_features'))
#     activity_entry_number=1
#     for line in input_file[1:]:
#         j=0
#         for item in line:
#             if j in activity_indices and item and item not in activity_index_dic.keys():
#                 activity_index_dic[item]=activity_entry_number
#                 activity_entry_number+=1
#                 activity_index_dic['negated-'+item]=activity_entry_number
#                 activity_entry_number+=1
#             j+=1
#     from collections import OrderedDict
#     complicationHeaders=['surgery', 'fistula', 'pouch', 'dilation', 'stricture', 'abscess']
#
#     this = OrderedDict(sorted(activity_index_dic.items(),key=lambda t:t[1]))
#     complication_entry_number = 0
#     for item in input_file[0]:
#         if item.lower() in complicationHeaders:
#             complication_index_dic[item.lower()]=complication_entry_number
#             complication_entry_number+=1
#             complication_index_dic['negated-'+item.lower()]=complication_entry_number
#             complication_entry_number+=1
#     sorted_complication_index_idex= OrderedDict(sorted(complication_index_dic.items(),key=lambda t:t[1]))
#     sorted_activity_index_dic=OrderedDict(sorted(activity_index_dic.items(),key=lambda t:t[1]))
#     return sorted_activity_index_dic, sorted_complication_index_idex
# # print header_line.index()
# ####structure of array
# # location : [just location, negated location, location activity 1, negated location activity 1....]
# # complication: [just complication 1, negated compication 1....]
#
# #############MOVE All THIS TO BETTER FILE!!!!!!!!!!!!!!! ###################
# # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ##
# activities,complications=get_annotation_indices('/home/john/Desktop/nlp_work/full-key-value_stidham.csv')
# all_arrays=make_annotation_feature_array(complication_mapping=complications,activity_mapping=activities)
# print all_arrays
# print len(complications)
# print all_arrays.shape





import sklearn.datasets



############ MOVE TO MORE GENERAL CODE IMPLEMENTATION #######
#############################################################

def get_list_of_files(directory,extension=0):
    ###Inputs = directory and extension of interest
    if extension !=0:
        return list((f for f in listdir(directory) if f.endswith('.' + extension)))
    else:
        return list((f for f in listdir(directory)))

def collection_annotations_and_text(folder_path):
    ###Inputs = folder path to documents of interest. Assumes files in folder adhere to brat strucutre of each document
        ##      existing as its own .txt file
    import csv, os
    folder_path = '/home/john/Desktop/brat-v1.3_Crunchy_Frog/data/rapid-annotated/'
    extension='txt'
    list_of_file_names= get_list_of_files(directory=folder_path,extension=extension)
    annotation_list_of_dics=[]
    for file_name in list_of_file_names:
        file_path=folder_path + file_name
        annotated_file = list(csv.reader(open(file_path,'rb')))
        annotated_file = annotated_file[0]
        # print annotated_file
        annotation_dic={'file_name':file_name}
        for item in annotated_file[:-1]:
            item=item.split('=')
            annotation_dic[item[0]]=item[1]
            # print item
        annotation_dic['document_text']=annotated_file[-1]
        annotation_list_of_dics.append(annotation_dic)
    return annotation_list_of_dics

# from os import listdir
# directory='/home/john/Desktop/brat-v1.3_Crunchy_Frog/data/rapid-annotated/'
# extension='txt'


# x=collection_annotations_and_text(directory)

# class node(object):
#     def __init__(self):
#         self.name=None
#         self.node=[]
#         self.otherInfo = None
#         self.parent=None
#     def child(self,child):
#         "Gets a node by number"
#         return self.node[child]
#     def parent(self):
#         return self.prev
#     def goto(self,data):
#         "Gets the node by name"
#         for child in range(0,len(self.node)):
#             if(self.node[child].name==data):
#                 return self.node[child]
#     def add(self):
#         node1=node()
#         self.node.append(node1)
#         node1.parent=self
#         return node1

class node(object):
    def __init__(self):
        self.name=None
        self.node=[]
        self.term = None
        self.parent=None
    def child(self,child):
        "Gets a node by number"
        return self.node[child]
    def parent(self):
        return self.prev

    def goto(self,data):
        "Gets the node by name"
        for child in range(0,len(self.node)):
            if(self.node[child].name==data):
                return self.node[child]
    def add(self):
        node1=node()
        self.node.append(node1)
        node1.parent=self
        return node1
#
tree=node()
root=tree
tree.name='root'
tree=tree.add()
tree.name='node1'
tree=tree.add()
tree.name='node2a'
tree=tree.add()
tree.name='node3'
tree=root
print root.node
tree=tree.add()
tree.name='node1a'
tree=tree.add()
tree.name='node2a'
print tree
print root.goto('node2')
print 'here'
print root.node[0].name
print root.node[1].name


def find_node(root,name,visited=[],found=[]):
    child_list = root.node
    i=0
    while child_list and i< len(child_list):
        for child in child_list:
            if child in visited: continue
            else: visited.append(child)
            if child.name == name:
                found.append(child)
                child_list=[]
                print 'here'
                break
            else:
                find_node(child, name,visited,found)
            i+=1
    return found

def render_tree_structure(root,filename):
    return
    ####################### example of .dot file structure ######################
#
#
# digraph Tree {
# node [shape=box] ;
# 0 [label="X[4332] <= 0.072\ngini = 0.5\nsamples = 1778\nvalue = [1438, 1388]"] ;
# 1 [label="gini = 0.5\nsamples = 1633\nvalue = [1274, 1323]"] ;
# 0 -> 1 [labeldistance=2.5, labelangle=45, headlabel="True"] ;
# 2 [label="gini = 0.407\nsamples = 145\nvalue = [164, 65]"] ;
# 0 -> 2 [labeldistance=2.5, labelangle=-45, headlabel="False"] ;
# }
#
#############PYGRAPHIVIZ EXAMPLE ###################3
# >>> import pygraphviz as pgv
# >>> G=pgv.AGraph()
# >>> G.add_node('a')
# >>> G.add_edge('b','c')
# >>> G
# strict graph {
#         a;
#         b -- c;
# }


this= find_node(root,'node2a')
print this
# print this.name

# from anytree import Node, RenderTree,Resolver,Walker

# cui0 = Node('cui0')
# root = kid

# for i in range(1,10):
#     name='cui'+str(i)
#     parent_name='cui'+str(i-1)
#     execute_string = name +' = Node("'+name+'",parent='+parent_name+')'
#     exec(execute_string)
#     print execute_string
#     # kid = Node(name,parent=kid)
# for pre, fill, node in RenderTree(cui0):
#     print("%s%s" % (pre, node.name))
# w=Walker()
# this= w.walk(cui0,cui5)
# for item in this:
#     print item
# # print r.get(kid,'cui5')
# # print r.glob(cui0,'cui5')