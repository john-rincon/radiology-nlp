####TO-DO######
    ##DONE - 1. Test package for annotation verification
    ##STARTED - almost done in test.py file 2. Change classification pipeline to pull from same data set as annotations
    ##DONE - 3. See if above changes radically improve performance
    ##4. Redo classifier using Ryan's formal documents + UMLS
    ##5. Re-test all above
    ###Secondary to do
        ##A. Add in decision tree stumps
            ##A1 - pass these stumps into the SVM
        ##B. Look over other classifier specific stuff

def display_feature_importance(classifier,X_test):
    import matplotlib.pyplot as plt
    import numpy as np
    forest = classifier
    importances = forest.feature_importances_
    std = np.std([tree.feature_importances_ for tree in forest.estimators_],
                 axis=0)
    indices = np.argsort(importances)[::-1]

    # Print the feature ranking
    print("Feature ranking:")
    X = X_test
    for f in range(X.shape[1]):
        print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

    # Plot the feature importances of the forest
    plt.figure()
    plt.title("Feature importances")
    plt.bar(range(X.shape[1]), importances[indices],
            color="r", yerr=std[indices], align="center")
    plt.xticks(range(X.shape[1]), indices)
    plt.xlim([-1, X.shape[1]])
    plt.show()


####END EXAMPLE
def classify_docs(train_path,test_path):
    import sklearn.datasets
    import csv, os
    import numpy as np
    from sklearn.pipeline import Pipeline
    from sklearn.cross_validation import train_test_split as tts
    ####Specify Data sets####
        ####To-Do:
         #1. make pipeline better so I'm not pointing in all these different places
    filepath=os.path.expanduser('~/Desktop/nlp_work/classified-report-text-test.csv')
    radiology_files= list(csv.reader(open(filepath,'rU'),delimiter=','))
    print len(radiology_files)
    print radiology_files[-1]

    ### used for testing ONLY !!!! ###
    from sklearn.feature_extraction.text import CountVectorizer
    count_vect = CountVectorizer()
    textData=[]
    classData=[]
    ###To-Do:
        ###1. FIX - there are doubles of files??? Not sure where this came from?

    ##########
    for line in radiology_files[1:]:
        textData.append(line[-1])
        classData.append(line[:-1])

    locDict = {1: 'ascending',
                   9: 'Duodenum',
                   0: 'Ileum',
                   7: 'Prox Ileum',
                   5: 'rectum',
                   10: 'Stomach',
                   3: 'Descending',
                   11: 'Esophagus',
                   8: 'Jejunum',
                   4: 'Sigmoid',
                   2: 'transverse',
                   6: 'prox small bowel',
                    12: 'absent'}
    targetData=[]
    newText=[]
    y=0
    total_here=0
    file_number_list=[]
    file_number_counter=0
    for line in classData:
        i=-1
        found_something=0

        ###FILTER OUT JUST ILEUM AND NEGATIVE RESULTS - WHY DOESNT THIS WORK WELL####

        # if int(line[0]) ==1:
        #     targetData.append(1)
        #     newText.append(textData[y])
        #     file_number_list+=[file_number_counter]
        #     total_here+=1
        # elif '1' not in line[:12]:
        #     targetData.append(0)
        #     newText.append(textData[y])
        #     file_number_list+=[file_number_counter]
        #     total_here+=1
        # file_number_counter+=1
        # continue
        ###########################################

        for value in line[:12]:
            i+=1



            ###TO-DO:
                # 1. Investigate below, seems iffy as far as correctly labeling files
            if int(value)>0:
                # targetData.append(i)
                newText.append(textData[y])
                # targetData.append(locDict[i])      ###*****this one does all the locations
                if i==0:
                    targetData.append('ileum')  ###for binary
                else:
                    targetData.append('other')
                #     print 'look down'
                #     print line
                found_something+=1
                file_number_list+=[file_number_counter]
               #  else: targetData.append(1)
               #  targetData.append('present')
               #  targetData.append(1)
                break
        if found_something == 0:
            newText.append(textData[y])
            # targetData.append(locDict[12])  ### for multi-label
            targetData.append('absent')   ##for binary
            file_number_list+=[file_number_counter]
        y+=1
        file_number_counter+=1

    textData=newText
    print 'file_num_list'
    print file_number_list[0:10]
    print file_number_list[-10:]
    print len(file_number_list)


    # Transform count features to "weights"
    from sklearn.feature_extraction.text import TfidfTransformer,TfidfVectorizer

    from imblearn.over_sampling import RandomOverSampler
    targetData=np.asarray(targetData)
    # print targetData.shape

    X_train,y_train=textData,targetData

    from sklearn import svm
    #
    from sklearn.linear_model import SGDClassifier
    #
    # #y_train is a 1939 length numpy.ndarray, each row has 1 number (probably corresponding to label??)
    # #X_train is a list of some sort. 1939 long with text of each report as contents
    #
    # # ########MASS UNCOMMENT BELOW HERE#######
    #
    # current_clfr = Pipeline([('vect', CountVectorizer(analyzer='char_wb',ngram_range=(1,3),stop_words='english',max_df=.8)), ('tfidf', TfidfTransformer(smooth_idf=True,norm='l2')), ('clfr', SGDClassifier(class_weight='balanced',loss='log', penalty='l2',alpha=1e-3))])

    current_clfr = Pipeline([('vect', CountVectorizer(analyzer='word',stop_words='english',ngram_range=(1,3))), ('tfidf', TfidfTransformer(smooth_idf=True,norm='l2')), ('clfr', svm.SVC(class_weight='balanced',kernel='linear',tol=.000001,C=1))]) ##good but not consistent

    from sklearn.ensemble import RandomForestClassifier
    # current_clfr = Pipeline([('vect', CountVectorizer(analyzer='word',stop_words='english',ngram_range=(1,4))), ('tfidf', TfidfTransformer(smooth_idf=True,norm='l2')), ('clfr', RandomForestClassifier(class_weight='balanced',max_features=5))]) ##good but not consistent

    ###RUN & PREDICT BELOW###
    # predicted= current_clfr.predict(X_test)
    # print np.mean(predicted == y_test)
    assignmentList=[]
    header=['Filename','Label']
    assignmentList.insert(0,header)
    # print len(assignmentList)
    # csv_file=csv.writer(open('/home/john/Desktop/nlp_work/svm-location.csv','wb'))
    # csv_file.writerows(assignmentList)

    ###Print out f1-scores and such
    from sklearn import metrics
    # print(metrics.classification_report(y_test,predicted))


