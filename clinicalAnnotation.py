class clinicalAnnotation(object):
    def __init__(self,general_modifier_list=0,location_dic=0,negation_list=0,
                 complication_dic=0,clinical_modifier_dic=0,access_specification={'general_modifier_list':1,'location_dic':1,'negation_list':1,
                 'complication_dic':0,'clinical_modifier_dic':0}):
        from collections import OrderedDict
        self.access_specification=OrderedDict(sorted(access_specification.items(), key=lambda t: t[1]))
        self.clinical_modifier_dic=clinical_modifier_dic  ##ileum, jejenum, stricture, etc...
        self.negation_list=negation_list
        self.complication_dic=complication_dic
        self.location_dic=location_dic
        # self.__modifiers=modifiers  ##don't know what this adds in addition to modifier
        self.general_modifier_list=general_modifier_list

    # @property
    # def clinical_modifier_dic(self):
    #     return self.__clinical_modifier_dic
    #
    # @clinical_modifier_dic.setter
    # def clinical_modifier_dic(self, value):
    #     if self.__clinical_modifier_dic != 0:
    #         self.__clinical_modifier_dic.append(value)
    #     else:
    #         self.__clinical_modifier_dic = value
    #

