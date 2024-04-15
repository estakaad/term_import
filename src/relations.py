import utils.log_config
import requests
import json

logger = utils.log_config.get_logger()

def create_relation(session, relation, base_url, dataset_code):
    parameters = {'crudRoleDataset': dataset_code}
    endpoint = base_url + "/api/meaning_relation/create"
    response = session.post(endpoint, params=parameters, json=relation)

    if response.status_code >= 200 and response.status_code < 300:
        try:
            response_data = response.json()
            logger.info(f'Created relation {relation}')
            return response_data['success']
        except json.JSONDecodeError:
            logger.warning(relation)
            logger.warning(f"Failed to parse JSON from response when creating relation {relation} "
                           f"Response text: {response.text}")

    else:
        logger.warning(relation)
        logger.warning(f"Received non-200 response when creating relation. "
                       f"Status code: {response.status_code}, "
                       f"Response text: {response.text}")
    return None

def create_relations(session, relations_file_path, base_url, dataset_code):

    logger.info(f'Started processing relations from file: {relations_file_path}')
    count_created_relations = 0
    with open(relations_file_path, 'r', encoding='utf-8') as f:
        relations_data = json.load(f)

        for relation in relations_data:
            relation_status = create_relation(session, relation, base_url, dataset_code)
            if relation_status is True:
                count_created_relations += 1

    logger.info('Number of created relations: ' + str(count_created_relations))