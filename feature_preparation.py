############################### START LEGACY CODE #####################################


###TO-DO###
    #1. Check that arrays are actually working
        ### DONE - working for complication and activity
    #2. Split out negation detection as a separate method that is optionally called by main method
        ### issue with compound words that contain negation (e.g. noninflamed)
    #3. Improve negation detection, or try using negex (or UMLS if possible)
    #4. Try getting rid of activity w/o location and see what happens
    #5. change location headers to a dictionary (which would be more robust to changes in content)
    #6. Fix hacks (jejunum, unrecognized term from capturing full words)
        ## this would need to detect negation + see what if maps back to that led to original regex hit



# locationHeaders=['ileum', 'duodenum', 'jejunum', 'ascending', 'transverse', 'descending', 'sigmoid', 'rectum', 'stomach', 'esophagus']
# location_dic={'ileum':0,
#               'duodenum':1,
#               'jejunum':2,
#               'ascending':3,
#               'transverse':4,
#               'descending':5,
#               'sigmoid':6,
#               'rectum':7,
#               'stomach':8,
#               'esophagus':9}
# reversed_location_dic={}
#
# for key in locationHeaders:
#     reversed_location_dic[location_dic[key]]=key
#
#
# def make_annotation_feature_array(complication_mapping,activity_mapping,file_number_list,relative_path='~/Desktop/brat-v1.3_Crunchy_Frog/data/rapid-annotated/'):
#     ####INPUTS = complication and activity mappings, location headers, list of file numbers upon which to operate, and
#                 #relative path to folder containing those files
#     ####OUTPUTS = # of files x ((len(locations) +1) x len(activity_mappings))
#         ## +1 is to account for cases in which activity is mentioned without an associated location
#
#     import json,os
#     skipped_term_list = []
#     skipped_filepath_list = []
#     path = os.path.expanduser(relative_path)
#     all_location_arrays=[]
#     all_complication_arrays=[]
#     for file_index in range(1,len(file_number_list)+1):
#         this_path = path + str(file_index) + '-classified.ftr'
#         if file_index < len(file_number_list)-1:
#             next_path = path + str(file_index+1) + '-classified.ftr'
#         else:
#             next_path = path+str(file_index)+'-classified.ftr'
#
#         if os.path.isfile(next_path): #### This should never fail in current implementation, but could help if there are unannotated files in interspersed in a data set
#             activity_indices_to_augment=[] ##list of indices to add +1 to in array for this file given found terms
#             location_findings=[0]*(len(activity_mapping)) # each location could have an activity mapping
#             location_findings=[location_findings]*(len(location_dic)+1)
#             #location finding is structured [location_index][activity_index]
#             complication_findings = [0]*(len(complication_mapping))
#             with open(this_path,'rb') as input_file:
#                 x=json.load(input_file)
#                 for dic in x:
#                     found_location_indices=[] #what are the row indices of locations found
#                     found_complication_indices=[]
#                     negation_present=0
#                     location_present=0
#                     if 'negation' in dic: negation_present=1
#                     ###TO-DO:
#                         ### handle locations
#                         ### handle multiple for each line locations
#                         ### handle activities without locations
#                         ### build array of location location x activity index + complications indices
#                     if 'location' in dic:
#                         location_present=1
#                         if type(dic['location']) != list: dic['location']=[dic['location']]
#                         for location in dic['location']:
#                             ### REVERT AFTER FIXING ANNOTATIONS ###
#                             if location == 'jejunum': continue
#                             else:
#                                 found_location_indices.append(location_dic[location])
#                     if 'complication' in dic:
#                         if type(dic['complication'])!= list: dic['complication']=[dic['complication']]
#                         for term in dic['complication']:
#                             if negation_present==1:
#                                 complication_findings[complication_mapping['negated-'+term]]+=1
#                                 # complication_indices_to_augment.append(complication_mapping['negated-'+term])
#                             else:
#                                 complication_findings[complication_mapping[term]]+=1
#
#                     if 'activity-terms' in dic:
#                         if type (dic['activity-terms']) != list: dic['activity-terms'] = [dic['activity-terms']]
#                         for term in dic['activity-terms']:
#                             ##To-Do - fix hacks below
#                             if term.lower() == 'noninflamed':
#                                 term = 'inflamed'
#                                 negation_present=1
#                             if term not in activity_mapping: ##HACK
#                                 skipped_filepath_list.append([this_path])
#                                 skipped_term_list.append([term])
#                                 continue
#                             if negation_present==1:
#                                 # activity_indices_to_augment.append(activity_mapping['negated-'+term])
#                                 activity_index=activity_mapping['negated-'+term]
#                             else:
#                                 # activity_indices_to_augment.append(activity_mapping[term])
#                                 activity_index=activity_mapping[term]
#                             if found_location_indices:
#                                 for location_index in found_location_indices:
#                                     location_findings[location_index][activity_index]+=1 ##increment activity finding for that location
#                             else:   ###handles when you see activity without location
#                                 location_findings[-1][activity_index]+=1
#
#             flat_location_findings = [item for sublist in location_findings for item in sublist]
#             all_location_arrays.append(flat_location_findings) #### all np location arrays
#             all_complication_arrays.append(complication_findings)  ### all np compliaction arrays
#             import numpy as np
#         else:
#             print 'BAD FILE PATH'
#             return None
#
#     all_location_arrays= np.asarray(all_location_arrays)
#     import csv
#     file_path_csv= csv.writer(open(os.path.expanduser('~/Desktop/bad_file_paths.csv'),'wb'),delimiter=',')
#     file_path_csv.writerows(skipped_filepath_list)
#     term_csv= csv.writer(open(os.path.expanduser('~/Desktop/bad_terms.csv'),'wb'),delimiter=',')
#     term_csv.writerows(skipped_term_list)
#
#     return all_location_arrays
#
#
# ####OLD WORKING VERSION BELOW (Doesn't use list input####
# # def make_annotation_feature_array(complication_mapping,activity_mapping,relative_path='~/Desktop/brat-v1.3_Crunchy_Frog/data/rapid-annotated/',list_number_list='todo'):
# #     import json,os
# #     path = os.path.expanduser(relative_path)
# #     all_location_arrays=[]
# #     all_complication_arrays=[]
# #     i=0
# #     while i ==0 or os.path.isfile(next_path):
# #         this_path = path + str(i)+'-classified.ftr'
# #         next_path = path + str(i+1)+'-classified.ftr'
# #         activity_indices_to_augment=[] ##list of indices to add +1 to in array for this file given found terms
# #         location_findings=[0]*(len(activity_mapping)) # +1 is to save space for activity with no location
# #         location_findings=[location_findings]*(len(locationHeaders)+1)
# #         complication_findings = [0]*(len(complication_mapping))
# #         with open(this_path,'rb') as input_file:
# #             x=json.load(input_file)
# #             for dic in x:
# #                 found_location_indices=[] #what are the row indices of locations found
# #                 found_complication_indices=[]
# #                 negation_present=0
# #                 location_present=0
# #                 if 'negation' in dic: negation_present=1
# #                 ###TO-DO:
# #                     ### handle locations
# #                     ### handle multiple for each line locations
# #                     ### handle activities without locations
# #                     ### build array of location location x activity index + complications indices
# #                 if 'location' in dic:
# #                     location_present=1
# #                     if type(dic['location']) != list: dic['location']=[dic['location']]
# #                     for location in dic['location']:
# #                         found_location_indices.append(locationHeaders.index(location))
# #                 if 'complication' in dic:
# #                     if type(dic['complication'])!= list: dic['complication']=[dic['complication']]
# #                     for term in dic['complication']:
# #                         if negation_present==1:
# #                             complication_findings[complication_mapping['negated-'+term]]+=1
# #                             # complication_indices_to_augment.append(complication_mapping['negated-'+term])
# #                         else:
# #                             complication_findings[complication_mapping[term]]+=1
# #
# #                 if 'activity-terms' in dic:
# #                     if type (dic['activity-terms']) != list: dic['activity-terms'] = [dic['activity-terms']]
# #                     for term in dic['activity-terms']:
# #                         ### TO-DO:
# #                             ### FIX THIS HACK TO BETTER DEAL WITH ACTIVITY ISSUES (COULD REGEX THROUGH EXISTING KEYS UNTIL A MATCH? ###
# #                         if term not in activity_mapping:
# #                             location_findings[-1][activity_index]+=1
# #                             continue
# #                         if negation_present==1:
# #                             # activity_indices_to_augment.append(activity_mapping['negated-'+term])
# #                             activity_index=activity_mapping['negated-'+term]
# #                         else:
# #                             # activity_indices_to_augment.append(activity_mapping[term])
# #                             activity_index=activity_mapping[term]
# #                         if found_location_indices:
# #                             for location_index in found_location_indices:
# #                                 location_findings[location_index][activity_index]+=1
# #                         else:   ###handles when you see activity without location
# #                             location_findings[-1][activity_index]+=1
# #         flat_location_findings = [item for sublist in location_findings for item in sublist]
# #         all_location_arrays.append(flat_location_findings) #### all np location arrays
# #         all_complication_arrays.append(complication_findings)  ### all np compliaction arrays
# #         import numpy as np
# #         i+=1
# #
# #     all_location_arrays= np.asarray(all_location_arrays)
# #     return all_location_arrays
#
#
#
# def get_annotation_indices(annotation_reference_file):
#     import csv
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
#
# ####structure of array
# # location : [just location, negated location, location activity 1, negated location activity 1....]
# # complication: [just complication 1, negated compication 1....]
#
#
#
# #############ANTIQUATED METHODS FOR ARRAY BUILDING USING .ANN FILES INSTEAD OF .FTR ###########
#
# # def get_file_annotations(num_docs,file_number_list='TODO'):
# #     ##To-Do:
# #         ###change from num_docs to file_number_list to ensure that it pulls right annotations
# #         ###change to handle .ftr files
# #     i=1
# #     import os, csv
# #     from pathlib import Path
# #     annotation_list = []
# #     annotation_filepath_base = os.path.expanduser('~/Desktop/brat-v1.3_Crunchy_Frog/data/rapid-annotated/')
# #     full_filepath= annotation_filepath_base+str(i)+'-classified.ann'
# #     while os.path.isfile(full_filepath) and i<num_docs: ##make sure it only gets enough, and is a real file
# #         these_annotations=list(csv.reader(open(full_filepath,'rU'),delimiter='\t'))
# #         for j in range(len(these_annotations)):
# #             annotation_type=these_annotations[j][1]  ###deal with formatting nuances to get annotaiotn type
# #             annotation_type=annotation_type.split(' ')[0]
# #             these_annotations[j]=annotation_type
# #         annotation_list.append(these_annotations)
# #         i+=1
# #         full_filepath = annotation_filepath_base + str(i) + '-classified.ann'
# #     print annotation_list
# #     return annotation_list
# #
# #
# # def transform_annotations_to_array(annotation_list):
# #     ###To-Do:
# #         ##1. use .ftr document
# #         ##2. generalize this so that it properly lines up with
# #     from collections import OrderedDict
# #     list_of_location_lists=[]
# #     for annotations in annotation_list:
# #         location_counts_list=[]
# #         location_count_dic={
# #         'ileum':0,
# #         'ascending':0,#
# #         'transverse':0,#
# #         'descending':0,#
# #         'sigmoid':0,#
# #         'rectum':0,#
# #         'jejunum':0,#
# #         'duodenum':0,#
# #         'stomach':0,#
# #         'esophagus':0}#
# #         OrderedDict(sorted(location_count_dic.items(), key=lambda t: t[0]))
# #         for key in location_count_dic:
# #             if location_count_dic[key] !=0:
# #                 found_something=1
# #             location_count_dic[key]=annotations.count(key)
# #             location_counts_list.append(location_count_dic[key])
# #         location_counts_list.append(annotations.count('activity-terms'))
# #         list_of_location_lists.append(location_counts_list)
# #     import numpy as np
# #     array_of_annotations = np.asarray(list_of_location_lists)
# #     return array_of_annotations
# # #####################################http://foc/###########################################
#
#
# ######EXAMPLE OF CALLS
# def verify_mappings():
#     activities,complications=get_annotation_indices('/home/john/Desktop/nlp_work/full-key-value_stidham.csv')
#     print activities
#     print complications
#     all_arrays=make_annotation_feature_array(complication_mapping=complications,activity_mapping=activities,file_number_list = range(1,10))
#     print all_arrays
#     for line in all_arrays:
#         print 'BEGIN NEW LINE BELOW'
#         element_index=0
#         for element in line:
#             print 'len line - '+str(len(line))
#             if  element_index < len(activities) and element > 0:
#                 print str(element_index)+ ' - '+str(activities.items()[element_index])
#
#             element_index+=1
#     # print all_arrays
#     # print len(complications)
#     print len(activities)
#     print len(complications)
#
# # verify_mappings()
# # print len(locationHeaders)
# # activities, complications = get_annotation_indices('/home/john/Desktop/nlp_work/full-key-value_stidham.csv')
# # print activities.items()[17]
#
# activities, complications = get_annotation_indices('/home/john/Desktop/nlp_work/full-key-value_stidham.csv')
# print activities
# all_arrays = make_annotation_feature_array(complication_mapping=complications, activity_mapping=activities,
#                                            file_number_list=range(1, 10))
# make_annotation_feature_array(complication_mapping=complications,activity_mapping=activities,file_number_list=range(1,10))

