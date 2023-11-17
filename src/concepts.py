import requests
import json
import utils.log_config
import copy
from time import sleep


logger = utils.log_config.get_logger()

def import_concepts(concepts_with_word_ids, concepts_saved, concepts_not_saved, crud_role_dataset, api_key, base_url):

    with open(concepts_with_word_ids, 'r', encoding='utf-8') as f:
        data = json.load(f)

    concepts_saved_list = []
    concepts_not_saved_list = []

    for concept in data:
        concept_copy = copy.copy(concept)

        try:
            concept_id = save_concept(concept_copy, crud_role_dataset, api_key, base_url)

            if concept_id:
                concept_copy['id'] = concept_id
                concepts_saved_list.append(concept_copy)
            else:
                concepts_not_saved_list.append(concept_copy)
                logger.error("Response code was 200 but no ID received.")

        except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError,
                requests.exceptions.Timeout, requests.exceptions.RequestException) as e:
            concepts_not_saved_list.append(concept)
            logger.exception("Error: %s.", e)
            break

    with open(concepts_saved, 'w', encoding='utf-8') as f:
        json.dump(concepts_saved_list, f, ensure_ascii=False, indent=4)

    with open(concepts_not_saved, 'w', encoding='utf-8') as f:
        json.dump(concepts_not_saved_list, f, ensure_ascii=False, indent=4)


def save_concept(concept, crud_role_dataset, api_key, base_url):

    header = {"ekilex-api-key": api_key}

    parameters = {
        'crudRoleDataset': crud_role_dataset
    }

    retries = 3

    while retries > 0:
        try:
            res = requests.post(
                base_url + "/api/term-meaning/save",
                params=parameters,
                json=concept,
                headers=header,
                timeout=5
            )

            if res.status_code != 200:
                raise requests.exceptions.HTTPError(f"Received {res.status_code} status code.")

            response_json = res.json()
            concept_id = response_json.get('id')

            logger.info(f'Created concept with ID {concept_id}')

            return concept_id

        except (requests.exceptions.ReadTimeout, requests.exceptions.HTTPError):
            retries -= 1
            if retries > 0:
                sleep(2)

    logger.error("Failed to save concept after maximum retries.")
    return None