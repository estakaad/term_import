from utils.config_loader import load_config, get_file_path
import src.sources as sources
import src.words as words
import src.concepts as concepts
import src.relations as relations
import utils
import requests
import src.tags as tags

logger = utils.log_config.get_logger()

# Load the configuration and crud_role_dataset
config_path = 'conf/esterm_test.json'
config, crud_role_dataset = load_config(config_path)

# Extracting API settings from the configuration
api_key = config['api_settings']['api_key']
base_url = config['api_settings']['base_url']
dataset_for_checking_word_ids = config['parameters']['datasetForWordIds']

# Initialize a session and set the default header
session = requests.Session()
session.headers.update({"ekilex-api-key": api_key})

# # # PATHS # # #

sources_without_ids = get_file_path(crud_role_dataset, "sources_files", "sources_without_ids")
sources_with_ids = get_file_path(crud_role_dataset, "sources_files", "sources_with_ids")
ids_of_added_sources = get_file_path(crud_role_dataset, "sources_files", "ids_of_added_sources")
ids_of_updated_sources = get_file_path(crud_role_dataset, "sources_files", "ids_of_updated_sources")
ids_of_deleted_sources = get_file_path(crud_role_dataset, "sources_files", "ids_of_deleted_sources")

concept_ids = get_file_path(crud_role_dataset, "concepts_files", "concept_ids")
concepts_with_all_data = get_file_path(crud_role_dataset, "concepts_files", "concepts_with_all_data")
concepts_without_word_ids = get_file_path(crud_role_dataset, "concepts_files", "concepts_without_word_ids")
concepts_with_word_ids = get_file_path(crud_role_dataset, "concepts_files", "concepts_with_word_ids")
concepts_saved = get_file_path(crud_role_dataset, "concepts_files", "concepts_saved")
concepts_not_saved = get_file_path(crud_role_dataset, "concepts_files", "concepts_not_saved")

meanings_with_all_data = get_file_path(crud_role_dataset, "meaning_files", "meanings_with_all_data")

words_without_id = get_file_path(crud_role_dataset, "concepts_files", "words_without_id")
words_with_more_than_one_id = get_file_path(crud_role_dataset, "concepts_files", "words_with_more_than_one_id")

word_ids = get_file_path(crud_role_dataset, "word_files", "word_ids")
words_with_all_data = get_file_path(crud_role_dataset, "word_files", "words_with_all_data")

relations_with_meaning_ids = get_file_path(crud_role_dataset, "relations_files", "relations_with_meaning_ids")
meaning_relation_ids = get_file_path(crud_role_dataset, "relations_files", "meaning_relation_ids")
ids_of_deleted_relations = get_file_path(crud_role_dataset, "relations_files", "ids_of_deleted_relations")

meaning_tags = get_file_path(crud_role_dataset, "tag_files", "meaning_tags")
lexeme_tags = get_file_path(crud_role_dataset, "tag_files", "lexeme_tags")
# # # REQUESTS # # #

# # SOURCES #
#sources.create_sources(session, sources_without_ids, sources_with_ids, ids_of_added_sources, base_url, crud_role_dataset)
#sources.update_sources(session, sources_with_ids, ids_of_updated_sources, base_url, crud_role_dataset)
#sources.delete_sources(session, ids_of_added_sources, ids_of_deleted_sources, crud_role_dataset, base_url)

# CONCEPTS #

# words.update_word_ids(session, concepts_without_word_ids, concepts_with_word_ids,
#                    words_without_id, words_with_more_than_one_id,
#                     base_url, crud_role_dataset, dataset_for_checking_word_ids)

concepts.import_concepts(session, concepts_with_word_ids, concepts_saved, concepts_not_saved,
                          crud_role_dataset, base_url)

#concepts.get_all_concepts_from_dataset(session, concept_ids, concepts_with_all_data, base_url, crud_role_dataset)
#concepts.get_all_meanings(session, concept_ids, meanings_with_all_data, base_url, crud_role_dataset)

# WORDS #

#words.get_all_words(session, word_ids, words_with_all_data, base_url, crud_role_dataset)
#words.save_words(session, words_with_all_data, crud_role_dataset, base_url)

# RELATIONS
#relations.create_relations(session, relations_with_meaning_ids, base_url, crud_role_dataset)
#relations.delete_meaning_relations(session, meaning_relation_ids, ids_of_deleted_relations, base_url, crud_role_dataset)

# TAGS
#tags.create_meaning_tags(session, meaning_tags, base_url, crud_role_dataset)
#tags.create_lexeme_tags(session, lexeme_tags, base_url, crud_role_dataset)