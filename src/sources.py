import utils.log_config
import requests
import json

logger = utils.log_config.get_logger()

def create_source(source, api_key, base_url, crud_role_dataset):

    header = {"ekilex-api-key": api_key}

    parameters = {
        'crudRoleDataset': crud_role_dataset
    }

    endpoint = base_url + "/api/source/create"
    response = requests.post(endpoint, headers=header, params=parameters, json=source)

    if response.status_code >= 200 and response.status_code < 300:
        try:
            response_data = response.json()
            logger.info(f'Created source with ID {response_data["id"]}')
            return response_data['id']
        except json.JSONDecodeError:
            logger.warning(source)
            logger.warning(f"Failed to parse JSON from response when creating source "
                           f"Response text: {response.text}")

    else:
        logger.warning(source)
        logger.warning(f"Received non-200 response when creating source. "
                       f"Status code: {response.status_code}, "
                       f"Response text: {response.text}")
    return None

def create_sources(sources_without_ids, sources_with_ids, ids_of_added_sources, api_key, base_url, crud_role_dataset):

    updated_sources = []
    ids_of_created_sources = []

    logger.info(f'Started assigning ID-s to all sources: {sources_without_ids}')

    with open(sources_without_ids, 'r', encoding='utf-8') as f:
        count_created_sources = 0
        data = json.load(f)

        for source in data:
            source_id = create_source(source, api_key, base_url, crud_role_dataset)
            if source_id:
                source['id'] = source_id
                updated_sources.append(source)
                ids_of_created_sources.append(source_id)
                count_created_sources += 1

    with open(sources_with_ids, 'w', encoding='utf-8') as source_files_with_ids:
        json.dump(updated_sources, source_files_with_ids, ensure_ascii=False, indent=4)

    logger.info(f'Created file with sources and their ID-s: {sources_with_ids}')

    with open(ids_of_added_sources, 'w', encoding='utf-8') as f:
        json.dump(ids_of_created_sources, f, ensure_ascii=False, indent=4)

    logger.info(f'Created list of ID-s of created sources: {ids_of_added_sources}')
    logger.info('Number of created sources: ' + str(count_created_sources))

    return source_files_with_ids


def delete_sources(ids_of_added_sources, ids_of_deleted_sources, crud_role_dataset, api_key, base_url):
    list_of_ids_of_deleted_sources = []

    header = {"ekilex-api-key": api_key}

    with open(ids_of_added_sources, 'r', encoding='utf-8') as file:
        source_ids = json.load(file)

    endpoint = base_url + "/api/source/delete"

    logger.info(f"Number of sources to be deleted: {len(source_ids)}.")

    for source_id in source_ids:
        params = {
            'sourceId': source_id,
            'crudRoleDataset': crud_role_dataset
        }

        response = requests.delete(endpoint, headers=header, params=params)

        if response.status_code >= 200 and response.status_code < 300:
            logger.info(f"Successfully deleted source with ID {source_id}.")
            list_of_ids_of_deleted_sources.append(source_id)
        else:
            logger.info(f"Failed to delete source with ID {source_id}. Status code: {response.status_code}, "
                        f"Response text: {response.text}")


    with open(ids_of_deleted_sources, 'w', encoding='utf-8') as f:
        json.dump(list_of_ids_of_deleted_sources, f, ensure_ascii=False, indent=4)

    logger.info(f'Created list of ID-s of deleted sources: {ids_of_deleted_sources}')
    logger.info('Number of deleted sources: ' + str(len(list_of_ids_of_deleted_sources)))


def update_source(source, api_key, base_url, crud_role_dataset):

    header = {"ekilex-api-key": api_key}

    parameters = {
        'crudRoleDataset': crud_role_dataset
    }

    endpoint = base_url + "/api/source/update"
    response = requests.post(endpoint, headers=header, params=parameters, json=source)

    if response.status_code >= 200 and response.status_code < 300:
        try:
            response_data = response.json()
            if response_data["success"] == True:
                logger.info(f'Updated source with ID {source["id"]}')
                return source["id"]
        except json.JSONDecodeError:
            logger.warning(source)
            logger.warning(f"Failed to parse JSON from response when updating source "
                           f"Response text: {response.text}")

    else:
        logger.warning(source)
        logger.warning(f"Received non-200 response when updating source. "
                       f"Status code: {response.status_code}, "
                       f"Response text: {response.text}")
    return None


def update_sources(sources_with_ids, ids_of_updated_sources, api_key, base_url, crud_role_dataset):
    list_of_ids_of_updated_sources = []

    logger.info(f'Started updating sources: {sources_with_ids}')

    with open(sources_with_ids, 'r', encoding='utf-8') as f:
        data = json.load(f)

        for source in data:
            result = update_source(source, api_key, base_url, crud_role_dataset)
            if result:
                list_of_ids_of_updated_sources.append(source['id'])

    with open(ids_of_updated_sources, 'w', encoding='utf-8') as f:
        json.dump(list_of_ids_of_updated_sources, f, ensure_ascii=False, indent=4)

    logger.info(f'Created list of ID-s of updated sources: {list_of_ids_of_updated_sources}')
    logger.info('Number of updated sources: ' + str(len(list_of_ids_of_updated_sources)))

    return list_of_ids_of_updated_sources