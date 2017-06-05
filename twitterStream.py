from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import operator
import numpy as np
import matplotlib.pyplot as plt


def main():
    conf = SparkConf().setMaster("local[2]").setAppName("Streamer")
    sc = SparkContext(conf=conf)
    ssc = StreamingContext(sc, 10)   # Create a streaming context with batch interval of 10 sec
    ssc.checkpoint("checkpoint")

    pwords = load_wordlist("positive.txt")
    nwords = load_wordlist("negative.txt")
   
    counts = stream(ssc, pwords, nwords, 100)
    make_plot(counts)


def make_plot(counts):
    """
    Plot the counts for the positive and negative words for each timestep.
    Use plt.show() so that the plot will popup.
    """
    import matplotlib.pyplot as plt
    
    pos = []
    neg = []
    for m in counts:
        if(len(m)!= 0):
            pos.append(m[0][1])
            neg.append(m[1][1])
    line1 = plt.plot(pos,label="Positive")
    line2 = plt.plot(neg,label="Negative")
    ymax = max(max(pos),max(neg)) + 60
    step = int(ymax/10)
    ymin = min(min(pos),min(neg)) - 40
    plt.xticks(np.arange(0,12,1.0))
    plt.yticks(np.arange(ymin,ymax,step))
    #start, end = ax.get_xlim()
    #ax.xaxis.set_ticks(np.arange(start, end, stepsize))
    plt.legend()
    plt.ylabel('Word Count')
    plt.xlabel('Time Step')
    plt.show()
    plt.savefig('plot.png')
    



def load_wordlist(filename):
    """ 
    This function should return a list or set of words from the given filename.
    """
    
    with open(filename) as f:
        content = f.readlines()
    content = [x.strip("\n") for x in content] 
    return content


def cnt(word, pwords,nwords):
    #print "HIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII"
    p = 0 
    n = 0
    if word in pwords:
        return ("positive",1)
    elif word in nwords:
        return ("negative",1)
    else:
        return ("none",1)

def updateFunc(val,runningCount):
    if runningCount is None:
        runningCount = 0
    return sum(val,runningCount)
    

def stream(ssc, pwords, nwords, duration):
    kstream = KafkaUtils.createDirectStream(
        ssc, topics = ['twitterstream'], kafkaParams = {"metadata.broker.list": 'localhost:9092'})
    tweets = kstream.map(lambda x: x[1].encode("ascii","ignore"))
    
    
    words = tweets.flatMap(lambda x: x.split(" "))
    pairs = words.map(lambda word: cnt(word,pwords,nwords))
    wordCounts = pairs.reduceByKey(lambda x,y: x + y)
    wordCounts = wordCounts.filter(lambda x: "positive" in x[0] or "negative" in x[0]) 
    
    runningCounts = wordCounts.updateStateByKey(updateFunc)
    
    #wordCounts.pprint()
    runningCounts.pprint()
    #words = twtlst.map(lambda y:cnt(y,pwords,nwords))
    
    # Each element of tweets will be the text of a tweet.
    # You need to find the count of all the positive and negative words in these tweets.
    # Keep track of a running total counts and print this at every time step (use the pprint function).
    
           
    
    # Let the counts variable hold the word counts for all time steps
    # You will need to use the foreachRDD function.
    # For our implementation, counts looked like:
    #   [[("positive", 100), ("negative", 50)], [("positive", 80), ("negative", 60)], ...]
    counts = []
    #counts.append([("positive",positive),("negative",negative)])
    wordCounts.foreachRDD(lambda t,rdd: counts.append(rdd.collect()))
    
    ssc.start()                         # Start the computation
    ssc.awaitTerminationOrTimeout(duration)
    ssc.stop(stopGraceFully=True)

    print counts
    return counts


if __name__=="__main__":
    main()