########################### END LEGACY CODE ####################################


def ftr_generation(input_path,kv_list):
    "Writes out .ftr files given kvs associated with each file "
    from keyValue import keyValue
    for path in fp_kv_dict:
        ftr_dict_list=[]
        for kv in kv_list:
            finding_dict={'concept_type':kv.concept_type,'concept_terms':kv.concept_related_terms,'mapped_term':kv.mapped_term,
            'negation':kv.negation,'modifiers':kv.modifiers}
            ftr_dict_list.append(finding_dict)
        import json
        with open(input_path.replace('.txt','.ftr'), 'w') as fout:
            json.dump(ftr_dict_list, fout)

def generate_feature_matrix(output_file=0):
    "maps all feature combinations (subject, modifier, negation) to an index. Uses only found features"
    import time
    t0=time.time()
    feature_matrix_pointer={} ## will hold the mappings for each type of unique concept being mapped (e.g. surery, anatomy, outcome, etc...)
    concept_mapping={}
    negation_mapping={}
    modifier_mapping={}
    i=0
    for path in fp_kv_dict:
        for kv in fp_kv_dict[path]:
            concept_type=kv.concept_type
            if concept_type not in feature_matrix_pointer: #create sub-dict for each type of concept
                i+=1
                feature_matrix_pointer[concept_type]={}
                feature_matrix_pointer[concept_type]['concept_mappings']=set()
                feature_matrix_pointer[concept_type]['negation_mappings']=set()
                feature_matrix_pointer[concept_type]['modifier_mappings']=set()
            mapped_term= kv.mapped_term
            negation_cuis=[]
            modifier_cuis=[]
            for negator in kv.negation:
                negation_cuis.append(negator['cui'])
            for modifier in kv.modifiers:
                modifier_cuis.append(modifier['cui'])
            feature_matrix_pointer[concept_type]['concept_mappings'].add(mapped_term)
            feature_matrix_pointer[concept_type]['negation_mappings'].update(set(negation_cuis))
            feature_matrix_pointer[concept_type]['modifier_mappings'].update(set(modifier_cuis))
    for concept_type in feature_matrix_pointer:
        for mapping in feature_matrix_pointer[concept_type]:
            feature_matrix_pointer[concept_type][mapping]=sorted(list(feature_matrix_pointer[concept_type][mapping]))

    matrix_pointer= feature_matrix_pointer

    concept_matrix_mappings={} ## merge dictionaries into single dict while maintaining self-consistent order
    index=0
    import itertools
    for concept_type in sorted(list(matrix_pointer.keys())): #iterate through keys (alphabetically so it's stable between calls)
        concept_mappings=matrix_pointer[concept_type]['concept_mappings']
        negation_mappings=matrix_pointer[concept_type]['negation_mappings']
        negation_mappings.insert(0,'none')
        modifier_mappings=matrix_pointer[concept_type]['modifier_mappings']
        modifier_mappings.insert(0,'none')
        all_mappings=[concept_mappings,negation_mappings,modifier_mappings]

        combination_list=list(itertools.product(*all_mappings))
        for key in combination_list:
            if key not in concept_matrix_mappings:
                concept_matrix_mappings[key]=index
                index+=1
    if output_file !=0:
        import json
        # with open(output_file,'w') as fout:
        #     string_concept_matrix_mappings={str(k):v for k,v in concept_matrix_mappings.items()}
        #     json.dump(string_concept_matrix_mappings,fout)
        from util import json_dump_tuple_key
        json_dump_tuple_key(output_file,concept_matrix_mappings)

    return concept_matrix_mappings #dict mappings of type (concept, negation cui, modifier cui):index





