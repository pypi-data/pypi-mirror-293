
# sentok

**Sentok** is a fast and dynamic Python package for converting paragraphs into sentences. It offers customizable thresholds for adaptive sentence segmentation and is built on top of pandas for high performance and easy adjustment. The package allows you to easily convert paragraphs into a list of sentences or a DataFrame with probability columns.

## Features

- **High Performance**: Efficient handling of large texts.
- **Dynamic Configuration**: Customizable parameters and regular expressions.
- **Simple Logic**: Easy to understand and extend.

## Installation

### Via pip

To install the latest version directly from the GitHub repository, use:

```bash
pip install sentok
```

Or

```bash
pip install git+https://github.com/kothiyarajesh/sentok.git
```

### Building from Source

1. Clone the repository:

    ```bash
    git clone https://github.com/kothiyarajesh/sentok.git
    ```

2. Navigate to the project directory:

    ```bash
    cd sentok
    ```

3. Install the package:

    ```bash
    python setup.py install
    ```

## Usage

### Python Script

Here’s a simple example of how to use the `sentok` library in a Python script:

```python
import sentok

# Display current weights used by the tokenizer
# Uncomment the following line to view the current weights in use:
# print(sentok.get_weights())

# Adjust weights only if necessary for specific use cases
# For example, updating the set of start characters:
# sentok.set_weights({'start_chars': list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')})

# Sample text for sentence tokenization
text = """Natural language processing (NLP) is a captivating domain that merges computer science, artificial intelligence, and linguistics. It empowers computers to comprehend, interpret, and produce human language in a manner that is both useful and insightful. NLP finds application in various fields, such as text analysis, speech recognition, and machine translation. For example, advanced language models like GPT-3 have showcased exceptional skills in generating text that resembles human writing and in answering queries. As technology progresses, NLP continues to advance, enhancing its precision and expanding its scope of applications."""

# Tokenize the sample text into sentences using the default threshold of 0.65
# Adjust the threshold as needed based on your text's quality.
sentences = sentok.sent_tokenize(text, 0.64)

# Print each extracted sentence
for sentence in sentences:
    print('->', sentence)

# Print the total number of sentences extracted
print('Total Sentences:', len(sentences))

# Obtain a DataFrame with tokenization features for further analysis or model training:
df = sentok.get_sent_tokenize_df(text)
print(df)
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
