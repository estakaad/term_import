import requests
import json
import utils.log_config
import copy
from time import sleep
import threading

logger = utils.log_config.get_logger()


def process_concepts(data_subset, crud_role_dataset, api_key, base_url, concepts_saved_list, concepts_not_saved_list, results_lock):
    for concept in data_subset:
        concept_copy = copy.copy(concept)
        concept_id = save_concept(concept_copy, crud_role_dataset, api_key, base_url)

        with results_lock:
            if concept_id:
                concept_copy['id'] = concept_id
                concepts_saved_list.append(concept_copy)
            else:
                concepts_not_saved_list.append(concept_copy)


def import_concepts(concepts_with_word_ids, concepts_saved, concepts_not_saved, crud_role_dataset, api_key, base_url, num_threads):
    with open(concepts_with_word_ids, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Calculate the size of each part based on the number of threads
    part_size = len(data) // num_threads
    threads = []
    results_lock = threading.Lock()
    concepts_saved_list = []
    concepts_not_saved_list = []

    logger.info(f'Start creating {num_threads} threads.')

    for i in range(num_threads):
        start_index = i * part_size
        end_index = None if i == (num_threads - 1) else start_index + part_size
        data_part = data[start_index:end_index]

        thread = threading.Thread(target=process_concepts, args=(data_part, crud_role_dataset, api_key, base_url, concepts_saved_list, concepts_not_saved_list, results_lock))
        threads.append(thread)

    logger.info('Starting threads.')

    for thread in threads:
        thread.start()

    logger.info('Waiting for all threads to finish.')

    for thread in threads:
        thread.join()

    logger.info('Saving the results.')

    with open(concepts_saved, 'w', encoding='utf-8') as f:
        json.dump(concepts_saved_list, f, ensure_ascii=False, indent=4)

    with open(concepts_not_saved, 'w', encoding='utf-8') as f:
        json.dump(concepts_not_saved_list, f, ensure_ascii=False, indent=4)


def save_concept(concept, crud_role_dataset, api_key, base_url):
    header = {"ekilex-api-key": api_key}
    parameters = {'crudRoleDataset': crud_role_dataset}

    try:
        res = requests.post(
            base_url + "/api/term-meaning/save",
            params=parameters,
            json=concept,
            headers=header,
            timeout=5
        )

        if res.status_code != 200:
            logger.error(f"Failed to save concept. Received {res.status_code} status code.")
            return None

        response_json = res.json()
        concept_id = response_json.get('id')
        if concept_id:
            logger.info(f'Created concept with ID {concept_id}')
            return concept_id

    except Exception as e:
        logger.error(f"Exception occurred while saving concept: {e}")
        return None
