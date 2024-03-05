import re
import nltk
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize
import glob
import os
from sklearn.model_selection import train_test_split
from gensim.models import Word2Vec


# Download NLTK data (you only need to do this once)
nltk.download('punkt')

lst_x_values = []
lst_y_values = []

def Text_processing(text, folder):

    # Function to extract links from text
    pattern_0 = r'https?://[^\s]+'
    extract_link = re.findall(pattern_0, text)
    text_1 = text.replace(str(extract_link), "WEBSITE_LINK")

    # GMAIL
    pattern_gmail = r"^[a-zA-Z0-9._]+@gmail\.com$"
    extract_gmail = re.match(pattern_gmail, text_1)
    gmail = text.replace(str(extract_gmail), "GMAIL_LINK")

    # Function to extract symbols from text
    pattern_1 = r'\W'
    extract_symbols = re.findall(pattern_1, gmail)
    symbols = text.replace(str(extract_symbols), "")

    # Function to extract a specific word from text
    pattern_2 = fr'\b{re.escape("The Great balaji")}\b'
    extract_specific_word = re.findall(pattern_2, symbols, flags=re.IGNORECASE)
    specific_word = text.replace(str(extract_specific_word), "ABCDE")

    # Match contractions like "couldn't" or "haven't"
    pattern_3 = r"\b(?:\w+'\w+|\w+n't)\b"
    # Find all matches in the text
    extract_contration_word = re.findall(pattern_3, specific_word)
    contractions_word = text.replace(str(extract_contration_word), "")

    # TOKENIZATION
    words = word_tokenize(contractions_word)

    # snowball stemmer
    language = 'english'
    snowball_stemmer = SnowballStemmer(language)
    stemmed_words = [snowball_stemmer.stem(word) for word in words]
    stemmed_text = ''.join(stemmed_words)
    lst_x_values.append(stemmed_text)
    lst_y_values.append(folder)

    data = [stemmed_text, folder]
    # Train the Skip-gram Word2Vec model
    model = Word2Vec(sentences=data, vector_size=100, window=5, sg=1, min_count=1, workers=4)
    #print("*******************", model)

    # Example of accessing word vectors
    word_vectors = model.wv
    print("^^^^^^^^^", word_vectors)
    if 'stemmed_text' in word_vectors and 'folder' in word_vectors:
        vector_x = word_vectors['x']
        vector_y = word_vectors['y']
    else:
        print("One or both of the words 'x' and 'y' are not in the vocabulary.")
        pass
    # vector_x = word_vectors[stemmed_text]
    # vector_y = word_vectors[folder]
    # #
    # # # You can use the word vectors for further processing or analysis
    # print("Vector for 'x':", vector_x)
    # print("Vector for 'y':", vector_y)
#******************************************************************************************************************
#split train adn test data

def split_data(X, y):

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Training data shape:", len(X_train), len(y_train))
    print("Testing data shape:", len(X_test), len(y_test))

#*********************************************************************************************************************

#def word2vec(X_train, y_test):


# Specify the path to your text file
folders = ['email', 'resume', 'scientific_publication']
file_list = []

# Iterate through each folder
for folder in folders:
    folder_path = os.path.join(r"D:\nlp\data_for_nlp", folder)
    file_path = os.path.join(folder_path, '*.txt')
    files = glob.glob(file_path)
    for file_content_1 in files:
        with open(file_content_1, 'r') as f:
            text = f.read()
            Text_processing(text, folder)



#print(lst_x_values, lst_y_values)




# split_data(lst_x_values, lst_y_values)
# word2vec(X_train, y_trai n)