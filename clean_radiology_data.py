import csv
import os
import re
from operator import itemgetter

################################### OVERVIEW ########################################################
## Methods for cleaning and writing out radiology data as well as Brat .txt and .ann files

#####INDEX NOTES##########
# locationIndices= range(15,27)
# fistulaIndices = [27,28]
# abcessIndices = [29,30]
# strictureIndex=31
# dilationIndex=32
# priorSurgeryIndex=33
# ostomyIndex=34
# pouchIndex=35
#print input_file[1][textIndex].split("\n \n")
#print input_file[1][textIndex]






def remove_unread_reports (input_file):
###################################################################################################################
####  INPUT = list of lists from import of data file containing raidology text and labels (or lackthereof) 
####  OUTPUT = list of lists of reports and labels for reports that have been read (indicated by either a "1" for any label
####         value, or a '1' in the 'Processed_manualOveride' column
####
#### *Note* - currently hardcoded to csv format, if we use consistent headers moving forward could get around this
####################################################################################################################

    read_reports=[]
    j=0
    for line in input_file:
        if j==0:
            j+=1
            read_reports.append(line)
            continue
        sum = 0
        processed_indicator = line[36]
        label_indicators = line[15:36]
        label_indicators.append(line[40])
        for number in label_indicators:
            sum += int(number)
        if sum == 0 or processed_indicator ==1 :
            j+=1
        else:
            read_reports.append(line)
    return read_reports





###############Punctuation Fixer###############
def fix_report_spacing (input_file):
####################################################################################################################
####  INPUT = list of lists from importing csv of document text and label file
####  OUTPUT = list of just REPORT TEXT ONLY, cleaned of spacing errors and unnecessary symbols/characters
####
#### *Note - this was largely necessary due to artefacts of current data (e.g. text wrap)
####################################################################################################################
    fixed_text = []
    i = 0
    for line in input_file:
        if type(line)==list:
        ## only handle raw csv files, where text is in index 14 (hard-coded for current use)
            rad_text=line[14].strip('#')   #get weird of weird pound symbols at end of docs
        else:
        ## normal usage - handle list of strings, rather than list of lists, that are not in a list of lists
            rad_text=line.strip('#')
        foundSpacing=re.findall(r'\w+\s+[\.\?\:\)]',rad_text) #finds spacing around punctuation
        if foundSpacing:
            firstMistake=''               #some null value
            for mistake in foundSpacing:
                if mistake == firstMistake:
                    continue
                ####Find goofy spacing and punctuation issues that mess with tokenizers, and replace weird characters
                else:
                    firstMistake=mistake
                    i+=1
                    startIndex= rad_text.index(mistake)
                    stopIndex=startIndex+len(mistake)
                    worstSpaces= rad_text[startIndex:stopIndex]  ##span of text with bad spacing
                    badSpaces= worstSpaces.replace(" ","")   ##span of text with some inappropraite spacing replaced
                    fixedSpaces=badSpaces.replace('\n',"")  ##span with all inappropriate spacing replaced
                    rad_text=rad_text.replace(worstSpaces,fixedSpaces)
        foundNewLine=re.findall(r'[^\n][ \t\w\.\?\)]\n[ \t\w\.\?\:]{2}',rad_text) ##find appropriate line breaks
            ###no new line, some character, new line, other characters (not new line), two minimum (save good \n \n)
        foundNewLine = set(foundNewLine)

        for lineMistake in foundNewLine:
            startIndex = rad_text.index(lineMistake)
            stopIndex = startIndex + len(lineMistake)
            if startIndex > 50: ##sentences are 77 characters long, but 50 gives a buffer
                prevSentenceIndex=startIndex-50
            else: prevSentenceIndex=0
            badNewLines=rad_text[startIndex:stopIndex]
            if lineMistake[1]=='\n':  ###don't lost info about setion breaks
                continue
            ###Check for intentional single line returns
            intentionalSnippet=rad_text[prevSentenceIndex:startIndex]
            if ":" in intentionalSnippet: ##breaks good things...
                continue
            if lineMistake[1]==" ":   ###strip \n's w/o adding unecessary formatting
                fixedNewLines=badNewLines.replace('\n',"")
            else:   ###add spaces in place of line breaks where appropriate
                fixedNewLines=badNewLines.replace('\n'," ")
            rad_text=rad_text.replace(badNewLines,fixedNewLines)

        rad_text=rad_text.replace(". .",".") #fix double period errors

        fixed_text.append(rad_text)
    return fixed_text



