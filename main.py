from utils.config_loader import load_config
import src.sources as sources

config_path = 'conf/test.json'
config = load_config(config_path)

api_key = config['api_settings']['api_key']
base_url = config['api_settings']['base_url']

crud_role_dataset = config['parameters']['crudRoleDataset']

sources_without_ids = config['sources_files']['sources_without_ids']
sources_with_ids = config['sources_files']['sources_with_ids']
ids_of_added_sources = config['sources_files']['ids_of_added_sources']
ids_of_updated_sources = config['sources_files']['ids_of_updated_sources']
ids_of_deleted_sources = config['sources_files']['ids_of_deleted_sources']

concepts_without_word_ids = config['concepts_files']['concepts_without_word_ids']
concepts_with_word_ids = config['concepts_files']['concepts_with_word_ids']
ids_of_concepts_added = config['concepts_files']['ids_of_concepts_added']

sources.create_sources(sources_without_ids, sources_with_ids, ids_of_added_sources, api_key, base_url, crud_role_dataset)
sources.update_sources(sources_with_ids, ids_of_updated_sources, api_key, base_url, crud_role_dataset)
sources.delete_sources(ids_of_updated_sources, ids_of_deleted_sources, crud_role_dataset, api_key, base_url)