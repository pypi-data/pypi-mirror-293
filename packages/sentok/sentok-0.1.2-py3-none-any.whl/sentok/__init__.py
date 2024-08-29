from . main import SenTok

# Create a single instance
_sentok_instance = SenTok()

# Expose all methods of SenTok directly
sent_tokenize = _sentok_instance.sent_tokenize
get_weights = _sentok_instance.get_weights
set_weights = _sentok_instance.set_weights
initialize_dataframe = _sentok_instance.initialize_dataframe
word_tokenize = _sentok_instance.word_tokenize
get_sent_tokenize_df = _sentok_instance.get_sent_tokenize_df

__all__ = ['sent_tokenize', 'get_weights', 'set_weights', 'initialize_dataframe', 'word_tokenize', 'get_sent_tokenize_df']
