from utils.config_loader import load_config, get_file_path
import src.sources as sources
import src.words as words
import src.concepts as concepts

# Load the configuration and crud_role_dataset
config_path = 'conf/mere_test.json'
config, crud_role_dataset = load_config(config_path)

# Extracting API settings from the configuration
api_key = config['api_settings']['api_key']
base_url = config['api_settings']['base_url']
dataset_for_checking_word_ids = config['parameters']['datasetForWordIds']
#
# # Generating file paths
sources_without_ids = get_file_path(crud_role_dataset, "sources_files", "sources_without_ids")
sources_with_ids = get_file_path(crud_role_dataset, "sources_files", "sources_with_ids")
ids_of_added_sources = get_file_path(crud_role_dataset, "sources_files", "ids_of_added_sources")
ids_of_updated_sources = get_file_path(crud_role_dataset, "sources_files", "ids_of_updated_sources")
ids_of_deleted_sources = get_file_path(crud_role_dataset, "sources_files", "ids_of_deleted_sources")

concepts_without_word_ids = get_file_path(crud_role_dataset, "concepts_files", "concepts_without_word_ids")
concepts_with_word_ids = get_file_path(crud_role_dataset, "concepts_files", "concepts_with_word_ids")
words_without_id = get_file_path(crud_role_dataset, "concepts_files", "words_without_id")
words_with_more_than_one_id = get_file_path(crud_role_dataset, "concepts_files", "words_with_more_than_one_id")
concepts_saved = get_file_path(crud_role_dataset, "concepts_files", "concepts_saved")
concepts_not_saved = get_file_path(crud_role_dataset, "concepts_files", "concepts_not_saved")

# # SOURCES #
#sources.create_sources(sources_without_ids, sources_with_ids, ids_of_added_sources, api_key, base_url, crud_role_dataset)
#sources.update_sources(sources_with_ids, ids_of_updated_sources, api_key, base_url, crud_role_dataset)
#sources.delete_sources(ids_of_added_sources, ids_of_deleted_sources, crud_role_dataset, api_key, base_url)

# CONCEPTS #
words.update_word_ids(concepts_without_word_ids, concepts_with_word_ids,
                    words_without_id, words_with_more_than_one_id,
                   api_key, base_url, crud_role_dataset, dataset_for_checking_word_ids)

#concepts.import_concepts(concepts_with_word_ids, concepts_saved, concepts_not_saved, crud_role_dataset, api_key, base_url)