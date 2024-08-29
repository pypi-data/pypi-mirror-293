import re
import logging
import numpy as np
import pandas as pd
from . sentok_weights import STWeights

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SenTok(STWeights):
    def __init__(self):
        super().__init__()

    def get_weights(self) -> dict:
        """
        Retrieve the current weights of the model.

        Returns:
            dict: Dictionary of current weights.
        """
        default_weights = vars(self)
        logger.info(f"Current weights: {default_weights}")
        return default_weights

    def set_weights(self, weights_dict: dict) -> None:
        """
        Update the weights of the model based on the provided dictionary.

        Args:
            weights_dict (dict): Dictionary where keys are weight names and values are the new weights.

        Updates:
            The model's weights are updated and logged.
        """
        for weight_name, new_value in weights_dict.items():
            if hasattr(self, weight_name):
                setattr(self, weight_name, new_value)
                logger.info(f"Updated {weight_name} to {new_value}")
            else:
                logger.error(f"{weight_name} does not exist")

    def initialize_dataframe(self, words: list[str]) -> pd.DataFrame:
        """
        Initialize a DataFrame from a list of words with features required for sentence segmentation.

        Args:
            words (list[str]): List of words to include in the DataFrame.

        Returns:
            pd.DataFrame: DataFrame with columns 'Length', 'First_Letter', 'Last_Letter', 'Current_Word', 'Prev_Word', 'Next_Word', 'Prob_First', and 'Prob_Last'.
        """
        lengths = np.array([len(word) for word in words])
        start_pos = np.array([word[0] if len(word) > 0 else '' for word in words])
        end_pos = np.array([word[-1] if len(word) > 0 else '' for word in words])
        prev_words = [words[i - 1] if i > 0 else '' for i in range(len(words))]
        next_words = [words[i + 1] if i < len(words) - 1 else '' for i in range(len(words))]
        prob_first = np.zeros(len(words))
        prob_last = np.zeros(len(words))

        return pd.DataFrame({
            'Length': lengths,
            'First_Letter': start_pos,
            'Last_Letter': end_pos,
            'Current_Word': words,
            'Prev_Word': prev_words,
            'Next_Word': next_words,
            'Prob_First': prob_first,
            'Prob_Last': prob_last,
        })
        
    def extract_sents(self, df: pd.DataFrame, thresh: float = None) -> list[str]:
        """
        Extract sentences from the DataFrame based on probability thresholds.

        Args:
            df (pd.DataFrame): DataFrame with word probabilities.
            thresh (float, optional): Threshold for sentence splitting.

        Returns:
            list[str]: List of sentences extracted from the DataFrame.
        """
        
        # Create a boolean mask where the sentence split should occur
        sentence_split_mask = df['Prob_Last'] > thresh
        
        # Use numpy for efficient operations
        current_texts = df['Current_Word'].values
        sentence_split_indices = np.where(sentence_split_mask)[0]
        sents = []
        start_idx = 0
        
        for end_idx in sentence_split_indices:
            sents.append(' '.join(current_texts[start_idx:end_idx + 1]).strip())
            start_idx = end_idx + 1
        
        # Handle the remaining part after the last threshold exceed
        if start_idx < len(current_texts):
            sents.append(' '.join(current_texts[start_idx:]).strip())
        
        return sents

    def calc_probs(self, df):
        # Create boolean masks for start and end characters
        start_char_mask = df['First_Letter'].isin(self.start_chars)
        end_char_mask = df['Last_Letter'].isin(self.end_chars)
        
        # Create boolean masks for start and end words
        start_word_mask = df['Current_Word'].isin(self.start_words)
        end_word_mask = df['Current_Word'].isin(self.end_words)
        
        # Update probabilities
        prev_is_empty = df['Prev_Word'].apply(len) == 0
        next_is_empty = df['Next_Word'].apply(len) == 0
        
        df['Prob_First'] += np.where(prev_is_empty, self.pro_first_word_weight, 0)
        df['Prob_First'] += np.where(start_char_mask, self.pro_start_char_mask_weight, 0)
        df['Prob_First'] += np.where(start_word_mask, self.pro_start_word_mask_weight, 0)
        
        df['Prob_Last'] += np.where(next_is_empty, self.pro_last_word_weight, 0)
        df['Prob_Last'] += np.where(end_char_mask, self.pro_end_char_mask_weight, 0)
        df['Prob_Last'] += np.where(end_word_mask, self.pro_end_word_mask_weight, 0)

    def adjust_probs(self, df):
        prob_first = df['Prob_First'].values
        prob_last = df['Prob_Last'].values

        prev_prob_first = np.roll(prob_first, shift=1)
        prev_prob_first[0] = 0

        prev_prob_last = np.roll(prob_last, shift=1)
        prev_prob_last[0] = 0

        next_prob_first = np.roll(prob_first, shift=-1)
        next_prob_first[-1] = 0

        next_prob_last = np.roll(prob_last, shift=-1)
        next_prob_last[-1] = 0

        # The following conditions carry more weight than the others.
        df['Prob_First'] += np.where(prev_prob_last >= self.prob_first_add_prev_prob_last_gte_condi_weight, self.prob_first_add_prev_prob_last_gte_val_weight, 0)
        df['Prob_Last'] += np.where(next_prob_first >= self.prob_last_add_next_prob_first_gte_condi_weight, self.prob_last_add_next_prob_first_gte_val_weight, 0)

        df['Prob_First'] -= np.where(prev_prob_first > prob_first, self.prob_first_sub_prev_prob_first_gt_prob_first_val_weight, 0)
        df['Prob_First'] -= np.where(next_prob_first > prob_first, self.prob_first_sub_next_prob_first_gt_prob_first_val_weight, 0)
        df['Prob_First'] -= np.where(next_prob_last > prob_first, self.prob_first_sub_next_prob_last_gt_prob_first_val_weight, 0)

        df['Prob_Last'] -= np.where(next_prob_last > prob_last, self.prob_last_sub_next_prob_last_gt_prob_last_val_weight, 0)
        df['Prob_Last'] -= np.where(prev_prob_first > prob_last, self.prob_last_sub_prev_prob_first_gt_prob_last_val_weight, 0)
        df['Prob_Last'] -= np.where(prev_prob_last > prob_last, self.prob_last_sub_prev_prob_last_gt_prob_last_val_weight, 0)

        # NOTE: The sequence of code execution is important. Prioritize `Prob_Last` more. TODO: Improve the logic if necessary.
        df['Prob_Last'] -= np.where(df['Prob_First'] >= df['Prob_Last'], self.prob_last_sub_prob_first_gte_prob_last_val_weight, 0)
        df['Prob_First'] -= np.where(df['Prob_Last'] >= df['Prob_First'], self.prob_first_sub_prob_last_gte_prob_first_val_weight, 0)

        df['Prob_First'] = np.clip(df['Prob_First'], 0, 1)
        df['Prob_Last'] = np.clip(df['Prob_Last'], 0, 1)


    def process_text(self, df: pd.DataFrame) -> None:
        """
        Process the DataFrame to calculate and adjust probabilities for sentence segmentation.

        Args:
            df (pd.DataFrame): DataFrame with initial probabilities.

        Updates:
            Modifies the 'Prob_First' and 'Prob_Last' columns in the DataFrame.
        """
        self.calc_probs(df)
        self.adjust_probs(df)

    def extract_special_words_from_text(self, text: str) -> None:
        """
        Extract words from the provided text based on start and end regular expression patterns.

        Args:
            text (str): The text from which to extract words.

        Updates:
            self.start_words (list[str]): List of words that match the start regular expression patterns.
            self.end_words (list[str]): List of words that match the end regular expression patterns.
        """
        if self.start_re_patterns:
            combined_start_pattern = '|'.join(self.start_re_patterns)
            start_matches = re.findall(combined_start_pattern, text)
            self.start_words.extend(start_matches)
        
        if self.end_re_patterns:
            combined_end_pattern = '|'.join(self.end_re_patterns)
            end_matches = re.findall(combined_end_pattern, text)
            self.end_words.extend(end_matches)

    def word_tokenize(self, text: str) -> list[str]:
        """
        Tokenize the input text into words.

        Args:
            text (str): The text to tokenize.

        Returns:
            list[str]: List of words extracted from the text.
        """
        # TODO: Enhance the advanced word tokenization logic
        return text.split()

    def sent_tokenize(self, text: str, thresh: float = 0.65) -> list[str]:
        """
        Tokenize the input text into sentences based on probabilities.

        Args:
            text (str): The text to process.
            thresh (float, optional): Threshold for sentence splitting. Default is 0.65.

        Returns:
            list[str]: List of sentences extracted from the text.
        """
        self.extract_special_words_from_text(text)
        df = self.initialize_dataframe(self.word_tokenize(text))
        self.process_text(df)
        return self.extract_sents(df, thresh)

    def get_sent_tokenize_df(self, text: str) -> pd.DataFrame:
        """
        Tokenize the input text into sentences based on probabilities.

        Args:
            text (str): The text to process.

        Returns:
            pd.DataFrame: DataFrame with columns 'Length', 'First_Letter', 'Last_Letter', 'Current_Word', 'Prev_Word', 'Next_Word', 'Prob_First', and 'Prob_Last'.
        """
        self.extract_special_words_from_text(text)
        df = self.initialize_dataframe(self.word_tokenize(text))
        self.process_text(df)
        return df
