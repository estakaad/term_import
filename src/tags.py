import utils.log_config
import requests
import json

logger = utils.log_config.get_logger()

def create_meaning_tag(session, request_body, base_url, dataset_code):
    parameters = {'crudRoleDataset': dataset_code}
    endpoint = base_url + "/api/meaning_tag/create"

    response = session.post(endpoint, params=parameters, json=request_body)

    if response.status_code >= 200 and response.status_code < 300:
        try:
            response_data = response.json()
            logger.info(f'Created meaning tag {request_body}')
            return response_data['success']
        except json.JSONDecodeError:
            logger.warning(request_body)
            logger.warning(f"Failed to parse JSON from response when creating meaning tag {request_body} "
                           f"Response text: {response.text}")

    else:
        logger.warning(request_body)
        logger.warning(f"Received non-200 response when creating meaning tag. "
                       f"Status code: {response.status_code}, "
                       f"Response text: {response.text}")
    return None

def create_meaning_tags(session, meaning_request_bodies_path, base_url, dataset_code):

    logger.info(f'Started processing relations from file: {meaning_request_bodies_path}')

    count_created_tags = 0

    with open(meaning_request_bodies_path, 'r', encoding='utf-8') as f:
        meaning_tags = json.load(f)

        for meaning_tag in meaning_tags:
            tag_status = create_meaning_tag(session, meaning_tag, base_url, dataset_code)
            if tag_status is True:
                count_created_tags += 1

    logger.info('Number of created meaning tags: ' + str(count_created_tags))