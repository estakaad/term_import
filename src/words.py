import requests
import json
import utils.log_config


logger = utils.log_config.get_logger()

def update_word_ids(concepts_without_word_ids, concepts_with_word_ids, words_without_id_file, words_with_more_than_one_id_file,
                    api_key, base_url, crud_role_dataset, dataset):

    with open(concepts_without_word_ids, 'r', encoding='utf-8') as file:
        concepts = json.load(file)

    concepts_with_word_ids_list = []
    words_without_id = []
    words_with_more_than_one_id = []

    for concept in concepts:
        for word in concept.get('words', []):
            try:
                word_ids = get_word_id(api_key, base_url, crud_role_dataset, dataset, word['value'], word['lang'])
            except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
                logger.info(f"Connection timed out for {word['value']}. Moving on to the next word.")
                continue
            if word_ids:
                if len(word_ids) == 1:
                    word['wordId'] = word_ids[0]
                    logger.info(f'Word \'{word["value"]}\' ({word["lang"]}) with ID {word_ids[0]} has one instance in \'{dataset}\'')
                elif len(word_ids) > 1:
                    words_with_more_than_one_id.append(word['value'])
                    logger.info(f'Word \'{word["value"]}\' ({word["lang"]}) has more than one instances in \'{dataset}\'')
            else:
                words_without_id.append(word['value'])
                logger.info(f'Word \'{word["value"]}\' ({word["lang"]}) does not have instances in \'{dataset}\'')

        concepts_with_word_ids_list.append(concept)

    with open(concepts_with_word_ids, 'w', encoding='utf-8') as file:
        json.dump(concepts_with_word_ids_list, file, indent=4, ensure_ascii=False)

    with open(words_without_id_file, 'w', encoding='utf-8') as f:
        json.dump(words_without_id, f, ensure_ascii=False, indent=4)

    with open(words_with_more_than_one_id_file, 'w', encoding='utf-8') as f:
        json.dump(words_with_more_than_one_id, f, ensure_ascii=False, indent=4)


def get_word_id(api_key, base_url, crud_role_dataset, dataset, word, lang):

    header = {"ekilex-api-key": api_key}

    parameters = {
        'crudRoleDataset': crud_role_dataset
    }

    res = requests.get(f'{base_url}/api/word/ids/{word}/{dataset}/{lang}',
        params=parameters,
        headers=header,
        timeout=5)

    if res.status_code == 200:
        try:
            response = res.json()
            return response
        except ValueError:
            print(f"Error decoding JSON for word: {word} in dataset: {dataset} for language: {lang}")
            return None
    else:
        return None