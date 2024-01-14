import requests
import json
import utils.log_config
import copy

logger = utils.log_config.get_logger()

def save_concept(session, concept, crud_role_dataset, api_key, base_url):
    header = {"ekilex-api-key": api_key}
    parameters = {'crudRoleDataset': crud_role_dataset}

    try:
        res = session.post(
            f'{base_url}/api/term-meaning/save',
            params=parameters,
            json=concept,
            headers=header,
            timeout=5
        )

        if res.status_code != 200:
            logger.error(f"Failed to save concept. Received {res.status_code} status code.")
            return None

        return res.json().get('id')

    except Exception as e:
        logger.error(f"Exception occurred while saving concept: {e}")
        return None

def import_concepts(concepts_with_word_ids, concepts_saved, concepts_not_saved, crud_role_dataset, api_key, base_url):
    with open(concepts_with_word_ids, 'r', encoding='utf-8') as f:
        data = json.load(f)

    session = requests.Session()
    concepts_saved_list = []
    concepts_not_saved_list = []

    logger.info('Starting to process concepts.')

    for concept in data:
        concept_copy = copy.copy(concept)
        concept_id = save_concept(session, concept_copy, crud_role_dataset, api_key, base_url)

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