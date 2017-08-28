# Basic-Sentiment-Analysis-MrJob-Twitter
Sentiment Analysis using dictionary implemented in MrJob. It might be executed in local or HDFS enviroments (such as Hadoop or AWS).
Real tweets are been download through link:https://dev.twitter.com/rest/public[Twitter_API]. Steps taken:
- To get information of location and selecting tweets with USA location.
- To check if state is real (States-USA.csv) and transform in correct format.
- To consult diccionary (AFINN-111.txt) for transforming each word in a number wich getting sentiment of word.
- To map each tweet as (state, sentiment_value)
- To Reduce each tweet by state. For each state it computes number of record and it solves (total_sentiment_value,total_record,mean_of_state)


For executions in local:
```
python Twitter_MR.py data/data_example.json > data/output_example.txt
```

For executions in AWS:
```
python Twitter_MR.py -r emr "path_s3_tweets" --output-dir="output_s3_AWS" --conf-path mrjob.conf --states="path of States-USA.csv" --dic="path of AFINN-111.txt"
```
