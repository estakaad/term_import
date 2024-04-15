import json


def load_config(file_path):
    with open(file_path, 'r') as config_file:
        config = json.load(config_file)

    crud_role_dataset = config['parameters']['crudRoleDataset']
    config['parameters']['baseFilePath'] = f"files/{crud_role_dataset}/"

    return config, crud_role_dataset


def get_file_path(crud_role_dataset, file_category, file_key):
    base_path = f"files/{crud_role_dataset}/"
    file_paths = {
        "sources_files": {
            "sources_without_ids": "sources.json",
            "sources_with_ids": "sources_with_ids.json",
            "ids_of_added_sources": "ids_of_added_sources.json",
            "ids_of_updated_sources": "ids_of_updated_sources.json",
            "ids_of_deleted_sources": "ids_of_deleted_sources.json"
        },
        "concepts_files": {
            "concept_ids": "concept_ids.json",
            "concepts_with_all_data": "concepts_with_all_data.json",
            "concepts_without_word_ids": "concepts_without_word_ids.json",
            "concepts_with_word_ids": "concepts_with_word_ids.json",
            "words_without_id": "words_without_id.json",
            "words_with_more_than_one_id": "words_with_more_than_one_id.json",
            "concepts_saved": "concepts_saved.json",
            "concepts_not_saved": "concepts_not_saved.json"
        },
        "relations_files": {
            "relations_without_ids": "relations_without_ids.json",
            "relations_with_ids": "relations_with_ids.json",
            "ids_of_added_relations": "ids_of_added_relations.json",
            "ids_of_deleted_relations": "ids_of_deleted_relations.json"
        }
    }
    return base_path + file_paths[file_category][file_key]
