import requests
import json
import utils.log_config
import copy

logger = utils.log_config.get_logger()


def get_concept(session, id, crud_role_dataset, base_url):
    parameters = {'crudRoleDataset': crud_role_dataset}

    endpoint = f"{base_url}api/term-meaning/details/{id}/{crud_role_dataset}"

    try:
        res = session.get(endpoint, params=parameters, timeout=5)

        if res.status_code != 200:
            logger.error(f"Failed to get concept. Received {res.status_code} status code.")
            return None

        return res.json()

    except Exception as e:
        logger.error(f"Exception occurred while getting concept: {e}")
        return None


def save_concept(session, concept, crud_role_dataset, base_url):
    parameters = {'crudRoleDataset': crud_role_dataset}
    endpoint = base_url + '/api/term-meaning/save'

    try:
        res = session.post(endpoint, params=parameters, json=concept, timeout=5)

        if res.status_code != 200:
            logger.error(f"Failed to save concept. Received {res.status_code} status code.")
            return None

        return res.json().get('id')

    except Exception as e:
        logger.error(f"Exception occurred while saving concept: {e}")
        return None

def import_concepts(session, concepts_with_word_ids, concepts_saved, concepts_not_saved, crud_role_dataset, base_url):
    with open(concepts_with_word_ids, 'r', encoding='utf-8') as f:
        data = json.load(f)

    concepts_saved_list = []
    concepts_not_saved_list = []

    logger.info('Starting to process concepts.')

    for concept in data:
        concept_copy = copy.copy(concept)
        concept_id = save_concept(session, concept_copy, crud_role_dataset, base_url)

        if concept_id:
            concept_copy['id'] = concept_id
            logger.info(f'Created concept with ID {concept_id}')
            concepts_saved_list.append(concept_copy)
        else:
            logger.warning(f"Concept saved but didn't receive an ID.")
            concepts_not_saved_list.append(concept_copy)

    logger.info('Saving the results.')

    with open(concepts_saved, 'w', encoding='utf-8') as f:
        json.dump(concepts_saved_list, f, ensure_ascii=False, indent=4)

    with open(concepts_not_saved, 'w', encoding='utf-8') as f:
        json.dump(concepts_not_saved_list, f, ensure_ascii=False, indent=4)

def get_all_concepts_from_dataset(session, concept_ids_file, concepts_with_all_data, base_url, crud_role_dataset):
    with open(concept_ids_file, 'r', encoding='utf-8') as file:
        concept_ids = json.load(file)

    concepts_from_dataset = []

    logger.info('Starting to fetch concepts...')

    for concept_id in concept_ids:
        concept_details = get_concept(session, concept_id, crud_role_dataset, base_url)

        if concept_details is not None and 'meaningId' in concept_details:
            logger.info(f"Fetched concept with ID {concept_details['meaningId']}")
            concepts_from_dataset.append(concept_details)
        else:
            logger.warning(f"Concept fetched but didn't receive meaningId: {concept_id}")

    logger.info('Saving the results.')

    with open(concepts_with_all_data, 'w', encoding='utf-8') as file:
        json.dump(concepts_from_dataset, file, ensure_ascii=False, indent=4)


def get_meaning(session, id, crud_role_dataset, base_url):
    parameters = {'crudRoleDataset': crud_role_dataset}

    endpoint = f"{base_url}/api/meaning/details/{id}/{crud_role_dataset}"

    try:
        res = session.get(endpoint, params=parameters, timeout=5)

        if res.status_code != 200:
            logger.error(f"Failed to get meaning. Received {res.status_code} status code.")
            return None

        return res.json()

    except Exception as e:
        logger.error(f"Exception occurred while getting meaning: {e}")
        return None

def get_all_meanings(session, concept_ids_file, meanings_with_all_data, base_url, crud_role_dataset):
    with open(concept_ids_file, 'r', encoding='utf-8') as file:
        meaning_ids = json.load(file)

    meanings = []
    logger.info(f'Base URL: {base_url}')
    logger.info(f'crud_role_dataset: {crud_role_dataset}')
    logger.info('Starting to fetch meanings...')

    for meaning_id in meaning_ids:

        meaning_details = get_meaning(session, meaning_id, crud_role_dataset, base_url)

        if meaning_details is not None and 'meaningId' in meaning_details:
            logger.info(f"Fetched meaning with ID {meaning_details['meaningId']}")
            meanings.append(meaning_details)
        else:
            logger.warning(f"Meaning fetched but didn't receive meaningId: {meaning_id}")

    logger.info('Saving the results.')

    with open(meanings_with_all_data, 'w', encoding='utf-8') as file:
        json.dump(meanings, file, ensure_ascii=False, indent=4)