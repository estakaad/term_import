import requests
import json
import utils.log_config

logger = utils.log_config.get_logger()

def get_word_id(session, base_url, crud_role_dataset, dataset, word, lang):
    parameters = {'crudRoleDataset': crud_role_dataset}
    try:
        res = session.get(f'{base_url}/api/word/ids/{word}/{dataset}/{lang}', params=parameters, timeout=5)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error for word '{word}': {e}")
        return None


def process_concepts(session, concepts, base_url, crud_role_dataset, dataset, concepts_with_word_ids_list, words_without_id, words_with_more_than_one_id):
    for concept in concepts:
        for word in concept.get('words', []):
            word_ids = get_word_id(session, base_url, crud_role_dataset, dataset, word['valuePrese'], word['lang'])
            if word_ids:
                if len(word_ids) == 1:
                    word['wordId'] = word_ids[0]
                    logger.info(f'1 word ID found in {dataset} for word {word["valuePrese"]}: {word["wordId"]}')
                    word.pop('valuePrese', None)
                    word.pop('lang', None)
                    word.pop('wordTypeCodes', None)
                elif len(word_ids) > 1:
                    logger.info(f'{len(word_ids)} word IDs found in {dataset} for word {word["valuePrese"]}')
                    words_with_more_than_one_id.append(word['valuePrese'])
            else:
                logger.info(f'0 word IDs found in {dataset} for word {word["valuePrese"]}')
                words_without_id.append(word['valuePrese'])
        concepts_with_word_ids_list.append(concept)


def update_word_ids(session, concepts_without_word_ids, concepts_with_word_ids, words_without_id_file, words_with_more_than_one_id_file, base_url, crud_role_dataset, dataset):
    with open(concepts_without_word_ids, 'r', encoding='utf-8') as file:
        concepts = json.load(file)

    concepts_with_word_ids_list = []
    words_without_id = []
    words_with_more_than_one_id = []
    logger.info('Base URL: ' + base_url)
    logger.info('Dataset: ' + dataset)
    logger.info('Starting to process concepts.')

    process_concepts(session, concepts, base_url, crud_role_dataset, dataset, concepts_with_word_ids_list, words_without_id, words_with_more_than_one_id)

    logger.info('Saving the results.')

    with open(concepts_with_word_ids, 'w', encoding='utf-8') as file:
        json.dump(concepts_with_word_ids_list, file, indent=4, ensure_ascii=False)

    with open(words_without_id_file, 'w', encoding='utf-8') as f:
        json.dump(words_without_id, f, ensure_ascii=False, indent=4)

    with open(words_with_more_than_one_id_file, 'w', encoding='utf-8') as f:
        json.dump(words_with_more_than_one_id, f, ensure_ascii=False, indent=4)


def get_word(session, id, crud_role_dataset, base_url):
    parameters = {'crudRoleDataset': crud_role_dataset}

    endpoint = f"{base_url}/api/lex-word/details/{id}/{crud_role_dataset}"

    try:
        res = session.get(endpoint, params=parameters, timeout=5)

        if res.status_code != 200:
            logger.error(f"Failed to get word. Received {res.status_code} status code.")
            return None

        return res.json()

    except Exception as e:
        logger.error(f"Exception occurred while getting word: {e}")
        return None


def get_all_words(session, word_ids_file, words_with_all_data, base_url, crud_role_dataset):
    with open(word_ids_file, 'r', encoding='utf-8') as file:
        word_ids = json.load(file)

    words = []

    logger.info('Starting to fetch words...')

    for word_id in word_ids:
        word_details = get_word(session, word_id, crud_role_dataset, base_url)

        if word_details is not None:
            logger.info(f"Fetched word with ID {word_details['wordId']}")
            words.append(word_details)
        else:
            logger.warning(f"Word fetched but didn't receive wordId: {word_id}")

    logger.info('Saving the results.')

    with open(words_with_all_data, 'w', encoding='utf-8') as file:
        json.dump(words, file, ensure_ascii=False, indent=4)


def save_word(session, word, crud_role_dataset, base_url):
    parameters = {'crudRoleDataset': crud_role_dataset}
    endpoint = base_url + '/api/lex-word/save'

    try:
        res = session.post(endpoint, params=parameters, json=word, timeout=5)

        if res.status_code != 200:
            logger.error(f"Failed to save word {word}. Received {res.status_code} status code.")
            return None

        return res.json().get('id')

    except Exception as e:
        logger.error(f"Exception occurred while saving word: {e}")
        return None

def save_words(session, words_with_details, crud_role_dataset, base_url):
    with open(words_with_details, 'r', encoding='utf-8') as f:
        data = json.load(f)

    logger.info('Starting to process words.')

    for word in data:
        response = save_word(session, word, crud_role_dataset, base_url)

        if response:
            logger.info(f'Saved word {response}')
        else:
            logger.warning(f"No response.")

    logger.info('Finished saving words.')