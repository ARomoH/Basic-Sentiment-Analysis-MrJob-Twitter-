# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 18:51:44 2017

@author: ARH
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Dec 07 12:23:15 2016

"""

import json
import csv
from mrjob.job import MRJob
from mrjob.step import MRStep

def filter_tweets(line):
    # (Retweets) If there is not retweet field, it produces a error for handling a exepction
    try:
        retweet = line.get('retweeted_status').get('place')
    except:
        retweet = None
    # All tweets has not location information
    if retweet is not None:
        retweet = retweet.get('country_code')
        # El país debe ser Estados Unidos
        if retweet != "US":
            return None
    # (Tweets) Same proccess as Retweets.
    tweet = line.get('place')
    if tweet is not None:
        tweet = tweet.get('country_code')
        if tweet != "US":
            return None
    else:
        return None
        
    
   # Tweet Language must be English
    if line.get('lang') != "en":
        return None

    # Checking if states of location are correct
    location = []
    location.append(line.get('place').get('full_name'))
    list_output = []
    # If there is retweet information it is also gathering
    if retweet is not None:
        location.append(line.get('retweeted_status').get('place').get('full_name'))
    for loc in location:
        # It was found some case where names are separated by spaces (no by commas)
        try:
            c = loc.split(',')
            codigo = c[len(c)-1].strip()
            nombre = loc.split(',')[0].strip().lower()
        except:
            c = loc.split(' ')
            codigo = c[len(c)-1].strip()
            nombre = loc.split(' ')[0].strip().lower()
        if codigo in usa_states:
            # Return idTweet, state name and text
            list_output.append([usa_states[codigo], line.get('text')])
        else:
            # In some cases it can be found state name as code (2 capital letters)
            if nombre in usa_states.values():
                list_output.append([nombre, line.get('text')])

    if len(list_output) == 0:
        return None
    else:
        return list_output
    
def tweet_value(line):
    tweet = line.strip().lower()
    sum_values = 0
    for word in tweet.split():
        if word in word_value:
            sum_values += word_value[word]

    return sum_values
    
class TweetCount(MRJob):

   def configure_options(self):
      # Options for executions in HDFS enviroments
      super(TweetCount, self).configure_options()
      self.add_file_option('--states')
      self.add_file_option('--dic')

   def steps(self):
      return[
         MRStep(mapper=self.mapper, reducer=self.reducer)
      ]
    
   def mapper(self, _, line):
      try:
          data = json.loads(line)
          list_tweets = filter_tweets(data)
          if list_tweets is not None:
              # Every tweet can get information of location of tweet and retweet
              for l in list_tweets:
                  # A tweet can get several words within dictionary of States and they must be weighted
                  value = tweet_value(l[1])
                  yield(l[0], value)
      except:
          pass
              
     
   def reducer(self, key, values):
      total = 0
      suma = 0
      for v in values:
          total += 1
          suma += v
      yield key, (suma, total, float(suma)/float(total))
      
if __name__ == '__main__':
   usa_states = dict()
   with open('data/States-USA.csv', 'r') as csvfile:
       reader = csv.reader(csvfile)
       for row in reader:
           usa_states.setdefault(row[1],row[0])
           
   word_value = dict()
   with open('data/AFINN-111.txt', 'r') as tsvfile:
      reader_2 = csv.reader(tsvfile, delimiter='\t')
      for row in reader_2:
         word_value.setdefault(row[0],int(row[1]))
   
   TweetCount.run()
