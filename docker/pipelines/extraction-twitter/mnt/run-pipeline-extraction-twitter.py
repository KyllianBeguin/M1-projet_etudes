# ===================================== IMPORTS ========================================
# To run the pipeline
from pipeline_extraction_twitter import PipelineExtractionTwitter

# To log the activity
import logging

# ==================================== RUN TESTS =======================================
if __name__ == "__main__":
    FORMAT = '%(asctime)s %(message)s'
    logging.basicConfig(format=FORMAT)
    logger = logging.getLogger('pipeline')
    logger.setLevel('INFO')
    logger.info("Started Tweet extraction")

    Pipeline = PipelineExtractionTwitter()
    topic = "réforme des retraites"
    tweets_content = Pipeline.RunTwitterExtraction(topic = topic)
    pushed = Pipeline.RunPushToMongo(tweets_content)

    if pushed:
        logger.info("Finished Tweet extraction")
    else:
        logger.info("Not tweets to push")