#############Below - pipeline with SVD transform
    from sklearn.decomposition import TruncatedSVD
    # SVD_clfr = Pipeline([('vect', CountVectorizer(analyzer='word',stop_words='english')), ('tfidf', TfidfTransformer(smooth_idf=True,sublinear_tf=True,use_idf=True,norm='l2')),('svd',TruncatedSVD(n_components=1000))])
    svd_on=0
############################

    ###Below = pipeline w/o SVD transform#######
    # count_vectorizer= CountVectorizer(analyzer='word',stop_words='english')
    # tfid_transformer= TfidfTransformer(smooth_idf=True,sublinear_tf=True,use_idf=True,norm='l2')
    tfid_vectorizer= TfidfVectorizer(analyzer='word',stop_words='english',ngram_range=(1,1), smooth_idf=True,sublinear_tf=True,use_idf=True,norm='l2')
    # truncated_sv= TruncatedSVD(n_components=150)
    ###OLD WORKED BELOW ####
    # tfid_pipeline = Pipeline([('vect', CountVectorizer(analyzer='word',stop_words='english')), ('tfidf', TfidfTransformer(smooth_idf=True,sublinear_tf=True,use_idf=True,norm='l2'))])

    #####################################
    print 'shape below'

    ###OLD WORKED BELOW ###
    # x_new=tfid_pipeline.fit_transform(X_train)
    x_new = tfid_vectorizer.fit_transform(X_train)
    feature_names = tfid_vectorizer.get_feature_names()
    print "FEATURES BELOW"
    print feature_names
    print x_new.shape
    import re
####### Add meta features ########
    transform_functions = [
        lambda x: len(x),
        lambda x: x.count(" "),
        lambda x: x.count("."),
        lambda x: x.count("!"),
        lambda x: x.count("?"),
        lambda x: len(x) / (x.count(" ") + 1),
        lambda x: x.count(" ") / (x.count(".") + 1),
        lambda x: len(re.findall("\d", x)),
        lambda x: len(re.findall("[A-Z]", x)),
    ]

    columns = []
    import pandas as pd
    num_docs=len(X_train)
    X_train=pd.DataFrame(X_train,columns=["text"])
    for func in transform_functions:
        columns.append(X_train["text"].apply(func))

    # Convert the meta features to a numpy array.
    meta = np.asarray(columns).T
    print "META"

    print meta.shape
