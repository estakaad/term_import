import requests
import json
import utils.log_config
import threading

logger = utils.log_config.get_logger()

def process_concepts(data_subset, api_key, base_url, crud_role_dataset, dataset, results_lock,
                     concepts_with_word_ids_list, words_without_id, words_with_more_than_one_id):
    try:
        for concept in data_subset:
            for word in concept.get('words', []):
                try:
                    word_ids = get_word_id(api_key, base_url, crud_role_dataset, dataset, word['value'], word['lang'])
                except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
                    logger.info(f"Connection timed out for {word['value']}. Moving on to the next word.")
                    continue
                if word_ids:
                    if len(word_ids) == 1:
                        word_value = word['value']
                        with results_lock:
                            word['wordId'] = word_ids[0]
                            word.pop('valuePrese', None)
                            word.pop('lang', None)

                        logger.info('1 word ID found in ' + dataset + ' for word ' + word_value + ': ' + str(word['wordId']))
                    elif len(word_ids) > 1:
                        logger.info(str(len(word_ids)) + ' word IDs found in ' + dataset + ' for word ' + word['value'])

                        with results_lock:
                            words_with_more_than_one_id.append(word['value'])
                else:
                    logger.info('0 word IDs found in ' + dataset + ' for word ' + word['value'])

                    with results_lock:
                        words_without_id.append(word['value'])

            with results_lock:
                concepts_with_word_ids_list.append(concept)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise


def update_word_ids(concepts_without_word_ids, concepts_with_word_ids, words_without_id_file, words_with_more_than_one_id_file, api_key, base_url, crud_role_dataset, dataset, num_threads):
    with open(concepts_without_word_ids, 'r', encoding='utf-8') as file:
        concepts = json.load(file)

    part_size = len(concepts) // num_threads
    threads = []
    results_lock = threading.Lock()
    concepts_with_word_ids_list = []
    words_without_id = []
    words_with_more_than_one_id = []

    logger.info(f'Start creating {num_threads} threads.')

    for i in range(num_threads):
        start_index = i * part_size
        end_index = None if i == (num_threads - 1) else start_index + part_size
        data_part = concepts[start_index:end_index]

        thread = threading.Thread(target=process_concepts, args=(data_part, api_key, base_url, crud_role_dataset, dataset, results_lock, concepts_with_word_ids_list, words_without_id, words_with_more_than_one_id))
        threads.append(thread)

    logger.info('Starting threads.')

    for thread in threads:
        thread.start()

    logger.info('Waiting for all threads to finish.')

    for thread in threads:
        thread.join()

    logger.info('Saving the results.')

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