import sys
import operator

infile = sys.argv[1]

lines = [l.strip() for l in open(infile, 'r').readlines()]

expected_number = 1
index = 0 

stats_dict = {}
full_transcript = []

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
        full_transcript.append(transcript)
        """
        split_transcript = transcript.split()
        for w in split_transcript:
            w = w.lower()
            if w not in stats_dict:
                stats_dict[w] = 0
            stats_dict[w] += 1
        """
    index += 1
#print full_transcript

from nltk.tokenize import RegexpTokenizer

tokenizer = RegexpTokenizer(r'\w+')
processed_text = tokenizer.tokenize(str(full_transcript))

final_text = []

for w in processed_text:
            
    w = w.lower()
    final_text.append(w)
    if w not in stats_dict:
        stats_dict[w] = 0
    stats_dict[w] += 1

print final_text

sorted_stats = sorted(stats_dict.items(), key=operator.itemgetter(1), reverse=True)
print sorted_stats






        