######### Add annotation features ####################
    from feature_preparation import get_annotation_indices,make_annotation_feature_array

    activities, complications = get_annotation_indices('/home/john/Desktop/nlp_work/full-key-value_stidham.csv')
    annotation_array = make_annotation_feature_array(complication_mapping=complications, activity_mapping=activities,file_number_list=file_number_list)
    ##TO - DO:
    ### 1. Change annotation method to using .ftr files w/ negation detection
    # annotation_array=annotation_array[:num_docs]
    print 'annotation shape'
    print annotation_array.shape

    ### stack the Tf-Id featueres with meta features
    print "SHAPES:"
    print 'x-new: '+str(x_new.shape)
    print 'meta: '+str(meta.shape)
    print "annotations"+str(annotation_array.shape)

    import scipy
    if svd_on==1:
        x_new=scipy.sparse.hstack([x_new,annotation_array,meta])
        x_new = truncated_sv.fit_transform(x_new)
    else:
        x_new=scipy.sparse.hstack([x_new,annotation_array,meta])
        # x_new=np.hstack([meta,annotation_array])
        # x_new=annotation_array
        # x_new=scipy.sparse.hstack([meta,x_new])

    print "NEW SHAPE - "+ str(x_new.shape)
    #############OVER SAMPLING#############
    #######################################
    ros=RandomOverSampler(random_state=1)
    ##SVM parameters below###
    # tuned_parameters = [{'kernel': ['linear'], 'C': [1]}]

    ###Random Forest Parameters - lots###
    # tuned_parameters = { 'n_estimators': [10, 100, 500], 'max_features': ['auto', 'log2']}

    ###Fast & Best
    tuned_parameters = { 'n_estimators': [100], 'max_features': ['auto']}


    X_train2, X_test2, y_train2, y_test2 = tts(x_new,y_train, test_size=.3) ##moved things up

    ####Over-sample underrepresented classes ####
    X_res,y_res=ros.fit_sample(X_train2,y_train2)

    ### Run without over sampling #####
    # X_res,y_res=X_train2,y_train2


    from sklearn.model_selection import GridSearchCV
    from sklearn.svm import SVC
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.metrics import classification_report
    # current_clfr=SGDClassifier(class_weight='balanced',loss='log', penalty='l2',alpha=1e-3)
    # current_clfr=svm.LinearSVC(class_weight='balanced',tol=.000001,C=1)
    # current_clfr = GridSearchCV(SVC(),tuned_parameters,cv=5,scoring='f1')
    # current_clfr = GridSearchCV(RandomForestClassifier(n_jobs=-1,max_features= 'sqrt' ,n_estimators=50, oob_score = True),tuned_parameters,cv=5,scoring='f1')
    # current_clfr = GridSearchCV(RandomForestClassifier(n_jobs=-1,oob_score = True),tuned_parameters,cv=5,scoring='f1')

    ########################### Best one for quick run ############################################################
    current_clfr=RandomForestClassifier(min_samples_split=100,n_jobs=-1,oob_score=True,n_estimators=100,max_features='auto') ###changing estimators and depth can help find stumps

    ######################################################################################
    from sklearn import tree

#############FOR FINDING STUMPS AND SELECTING OUT FEATURES #####################
    from sklearn.tree import DecisionTreeClassifier
    #
    # current_clfr=tree.DecisionTreeClassifier(splitter='random',max_depth=2,min_samples_leaf=1)
    #
    # ### Stump based estimator #####
    # from sklearn.ensemble import AdaBoostClassifier
    # current_clfr=AdaBoostClassifier(DecisionTreeClassifier(max_depth=2),n_estimators=1000,algorithm='SAMME')
    # # current_clfr=MultinomialNB()
    # ###Run selected classifier
    # from inspect import getmembers
    # # print current_clfr
    # from sklearn import tree
    # this_tree= current_clfr.tree_
    # feature= this_tree.feature
    # nodes= this_tree.node_count
    # children_left = this_tree.children_left
    # children_right = this_tree.children_right
    # threshold = this_tree.threshold
    # features_used=[]
    # for i in range(nodes):
    #     if feature[i] != -2:    # current_clfr = current_clfr.fit(X_res, y_res)

    #         features_used.append(feature[i])
    #         print feature_names[feature[i]]
    # print features_used
###################################

    current_clfr = current_clfr.fit(X_res, y_res)



######GRID SEARCH BELOW - GOOD CODE#######
    # print "STARTING GRID SEARCH"
    # current_clfr = current_clfr.fit(X_res, y_res)
    #
    #
    # print("Best parameters set found on development set:")
    # print()
    # print(current_clfr.best_params_)
    # print()
    # print("Grid scores on development set:")
    # print()
    # means = current_clfr.cv_results_['mean_test_score']
    # stds = current_clfr.cv_results_['std_test_score']
    # for mean, std, params in zip(means, stds, current_clfr.cv_results_['params']):
    #         print("%0.3f (+/-%0.03f) for %r"
    #               % (mean, std * 2, params))
    # print()
    #
    # print("Detailed classification report:")
    # print()
    # print("The model is trained on the full development set.")
    # print("The scores are computed on the full evaluation set.")
    # print()
    #
    #
    # y_true, y_pred = y_test2, current_clfr.predict(X_test2)
    # print(classification_report(y_true, y_pred))
    # print()

