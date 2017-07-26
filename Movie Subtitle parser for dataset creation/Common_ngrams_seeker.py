import os
import sys
import operator
import numpy as np

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

def get_tokens_with_time_from_srt(infile):
    lines = [l.strip() for l in open(infile, 'r').readlines()]
    index = 0 
    stats_dict = {}
    all_tokens = []
    time_of_word = []
    tokenizer = RegexpTokenizer(r"\w+'?\w{,2}")
    while True:
        if index >= len(lines):
            break
        line = lines[index]
        buffer_ = []
        while line!="":
            buffer_.append(line)
            index += 1
            if index >= len(lines):
                break
            line = lines[index]
        if len(buffer_)!=0:
            number = buffer_[0]
            duration = buffer_[1]
            transcript = " ".join(buffer_[2:])
            tokens = tokenizer.tokenize(str(transcript.lower()))
            time_of_word += [duration] * len(tokens)
            all_tokens += tokens
        index += 1
    return all_tokens, time_of_word

def get_all_ngrams_with_time_from_tokens(tokens, timeinfo, n=2):
    ngram_list = []
    timeinfo_list = []
    for i in range(len(tokens)-n):
        ngram = ' '.join(tokens[i:i+n])
        ngram_list.append(ngram)
        timeinfo_list.append(timeinfo[i].split('-->')[0] + '-->' + timeinfo[i+n-1].split('-->')[1])
    return ngram_list, timeinfo_list


if __name__=='__main__':
    
    subtitle_dir='subtitle_movies'
    subtitle_files= [os.path.join(subtitle_dir, f) for f in os.listdir(subtitle_dir)]

    np.random.shuffle(subtitle_files)
    
    j = 0
    while ((j+4) < len(subtitle_files)):

        count=1
        prev_ngram_list = []
    
        for i in subtitle_files[j:j+5]:
           
            print i, '\n'
            infile = i
            tokens, timeinfo = get_tokens_with_time_from_srt(infile)
            ngrams, ngram_timeinfo = get_all_ngrams_with_time_from_tokens(tokens, timeinfo, n=5)
            
            ngram_info = zip(ngrams, ngram_timeinfo)

            if count == 1 :
                prev_ngram_list = ngram_info
                count += 1
                continue
            
            common_tuple_list = []
            common_timeinfo_list = []
            
            for ngram1 in prev_ngram_list:
                for ngram2, t2 in ngram_info:
                    flag = 0
                    if ngram1[0] == ngram2:
                        for i, item in enumerate(common_tuple_list):
                            #print i,item
                            if item[0] == ngram2 :
                                common_tuple_list[i] = item + (t2,)
                                flag = 1
                                break
                        if flag == 0 :
                            common_tuple_list.append(ngram1 + (t2,))
            

            prev_ngram_list = common_tuple_list
            
        print 'final list \n'
               
        for x in prev_ngram_list :
                
            print x, '\n'
        
        print 'Done!'
        
        j = j+5
    

