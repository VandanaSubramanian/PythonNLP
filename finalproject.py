#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 18:53:13 2024

@author: vandanasubramanian, ruthvikreddy 
emails: vandusu@bu.edu, ruthvik@bu.edu
"""
import math 

def clean_text(txt):
    """takes a string txt as a parameter and returns a list containing the words in txt after it has been cleaned"""
    s = txt.lower().split()
    clean = []
    for word in s:
        for symbol in """.,?"'!;:""":
            word = word.replace(symbol,'')
        clean += [word]
    return clean

def stem(s):
    """returns the stem of an input string s"""
    d = {'taller':'tall','smaller':'small','seer':'see','her':'her','loving':'love'}
    
    if s[-3:] == 'ies':
        if len(s) == 4:
            return s
        else:
            s = s[:-3] + 'y'
            return s
    
    elif s[-2:] == 'es':
        s = s[:-2]
        return s
        
    elif s[-1] == 's': 
        s = s[:-1]
        return s
        
    elif s[-3:] == 'ing':
        if s in d:
            s = d[s]
        elif len(s) == 4:
            s = s
        elif s[-4] == s[-5] and s[-4] not in 'aeiou':
            s = s[:-4]
        else:
            s = s[:-3]
        return s
    
    elif s[-3:] == 'ier':
        s = s[:-3] + 'y'
        return s
            
    elif s[-2:] == 'er':
        if s in d:
            s = d[s]
        elif s[-3] == s[-4] and s[-5] in 'aeiou':
            s = s[:-3]
        else:
            s = s[:-2]
        return s

    elif s[-2:] == 'ed':
        if s[-3] == s[-4]:
            s = s[:-3]
        else:
            s = s[:-2]
        return s
    
    elif s[-4:] == 'iest':
        s = s[:-4] + 'y'
        return s
    
    elif s[-3:] == 'est':
        if len(s) == 4:
            s = s
        elif s[-4] == s[-5]:
            s = s[:-4]
        else:
            s = s[:-3]
        return s

    return s

def compare_dictionaries(d1,d2):
    """take two feature dictionaries d1 and d2 as inputs and compute and return their log similarity score"""
    if d1 == {}:
        return -50
    else:
        score = 0
        total = 0
        for key in d1:
            total += d1[key]
        for key in d2:
            if key in d1:
                score += d2[key] * math.log(d1[key]/total)
            else:
                score += d2[key] * math.log(0.5/total)
    return score 


