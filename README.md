# Basic-Sentiment-Analysis-MrJob-Twitter
Project developed to make an sentiment analysis using dictionary implemented with MrJob with a map-reduce model. It can be executed locally or in HDFS enviroments (such as Hadoop or AWS). Real tweets are been downloaded through [Twitter API](https://dev.twitter.com/rest/public).

## Stages of project
Steps dones:
- Information of location was obtained and tweets with USA location were selected.
- State gather must be real (States-USA.csv).
- Dictionary (AFINN-111.txt) with vocabulary was consulted for transforming each word in a number wich getting sentiment of words.
- Mapper stage: each tweet is mapped as (state, sentiment_value)
- Mapper stage: each tweet is reduced by state. For each state it computes number of record getting (total_sentiment_value,total_record,mean_of_state)

## Execution Examples
For executions in local:
```
python Twitter_MR.py data/data_example.json > data/output_example.txt
```
For AWS executions using EMR:
```
python Twitter_MR.py -r emr "path_s3_tweets" --output-dir="output_s3_AWS" --conf-path mrjob.conf --states="path of States-USA.csv" --dic="path of AFINN-111.txt"
```

Furthermore, for AWS execution mrjob.conf is necessary. It must be fill with your own account data.

