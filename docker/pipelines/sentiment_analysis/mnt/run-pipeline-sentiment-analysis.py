# ===================================== IMPORTS ========================================
# To run the pipeline
from pipeline_sentiment_analysis import PipelineSentimentAnalysis

# To log the activity
import logging

# ==================================== RUN TESTS =======================================
if __name__ == "__main__":
    FORMAT = '%(asctime)s %(message)s'
    logging.basicConfig(format=FORMAT)
    logger = logging.getLogger('pipeline')
    logger.setLevel('INFO')
    logger.info("Started Sentiment analysis")

    pipeline = PipelineSentimentAnalysis()
    raw_tweets = pipeline.RunGetTweets()
    logger.info("Extracted tweets from raw data collection")

    processed_tweets = pipeline.RunSentimentAnalysis(raw_tweets)
    logger.info("Performed sentiment analysis")
    print(processed_tweets)