###################################################################

############## Performance Printout ##############################
    predicted= current_clfr.predict(X_test2)
    print np.mean(predicted == y_test2)
    print(metrics.classification_report(y_test2,predicted))
##################################################################


   ######### TO VISUALIZE DECISION TREE####################
    # import graphviz
    # feature_names+=[0]*878
    # tree.export_graphviz(current_clfr,out_file='test-tree.dot',feature_names=feature_names)
    ################################################################

########## sklearn
    from sklearn import tree
    from inspect import getmembers
    i_tree = 0
    #################For getting Random Forest Parameters #########
    # for tree_in_forest in current_clfr.estimators_:
    #     with open('tree_' + str(i_tree) + '.dot', 'w') as my_file:
    #         my_file = tree.export_graphviz(tree_in_forest, out_file=my_file)
    #     i_tree = i_tree + 1
    #     print getmembers(tree_in_forest.tree_)
    ###graphing forest features ####




#####GRAPH RESULTS #####

# print(__doc__)
def graph_results():
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn import svm, datasets


    def make_meshgrid(x, y, h=.02):
        """Create a mesh of points to plot in

        Parameters
        ----------
        x: data to base x-axis meshgrid on
        y: data to base y-axis meshgrid on
        h: stepsize for meshgrid, optional

        Returns
        -------
        xx, yy : ndarray
        """
        x_min, x_max = x.min() - .1, x.max() + .1
        y_min, y_max = y.min() - .1, y.max() + .1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                             np.arange(y_min, y_max, h))
        return xx, yy


    def plot_contours(ax, clf, xx, yy, **params):
        """Plot the decision boundaries for a classifier.

        Parameters
        ----------
        ax: matplotlib axes object
        clf: a classifier
        xx: meshgrid ndarray
        yy: meshgrid ndarray
        params: dictionary of params to pass to contourf, optional
        """
        Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)
        out = ax.contourf(xx, yy, Z, **params)
        return out


    # import some data to play with
    iris = datasets.load_iris()
    # Take the first two features. We could avoid this by using a two-dim dataset
    X = X_res
    y = y_res

    # we create an instance of SVM and fit out data. We do not scale our
    # data since we want to plot the support vectors
    C = 1.0  # SVM regularization parameter
    models = (svm.SVC(kernel='linear', C=C,class_weight='balanced'),
              svm.LinearSVC(C=C),
              svm.SVC(kernel='rbf', gamma=0.7, C=C),
              svm.SVC(kernel='poly', degree=2, C=C))
    models = (clf.fit(X, y) for clf in models)

    # title for the plots
    titles = ('SVC with linear kernel','LinearSVC (linear kernel)',
              'SVC with RBF kernel',
              'SVC with polynomial (degree 2) kernel')

    # Set-up 2x2 grid for plotting.
    fig, sub = plt.subplots(2, 2)
    plt.subplots_adjust(wspace=0.4, hspace=0.4)

    X0, X1 = X[:, 0], X[:, 1]
    xx, yy = make_meshgrid(X0, X1)

    for clf, title, ax in zip(models, titles, sub.flatten()):
        plot_contours(ax, clf, xx, yy,
                      cmap=plt.cm.coolwarm, alpha=0.8)
        ax.scatter(X0, X1, c=y, cmap=plt.cm.coolwarm, s=20, edgecolors='k')
        ax.set_xlim(xx.min(), xx.max())
        ax.set_ylim(yy.min(), yy.max())
        ax.set_xlabel('Principal Component 1')
        ax.set_ylabel('Principal Component 2')
        ax.set_xticks(())
        ax.set_yticks(())
        ax.set_title(title)

    plt.show()

classify_docs(train_path='/home/john/Desktop/nlp_work/labeled-data/location',test_path='/home/john/Desktop/nlp_work/labeled-data/location')
# x=transform_annotations_to_array(get_file_annotations())
# print x

#### TO VISUALIZE TREE .dot file as PDF ####
# from graphviz import Digraph,Source
# file = open('test-tree.dot','r')
# text=file.read()
# dot=Source(text)
# dot.render('test-graph.gv', view=True)


#
# from sklearn.externals.six import StringIO
# from IPython.display import Image
# from sklearn.tree import export_graphviz
# import pydotplus
#
# dot_data = StringIO()
#
# export_graphviz(current_clfr, out_file=dot_data,
#                 filled=True, rounded=True,
#                 special_characters=True)
#
# graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
# Image(graph.create_png())