###############GET RID OF UNNECESSARY INFORMATION BEFORE SECTIONS##################
def cut_unnecessary_sections (report_list):
######################################################################################################################
####  INPUT = list of report text
####  OUTPUT = list of report text cut down to pertinent sections. If cannot find section to cut at, returns original
######################################################################################################################
    import re
    num_with_finding = 0  ## counters to verify performance
    num_no_finding_or_impression = 0
    trimmed_reports=[]
    for line in report_list:
        #finds all FINDINGS headingscut
        finding_heading = re.search(r'(FINDING|Finding)[s|S]{0,2} {0,1}(:|;|\n \n|\n\n)', line)  ##find appropriate line breaks
        if finding_heading:
            finding_heading.start()
            num_with_finding+=1
        impression_heading = re.search(r'(IMPRESSION|Impression|impression|CONCLUSION|Conclusion)[s|S]{0,2} {0,1}(:|;|\n \n|\n\n)', line)  ##find appropriate line breaks
        if not impression_heading and not finding_heading:
            k=0
            num_no_finding_or_impression+=1
        if finding_heading and impression_heading:
            #### USE THE HEADING THAT COMES FIRST ###
            if finding_heading.start()<impression_heading.start():
                usefulText=line[finding_heading.start():]
            else:
                usefulText=line[impression_heading.start():]
        elif finding_heading:
            usefulText = line[finding_heading.start():]
        elif impression_heading:
            usefulText = line[impression_heading.start():]
        else:
            usefulText=line
        trimmed_reports.append(usefulText)
    return trimmed_reports



########READ IN REPORT 'FIXED THINGS' AND ADD CLASSIFIERS BACK TO TEXT###########
def add_labels (report_text,read_reports):
##### INPUT = list of report texts (no labels)
##### OUTPUT = list of lists of report texts (labels added back)
    classfiedTextCorpus=[]
    for j in range(len(report_text)):
        classifiedText=read_reports[j][15:36]+[report_text[j]] #indices 15 through 35 have ML applicable labels

        classfiedTextCorpus.append(classifiedText)
    return classfiedTextCorpus





####WRITES OUT CLASSIFIED TEXT###############
def write_out_for_brat(classified_texts,output_folder):
##########################################################################################################
####  INPUT = lists of lists (each list is report text + labels), and output folder location 
####  OUTPUT = no return. Writes out Brat annotator format of .txt files and .ann files for each report
####           >.txt files contain list of annotations found + report txt, and .ann files are blank
###########################################################################################################

    annotation_dic={}
    if output_folder[-1] != '/':
        return 'ERROR'
    header_row=classified_texts[0]
    header_index=0
    for header in header_row:
        annotation_dic[header_index]=header
        header_index+=1
    file_count=0
    for j in range(1,len(classified_texts)):  ##don't alter the header row or any text columns
        for i in range(len(classified_texts[j])-1):
            classified_texts[j][i]=annotation_dic[i]+'='+str(classified_texts[j][i])
        classified_texts[j][-1] ='\n'+classified_texts[j][-1]
    for line in classified_texts:
        full_outpath=output_folder+str(file_count)+'-classified.txt'
        annotatedOutpath=output_folder+str(file_count)+'-classified.ann'
        csv_file=csv.writer(open(full_outpath,'wb'),delimiter=',')
        csv_file.writerow(line)
        csv_file = csv.writer(open(annotatedOutpath, 'wb'), delimiter=',')
        csv_file.writerow('')
        file_count+=1



######### TRANSFORM AND CLEAN TEXT ###################
# filepath=os.path.expanduser('~/Desktop/nlp_work/nlp-rad-data2.csv') ##to Ryan's .csv file
# radiology_files= list(csv.reader(open(filepath,'rU'),delimiter=','))
# read_reports = remove_unread_reports(radiology_files)
# fixed_spacing=fix_report_spacing([line[14] for line in read_reports])
# trimmed_text=cut_unnecessary_sections(fixed_spacing)
# classified_texts= add_labels(trimmed_text,read_reports)
# # write_out_for_brat(classified_texts,'/home/john/Desktop/nlp_work/test-annotations')
# ###### WRITEOUT TEXT #########################
# classified_reports_outpath='/home/john/Desktop/nlp_work/classified-report-text-test.csv'
# csv_file=csv.writer(open(classified_reports_outpath,'wb'),delimiter=',')
# csv_file.writerows(classified_texts)


