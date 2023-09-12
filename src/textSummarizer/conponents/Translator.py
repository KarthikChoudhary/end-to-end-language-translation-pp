import logging
import time
from src.textSummarizer.exceptions import TranslationServiceException, DatabaseException
from src.textSummarizer.logging import logger


class TranslatorService:
    def get_translation(self, db, text, source_lang='en', target_lang='fr'):
        """
        Get available translation from the database or return None.

        :param db: MySQLDatabase instance.
        :param text: Text to be translated.
        :param source_lang: Source language code.
        :param target_lang: Target language code.

        :return: Translation result or None if not found.
        """
        try:
            logger.info("Fetching existing translation from the database")

            query = f"""SELECT
                            fs.french_sentence AS translated_text
                        FROM
                            english_sentences AS es
                        JOIN french_sentences AS fs ON
                            es.french_sentence_id = fs.id
                        WHERE
                            es.english_sentence = '{text}';"""

            result = db.execute_query(query)
            logger.info(f"Result of {query}: is {result}")

            if result:
                logger.info(f"Translation retrieved from the database: {result}")
                return result
            else:
                logger.info("Translation not found in the database")
                return None

        except Exception as e:
            logging.error(f"Error in get_translation: {e}")
            raise DatabaseException("Database error")

    def perform_translation(self, text, source_lang, target_lang):
        """
        Perform text translation using NLP.
        :param text: Text to be translated.
        :param source_lang: Source language code.
        :param target_lang: Target language code.
        :return: Translation result.
        """
        try:
            logger.info(f"Performing translation from {source_lang} to {target_lang} on the text: {text}")
            translated_text = 'traduction factice'  # Dummy translation
            # TODO - Perform translation here
            logger.info(f"Translation performed successfully and the translated text is: {translated_text}")
            return translated_text
        except Exception as e:
            print(f"Error in perform_translation: {e}")
            raise TranslationServiceException("Translation service error")

    def save_translation(self, db, text, translation_text):
        """
        Save the translation in database.
        :param db: MySQLDatabase instance.
        :param text: Text to be translated.
        :param source_lang: Source language code.
        :param target_lang: Target language code.
        :param translation_text: Translation result.
        """
        try:
            uid = int(time.time())  # Unique Id for each translation
            logger.info(f"Unique ID created for translation: {uid}")

            # Add French translation to database
            logger.info("Adding French translation to the database")
            add_fr_sentence_query = "INSERT INTO french_sentences (id, french_sentence) VALUES (%s, %s);"
            fr_params = (uid, translation_text)
            db.execute_query(add_fr_sentence_query, fr_params)
            logger.info("French translation added to the database")

            # Add English sentence to database
            logger.info("Adding the original English sentence to database")
            add_en_sentence_query = "INSERT INTO english_sentences (id, english_sentence, french_sentence_id) VALUES (%s, %s, %s);"
            en_params = (uid, text, uid)
            db.execute_query(add_en_sentence_query, en_params)
            logger.info("English sentence added to the database")

            # commit the data
            db.connection.commit()
            logger.info("Translation saved to the database")

        except Exception as e:
            logging.error(f"Error in save_translation: {e}")
            raise DatabaseException("Database error")