import json
def ftr_to_mapping(filepath,concept_matrix_mappings):  ### change this to the fancy folder method
    import json,itertools
    with open(filepath,'r') as ftr_file:
        found_indices=[0]*len(concept_matrix_mappings)
        found_concepts = json.load(ftr_file)
        for concept in found_concepts:
            finding_combinations=[]
            negations=[]
            modifiers=[]
            subject = concept['mapped_term']
            if concept['negation']:
                for negator in concept['negation']:
                    negations.append(negator['cui'])
            else: negations.append('none')
            if concept['modifiers']:
                for modifier in concept['modifiers']:
                    modifiers.append(modifier['cui'])
            else: modifiers.append('none')
            concept_combinations=list(itertools.product(*[[subject],negations,modifiers]))
            for combo in concept_combinations:
                if combo in concept_matrix_mappings:
                    mapped_index=concept_matrix_mappings[combo]
                    found_indices[mapped_index]=1
                else:
                    print 'ERROR - Unknown combination'
    return found_indices


### MAKE MAPPINGS FROM FTR FILES #########
# from util import save_object,load_object
#
# # from keyValue import keyValue
# fp_kv_dict=load_object('file_kvs.pkl')
#
# concept_matrix_maps=generate_feature_matrix(output_file='feature_matrix_mappings.json')
# # print 'length =',len(concept_matrix_maps),'; dict =',concept_matrix_maps
# print concept_matrix_maps
#
# from util import find_files_in_folder
# all_ftr_files= find_files_in_folder('/home/john/Desktop/brat-v1.3_Crunchy_Frog/data/new-method-annotations/','ftr')
# for ftr_file in all_ftr_files:
#     ftr_to_mapping(filepath=ftr_file,concept_matrix_mappings=concept_matrix_maps)


######## ACTUALLY MAKES FTR FILES ############
# for filepath in fp_kv_dict:
#     print filepath
#     ftr_generation(input_path=filepath,kv_list=kv_list)


