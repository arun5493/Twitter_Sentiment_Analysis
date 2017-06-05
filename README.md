# Twitter_Sentiment_Analysis
### Basic Twitter Sentiment Analytics using Apache Spark Streaming APIs and Python
Python application for sentiment analysis on live twitter feed using Apache Spark, Kafka


### Summary
In this project, we learned about processing live data streams using Spark’s streaming APIs and Python. We performed a basic sentiment analysis of realtime tweets. In addition, we also got a basic introduction to Apache Kafka, which is a queuing service for data streams.
 
### Background
In this project, we also processed streaming data in real time. One of the first requirements was to get access to the streaming data; in this case, realtime tweets. Twitter provides a very convenient API to fetch tweets in a streaming manner. (Documentation link can be found [here](https://dev.twitter.com/streaming/overview))
In addition, we also used Kafka to buffer the tweets before processing. Kafka provides a distributed queuing service which can be used to store the data when the data creation rate is more than processing rate. It also has several other uses. (Documentation link can be found [here](https://kafka.apache.org/documentation.html#gettingStarted))

### Project Setup

##### Installing Required Python Libraries
We have provided a text file containing the required python packages: requirements.txt.
To install all of these at once, simply run (only missing packages will be installed):
```
$ sudo pip install -r requirements.txt
```


##### Installing and Initializing Kafka
Download and extract the latest binary from https://kafka.apache.org/downloads.html

Start zookeeper service:
$ bin/zookeeper -server -start.sh config/zookeeper.properties

Start kafka service:
$ bin/kafka -server -start.sh config/server.properties

Create a topic named twitterstream in kafka:
$ bin/kafka -topics.sh --create --zookeeper localhost:2181 --replication-factor 1
--partitions 1 --topic twitterstream




### Project Requirements
For the project, in file twitterStream.py, the function to write the running total count of the number of positive and negative words that have been tweeted is included. In addition, the total positive and negative word counts for each timestep have been plotted. 
The word lists for [positive words](http://www.unc.edu/~ncaren/haphazard/positive.txt) and [negative words](http://www.unc.edu/~ncaren/haphazard/negative.txt) were given in the p ositive.txt and negative.txt files respectively.
 
### load_wordlist(filename)
This function is used to load the positive words from p ositive.txt and the negative words from negative.txt . This function returns the words as a list or set.
 
### stream(ssc, pwords, nwords, duration)
This is the main streaming function consisting of several steps that you must complete. There is skeleton code for starting the stream, getting the tweets from kafka, and stopping the stream. The intermediate steps of taking the streamed tweets and finding the number of positive and negative words were completed. 
The tweets variable is a DStream object on which we can perform similar [transformations](http://spark.apache.org/docs/latest/streaming-programming-guide.html#transformations-on-dstreams) that we could transform to an RDD. Currently, tweets consists of rows of strings, with each row representing one tweet. This structure can be viewed by using the [pprint function](http://spark.apache.org/docs/latest/streaming-programming-guide.html#output-operations-on-dstreams) : tweets.pprint(). 
We want to combine the positive word counts together and to combine the negative word counts together. Therefore, rather than mapping each word to (word, 1) (as is done in the example), you can map each word to (“positive”, 1) or (“negative”, 1) depending on which class that word belongs. Then, the counts can be aggregated using the [reduceByKey](http://spark.apache.org/docs/latest/streaming-programming-guide.html#transformations-on-dstreams) function to get the total counts for “positive” and the total counts for “negative”. 
To get the running total, we use the [updateStateByKey](http://spark.apache.org/docs/latest/streaming-programming-guide.html#transformations-on-dstreams) function (more details [here](http://spark.apache.org/docs/latest/streaming-programming-guide.html#updatestatebykey-operation)). It is this DStream (the one with the running totals) that we need to output using the pprint function. The other DStream (the one that doesn’t store the running total) can be used to make the plot that shows the total counts at each time step. However, we first must convert the DStream into something useable. To do this, we use the [foreachRDD](http://spark.apache.org/docs/latest/streaming-programming-guide.html#output-operations-on-dstreams) function. With this function, we can loop over the sequence of RDDs of that DStream object and get the actual values. 

### make_plot(counts).
In this function, we use the matplotlib (Tutorial link - [here](http://matplotlib.org/users/pyplot_tutorial.html)) to plot the total word counts at each time step. This information is stored in the output of your stream function (counts) . 


### Plot for Positive and Negative words
![Alt text](plot.png 'Plot')
