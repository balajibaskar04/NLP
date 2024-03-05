import re
import nltk
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize
# Download NLTK data (you only need to do this once)
nltk.download('punkt')

# Specify the path to your text file
file_path = r"D:\nlp\data_for_nlp\email\extract_text*.txt"

lst_x_values = []
lst_tokenize = []
def Text_processing(text):

        # Function to extract links from text
        pattern_0 = r'https?://[^\s]+'
        extract_link = re.findall(pattern_0, text)
        text_1= text.replace(str(extract_link), "WEBSITE_LINK")
        #print("Full_text", text_1)

        #GMAIL
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
        #print("!!!!!!!!!!!!!!!!", specific_word)

        # Match contractions like "couldn't" or "haven't"
        pattern_3 = r"\b(?:\w+'\w+|\w+n't)\b"
        # Find all matches in the text
        extract_contration_word = re.findall(pattern_3, specific_word)
        contractions_word = text.replace(str(extract_contration_word), "")
        #print("&&&&&&&&&&&&&&&&&&&&&&&")
        #print("extract_contration_word", contractions_word)



        # contration = ""
        # if contractions_word == "cann't":
        #     contration =text.replace(str(contractions_word), "can not")
        # elif extract_contration_word == "haven't":
        #     contration = text.replace(str(contractions_word), "have not")
        # else:
        #     pass

        #TOKENIZATION
        words = word_tokenize(contractions_word)
        lst_tokenize.append(words)

        # snowball stemmer
        language = 'english'
        snowball_stemmer = SnowballStemmer(language)
        stemmed_words = [snowball_stemmer.stem(word) for word in words]
        stemmed_text = ''.join(stemmed_words)
        lst_x_values.append(stemmed_text)




print("x values", lst_x_values)
print("******************************************")
print("tokenize", lst_tokenize)

# Read the content of the text file
with open(file_path, 'r', encoding='utf-8') as file:
    file_content = file.read()

Text_processing(file_content)

