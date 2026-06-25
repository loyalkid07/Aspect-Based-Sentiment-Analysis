"""
Core Aspect-Based Sentiment Analysis Module

This module contains the main function for performing aspect-based sentiment analysis.
It extracts aspects from text and determines sentiment for each aspect.
"""

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def aspect_sentiment_analysis(txt, stop_words, nlp, sid):
    """
    Perform aspect-based sentiment analysis on input text.
    
    Args:
        txt (str): Input text to analyze
        stop_words (set): Set of stopwords to filter out
        nlp: Stanza NLP pipeline object
        sid: NLTK SentimentIntensityAnalyzer object
    
    Returns:
        list: List of [aspect, sentiment_score] pairs
    """
    txt = txt.lower()
    sentList = nltk.sent_tokenize(txt)

    finalcluster = []

    for line in sentList:
        newtaggedList = []
        txt_list = nltk.word_tokenize(line)
        taggedList = nltk.pos_tag(txt_list)

        newwordList = []
        flag = 0
        for i in range(0,len(taggedList)-1):
            if(taggedList[i][1]=="NN" and taggedList[i+1][1]=="NN"):
                newwordList.append(taggedList[i][0]+taggedList[i+1][0])
                flag=1
            else:
                if(flag==1):
                    flag=0
                    continue
                newwordList.append(taggedList[i][0])
                if(i==len(taggedList)-2):
                    newwordList.append(taggedList[i+1][0])

        finaltxt = ' '.join(word for word in newwordList)
        new_txt_list = nltk.word_tokenize(finaltxt)
        wordsList = [w for w in new_txt_list if not w in stop_words]
        taggedList = nltk.pos_tag(wordsList)

        doc = nlp(finaltxt)

        dep_node = []
        for sent in doc.sentences:
            for dep_edge in sent.dependencies:
                dep_node.append([dep_edge[2].text, dep_edge[0].id, dep_edge[1]])

        for i in range(0, len(dep_node)):
            if (int(dep_node[i][1]) != 0):
                dep_node[i][1] = newwordList[(int(dep_node[i][1]) - 1)]

        featureList = []
        categories = []
        for i in taggedList:
            if(i[1]=='JJ' or i[1]=='NN' or i[1]=='JJR' or i[1]=='NNS' or i[1]=='RB'):
                featureList.append(list(i))
                categories.append(i[0])

        for i in featureList:
            filist = []
            for j in dep_node:
                if((j[0]==i[0] or j[1]==i[0]) and (j[2] in ["nsubj", "acl:relcl", "obj", "dobj", "agent", "advmod", "amod", "neg", "prep_of", "acomp", "xcomp", "compound"])):
                    if(j[0]==i[0]):
                        filist.append(j[1])
                    else:
                        filist.append(j[0])
            finalcluster.append([i[0], filist])

    # Sentiment analysis
    aspect_sentiments = []
    for aspect in finalcluster:
        aspect_text = aspect[0]
        sentiment_score = sid.polarity_scores(aspect_text)['compound']
        aspect_sentiments.append([aspect_text, sentiment_score])

    return aspect_sentiments