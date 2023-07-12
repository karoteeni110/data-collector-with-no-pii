import logging
from pprint import pprint
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

class ComprehendDetect:
    """Encapsulates Comprehend detection functions."""
    def __init__(self, comprehend_client):
        """
        :param comprehend_client: A Boto3 Comprehend client.
        """
        self.comprehend_client = comprehend_client

    def detect_languages(self, text):
        """
        Detects languages used in a document.

        :param text: The document to inspect.
        :return: The list of languages along with their confidence scores.
        """
        try:
            response = self.comprehend_client.detect_dominant_language(Text=text)
            languages = response['Languages']
            logger.info("Detected %s languages.", len(languages))
        except ClientError:
            logger.exception("Couldn't detect languages.")
            raise
        else:
            return languages

    def detect_pii(self, text, language_code):
        """
        Detects personally identifiable information (PII) in a document. PII can be
        things like names, account numbers, or addresses.

        :param text: The document to inspect.
        :param language_code: The language of the document.
        :return: The list of PII entities along with their confidence scores.
        """
        try:
            response = self.comprehend_client.detect_pii_entities(
                Text=text, LanguageCode=language_code)
            entities = response['Entities']
            logger.info("Detected %s PII entities.", len(entities))
        except ClientError:
            logger.exception("Couldn't detect PII entities.")
            raise
        else:
            return entities

if __name__ == "__main__":
    demo_size = 3
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    session = boto3.Session(profile_name='saml')
    comp_client = session.client('comprehend')
    comp_detect = ComprehendDetect(comp_client)
    
    sample_text = """Managing Your Accounts Primary Branch Canton John Doe Phone Number 443-573-4800 123 Main StreetBaltimore, MD 21224
Online Banking HowardBank.com  Telephone 1-877-527-2703 Bank 3301 Boston Street, Baltimore, MD 21224"""
    # Expected detection:
    # Managing Your Accounts Primary Branch ****** ******** Phone Number ************ **********************************
    # Online Banking **************  Telephone ************** Bank ***************************************     
   
    print("Detecting languages.")
    languages = comp_detect.detect_languages(sample_text)
    pprint(languages)
    lang_code = languages[0]['LanguageCode']
    pprint(lang_code)

    print("Detecting entities.")
    entities = comp_detect.detect_pii(sample_text, lang_code)
    print(f"The first {demo_size} are:")
    pprint(entities[:demo_size])
    
    print("Sample text:")
    pprint(sample_text)
    for entity in entities[:demo_size]:
        beginOffset, endOffset = entity["BeginOffset"], entity["EndOffset"]
        pii = sample_text[beginOffset:endOffset]
        print(pii)
        print()
        
    
 