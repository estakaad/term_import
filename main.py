from utils.config_loader import load_config, get_file_path
import src.sources as sources

# Load the configuration and crud_role_dataset
config_path = 'conf/test.json'
config, crud_role_dataset = load_config(config_path)

# Extracting API settings from the configuration
api_key = config['api_settings']['api_key']
base_url = config['api_settings']['base_url']

# Generating file paths
sources_without_ids = get_file_path(crud_role_dataset, "sources_files", "sources_without_ids")
sources_with_ids = get_file_path(crud_role_dataset, "sources_files", "sources_with_ids")
ids_of_added_sources = get_file_path(crud_role_dataset, "sources_files", "ids_of_added_sources")
ids_of_updated_sources = get_file_path(crud_role_dataset, "sources_files", "ids_of_updated_sources")
ids_of_deleted_sources = get_file_path(crud_role_dataset, "sources_files", "ids_of_deleted_sources")

concepts_without_word_ids = get_file_path(crud_role_dataset, "concepts_files", "concepts_without_word_ids")
concepts_with_word_ids = get_file_path(crud_role_dataset, "concepts_files", "concepts_with_word_ids")
ids_of_concepts_added = get_file_path(crud_role_dataset, "concepts_files", "ids_of_concepts_added")

# SOURCES #
sources.create_sources(sources_without_ids, sources_with_ids, ids_of_added_sources, api_key, base_url, crud_role_dataset)
sources.update_sources(sources_with_ids, ids_of_updated_sources, api_key, base_url, crud_role_dataset)
sources.delete_sources(ids_of_updated_sources, ids_of_deleted_sources, crud_role_dataset, api_key, base_url)

# CONCEPTS #
# TODO #