class TextModel:
    """a data type for objects that model a body of text"""
    
    def __init__(self,model_name):
        
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.punctuation = {}
    
    def __repr__(self):
        """returns a string that includes the name of the model and
           the sizes of the dictionaries for each feature of the text"""
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        s += '  number of stems: ' + str(len(self.stems)) + '\n'
        s += '  number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'
        s += '  number of punctuations: ' + str(len(self.punctuation)) + '\n'
        return s
    
    def add_string(self,s):
        """adds a string of text s to the model by augmenting the feature 
           dictionaries defined in the constructor"""
        
        for word in s:
            if word[-1] == '.':
                if '.' not in self.punctuation:
                    self.punctuation['.'] = 1
                else:
                    self.punctuation['.'] += 1
            elif word[-1] == '?':
                if '?' not in self.punctuation:
                    self.punctuation['?'] = 1
                else:
                    self.punctuation['?'] += 1
            elif word[-1] == '!':
                if '!' not in self.punctuation:
                    self.punctuation['!'] = 1
                else:
                    self.punctuation['!'] += 1
                
        split = s.split()
        count = 0
        for c in split:
            if c[-1] not in '.?!':
                count += 1
            else:
                count += 1
                if count not in self.sentence_lengths:
                    self.sentence_lengths[count] = 1
                else: 
                    self.sentence_lengths[count] += 1
                count = 0
        if split[-1][-1] not in '.?!':
            if count not in self.sentence_lengths:
                self.sentence_lengths[count] = 1
            else:
                self.sentence_lengths[count] += 1
                
        word_list = clean_text(s)
        for w in word_list:
            if w in self.words:
                self.words[w] += 1
            else:
                self.words[w] = 1
            if len(w) not in self.word_lengths:
                self.word_lengths[len(w)] = 1
            else:
                self.word_lengths[len(w)] += 1
            if stem(w) not in self.stems:
                self.stems[stem(w)] = 1
            else:
                self.stems[stem(w)] += 1
            
    
    def add_file(self,filename):
        """adds all of the text in the file identified by filename to the model"""
        f = open(filename, 'r', encoding = 'utf8',errors = 'ignore')
        text = f.read()
        f.close()
        self.add_string(text)
    
    def save_model(self):
        """saves object by writing its various feature dictionaries to files"""
        
        file_name1 = self.name + '_' + 'words'
        f = open(file_name1,'w')
        f.write(str(self.words))
        f.close()
        
        file_name2 = self.name + '_' + 'word lengths'
        f_length = open(file_name2,'w')
        f_length.write(str(self.word_lengths))
        f_length.close()
        
        file_name3 = self.name + '_' + 'sentence lengths'
        f_sentence_length = open(file_name3,'w')
        f_sentence_length.write(str(self.sentence_lengths))
        f_sentence_length.close()
        
        file_name4 = self.name + '_' + 'stems'
        f_stems = open(file_name4,'w')
        f_stems.write(str(self.stems))
        f_stems.close()
        
        file_name5 = self.name + '_' + 'punctuation'
        f_punctuation = open(file_name5,'w')
        f_punctuation.write(str(self.punctuation))
        f_punctuation.close()
    
    def read_model(self):
        """reads the stored dictionaries for the called TextModel object and 
           assigns them to the attributes of the called TextModel"""
        
        file_name1 = self.name + '_' + 'words'
        f = open(file_name1,'r')
        d_str = f.read()
        f.close()
        d = dict(eval(d_str))
        self.words = d
        
        
        file_name2 = self.name + '_' + 'word lengths'
        f_lengths = open(file_name2,'r')
        d_str_length = f_lengths.read()
        f_lengths.close()
        d1 = dict(eval(d_str_length))
        self.word_lengths = d1
        
        file_name3 = self.name + '_' + 'sentence lengths'
        f_senlen = open(file_name3,'r')
        d_str_senlen = f_senlen.read()
        f_senlen.close()
        d2 = dict(eval(d_str_senlen))
        self.sentence_lengths = d2
        
        file_name4 = self.name + '_' + 'stems'
        f_stems = open(file_name4,'r')
        d_str_stems = f_stems.read()
        f_stems.close()
        d3 = dict(eval(d_str_stems))
        self.stems = d3
        
        file_name5 = self.name + '_' + 'punctuation'
        f_punc = open(file_name5,'r')
        d_str_punc = f_punc.read()
        f_punc.close()
        d4 = dict(eval(d_str_punc))
        self.punctuation = d4
    
    def similarity_scores(self,other):
        """computes and returns a list of log similarity scores measuring the similarity of self 
           and other"""
        words_score = compare_dictionaries(other.words,self.words)
        word_len_score = compare_dictionaries(other.word_lengths,self.word_lengths)
        word_stems = compare_dictionaries(other.stems, self.stems)
        word_sen_lengths = compare_dictionaries(other.sentence_lengths,self.sentence_lengths)
        word_punctuation = compare_dictionaries(other.punctuation, self.punctuation)
        sim_list = [words_score] + [word_len_score] + [word_stems] + [word_sen_lengths] + [word_punctuation]
        return sim_list
    
    def classify(self,source1,source2):
        """compares the called TextModel object to two other source TextModel objects and determines
           which of these other TextModels is the more likely source of the called TextModel"""
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        print('scores for',source1.name +': ',scores1)
        print('scores for',source2.name +': ',scores2)
        count1 = 0
        count2 = 0
        for i in range(len(scores1)):
            if scores1[i] > scores2[i]:
                count1 += 1 
            elif scores1[i] < scores2[i]:
                count2 += 1 
        if count1 > count2:
            print(self.name,'is more likely to have come from',source1.name)
        else:
            print(self.name,'is more likely to have come from',source2.name)

def run_tests():
    """ classifies model objects as belonging to one source text over the other """
    source1 = TextModel('Davidson')
    source1.add_file('Pete Davidson Source.txt')

    source2 = TextModel('Trump')
    source2.add_file('Trump Speech Source.txt')

    new1 = TextModel('Test1')
    new1.add_file('Pete Davidson Test.txt')
    new1.classify(source1, source2)
    
    new2 = TextModel('Test2')
    new2.add_file('Trump speech Test.txt')
    new2.classify(source1, source2)
    
    new3 = TextModel('Test3')
    new3.add_file('Eminem Test.txt')
    new3.classify(source1, source2)
    
    new4 = TextModel('Test4')
    new4.add_file('Good Will Hunting Test.txt')
    new4.classify(source1, source2)
    
    

                
        

            
        