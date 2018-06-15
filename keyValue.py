class keyValue(object):
    def __init__(self,concept='',concept_type='',negation='',activity_terms='',concept_related_terms='',modifiers='',sentence=''):
        self.__concept=concept  ##ileum, jejenum, stricture, etc...
        self.__negation=negation
        self.__activity_terms=activity_terms
        self.__concept_related_terms=concept_related_terms  ##actual words that indicate the location or complication
        # self.__modifiers=modifiers  ##don't know what this adds in addition to modifier
        self.__modifiers=modifiers
        self.__concept_type=concept_type  ##location or complication
        self.sentence=sentence
    #    self.__concept=10
    #     self.__concept=concept
        # self.concept_related_terms=concept_related_terms
        # self.activity_terms=activity_terms
        # self.modifiers=modifiers
        # self.negation=negation

    @property
    def concept(self):
        return self.__concept

    @concept.setter
    def concept(self,value):
        # if self.__concept=='':
        self.__concept = value
        # else:
            # self.__concept+=', '
            # self.__concept+=value

    @property
    def concept_type(self):
        return self.__concept_type

    @concept_type.setter
    def concept_type(self, value):
        # if self.__concept_type == '':
        self.__concept_type = value
        # else:
        #     self.__concept_type =value


    @property
    def activity_terms(self):
        return self.__activity_terms

###MAKE MORE GENERALIZABLE
    #### RENAME modifier_clinical
    #### EACH WILL BE A TWO MEMBER LIST
    ### on addition, check which list should be match, and alter string accordingly
    ### change code for activity two add to this in both types of activity
    @activity_terms.setter
    def activity_terms(self,value):
        if self.__activity_terms == '':
            self.__activity_terms = [value]
        else:
            self.__activity_terms.append(value)
            from ibs_nlp_util import removeOverlappingPhrases
            self.__activity_terms=removeOverlappingPhrases(self.__activity_terms)

    @property
    def concept_related_terms(self):
        return self.__concept_related_terms

    @concept_related_terms.setter
    def concept_related_terms(self,value):
        if self.__concept_related_terms == '':
            self.__concept_related_terms = value
        else:
            self.__concept_related_terms =value
    @property
    def modifiers(self):
        return self.__modifiers

    ##rename modifier_general
    @modifiers.setter
    def modifiers(self,value):
        if self.__modifiers == '':
            self.__modifiers = [value]
        else:
            self.__modifiers.append(value)
            from ibs_nlp_util import removeOverlappingPhrases
            self.__modifiers=removeOverlappingPhrases(self.__modifiers)

    @property
    def negation(self):
        return self.__negation

    @negation.setter
    def negation(self,value):
        if self.__negation == '':
            self.__negation = [value]
        else:
            from ibs_nlp_util import removeOverlappingPhrases
            self.__negation.append(value)
            self.__negation=removeOverlappingPhrases(self.__negation)

    @property
    def values(self):
        return ###add everything
    def mapFindings(self,mapping):
        return ###output findings in a sklearn usable way (maybe as vector representation from spaCy)
        ###query list of constant vlaues (locations of something) that make it know how many possible combos it has
    def makeDisplay(self):
        return ### look up some way to print out the values associated with a finding


### TO-DO ##
    #Make keyValue objects output themselves in the appropriate brat or ftr format
# def make_np_key_value(kv_object):
#     import numpy as np
    #### do things to convert kv into np representations for each part


###NOTES ABOUT LOCATION####
#1. For review, just need small bowel
#2. For classifier, both labels would be ideal (treat as independent items)
    ###A. Vinod notes - either flatten out, or go from child to parent (after classification)
#3. Notes (strictures have a fixed location and various terms)
#4. Use query expansion to go from these terms to others 'if possible'
#5. Use simstring