import requests
import json
import utils.log_config

logger = utils.log_config.get_logger()

def get_word_id(session, api_key, base_url, crud_role_dataset, dataset, word, lang):
    header = {"ekilex-api-key": api_key}
    parameters = {'crudRoleDataset': crud_role_dataset}
    try:
        res = session.get(f'{base_url}/api/word/ids/{word}/{dataset}/{lang}', params=parameters, headers=header, timeout=5)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error for word '{word}': {e}")
        return None

def process_concepts(session, concepts, api_key, base_url, crud_role_dataset, dataset, concepts_with_word_ids_list, words_without_id, words_with_more_than_one_id):
    for concept in concepts:
        for word in concept.get('words', []):
            word_ids = get_word_id(session, api_key, base_url, crud_role_dataset, dataset, word['valuePrese'], word['lang'])
            if word_ids:
                if len(word_ids) == 1:
                    word['wordId'] = word_ids[0]
                    logger.info(f'1 word ID found in {dataset} for word {word["valuePrese"]}: {word["wordId"]}')
                    word.pop('valuePrese', None)
                    word.pop('lang', None)
                elif len(word_ids) > 1:
                    logger.info(f'{len(word_ids)} word IDs found in {dataset} for word {word["valuePrese"]}')
                    words_with_more_than_one_id.append(word['valuePrese'])
            else:
                logger.info(f'0 word IDs found in {dataset} for word {word["valuePrese"]}')
                words_without_id.append(word['valuePrese'])
        concepts_with_word_ids_list.append(concept)

def update_word_ids(concepts_without_word_ids, concepts_with_word_ids, words_without_id_file, words_with_more_than_one_id_file, api_key, base_url, crud_role_dataset, dataset):
    with open(concepts_without_word_ids, 'r', encoding='utf-8') as file:
        concepts = json.load(file)

    concepts_with_word_ids_list = []
    words_without_id = []
    words_with_more_than_one_id = []

    session = requests.Session()

    logger.info('Starting to process concepts.')

    process_concepts(session, concepts, api_key, base_url, crud_role_dataset, dataset, concepts_with_word_ids_list, words_without_id, words_with_more_than_one_id)

    logger.info('Saving the results.')

    with open(concepts_with_word_ids, 'w', encoding='utf-8') as file:
        json.dump(concepts_with_word_ids_list, file, indent=4, ensure_ascii=False)

    with open(words_without_id_file, 'w', encoding='utf-8') as f:
        json.dump(words_without_id, f, ensure_ascii=False, indent=4)

    with open(words_with_more_than_one_id_file, 'w', encoding='utf-8') as f:
        json.dump(words_with_more_than_one_id, f, ensure_ascii=False, indent=4)
