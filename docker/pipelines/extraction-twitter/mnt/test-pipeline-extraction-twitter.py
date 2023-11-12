# ===================================== IMPORTS ========================================
from pipeline_extraction_twitter import PipelineExtractionTwitter

# ==================================== RUN TESTS =======================================
if __name__ == "__main__":
    Pipeline = PipelineExtractionTwitter()
    topic = "réforme des retraites"
    tweets_content = Pipeline.RunTwitterExtraction(topic = topic)
    Pipeline.RunPushToMongo(tweets_content)
