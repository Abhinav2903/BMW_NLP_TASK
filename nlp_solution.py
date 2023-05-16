
# Define all the import  that are needed for the task to be completed
from dateutil.parser import parse
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import calendar
from abbrevations import abbreviations
from model_type_codecs import model_type_codes
import json
import re
import nltk
import numpy
import keyboard
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

# Define the class that handles all the functions and
class NlpPromptConverter:

    def __init__(self, prompt):
        self.prompt = prompt
        

    # Define function to evaluate boolean formula have to modify accordingly
    def evaluate_formula(self, formulas):
        boolean_formula=[]
        bool_prompt = self.prompt.lower();
        # Tokenize the text into words
        tokens = nltk.word_tokenize(self.prompt)

        # Perform part-of-speech tagging
        pos_tags = nltk.pos_tag(tokens)

        # Define a chunk grammar to extract the desired phrases
        chunk_grammar = r"""
            Phrase: {<NNP|NN.*>+}   # Chunk any combination of nouns
            """

        # Create a chunk parser with the defined grammar
        chunk_parser = nltk.RegexpParser(chunk_grammar)

        # Apply chunking to the part-of-speech tagged text
        chunked_text = chunk_parser.parse(pos_tags)

        # Extract the desired phrases from the chunked text
        desired_phrases = []
        bool_phrases=[]
        for subtree in chunked_text.subtrees():
            #print("subtree",subtree)
            if (subtree.label() == 'Phrase'):
                phrase = ' '.join(word for word, tag in subtree.leaves())
            # Check if the extracted phrase matches any of the desired abbrevation descriptions
                for abbreviation, meaning in abbreviations.items():
                    descritipn_lower = meaning.lower()
                    phrase_lower = phrase.lower()
                    word_set1 = set(descritipn_lower.split())
                    word_set2 = set(phrase_lower.split())
                    if word_set1 == word_set2:
                        desired_phrases.append((abbreviation, meaning))
                        bool_phrases.append((abbreviation,phrase_lower))
        for abbreviation, meaning in desired_phrases:
            formulas.append(abbreviation)

        for abbreviation, meaning in abbreviations.items():
            if (meaning.lower() in self.prompt.lower() and (abbreviation.lower()=='rl' or abbreviation.lower()=='ll' )):
                formulas.append(abbreviation)
                bool_prompt = bool_prompt.replace(meaning.lower(),abbreviation)
        for abbreviation, phrase in bool_phrases:
            bool_prompt = bool_prompt.replace(phrase.lower(),abbreviation)
        boolean_formula = formulas
        
        boolean_formula = self.convert_to_boolean(boolean_formula,bool_prompt)
        return [boolean_formula]

    
    def convert_to_boolean(self,formulas,bool_prompt):
        exact_boolean =''
        boolean_formula_array =[]
        for key in formulas:
            if key in bool_prompt:
                key_value = abbreviations.get(key)
                #print(key,key_value)
                if(key_value!=None):
                    pattern = r"((?:and|or|not|and not|or not|without) (?:\w+\W+){0,3})?(" + key + ")"
                    #print(pattern)
                    matches = re.findall(pattern, bool_prompt, flags=re.IGNORECASE)
                    #print(matches)
                    if matches:
                        preceding_words = matches[0][0].strip() if matches[0][0] else None
                        #print(preceding_words)
                        if(preceding_words!=None):
                            if 'and not' in preceding_words:
                                 exact_boolean = '+-'+ key
                            elif 'and with' in preceding_words:
                                 exact_boolean = '+'+ key     
                            elif 'or not' in preceding_words:
                                exact_boolean =  '/-'+key
                            elif 'and' in preceding_words :
                                exact_boolean =  '+'+key
                            elif 'or' in preceding_words:
                                exact_boolean =  '/'+key
                            elif 'without' in preceding_words:
                                exact_boolean =  '-'+key    
                        else:
                            exact_boolean = '+'+ key    
            boolean_formula_array.append(exact_boolean)
        boolean_formula_array = ' '.join(boolean_formula_array)
        boolean_formula_array = ''.join(boolean_formula_array.split())    
        return boolean_formula_array            

    # define the function to extract relevant information from the prompt provided
    def extract_info(self):
        model_type = []
        formulas = []
        date = None

        model_type = self.extract_model_type(model_type)
        formulas = self.evaluate_formula(formulas)
        date = self.extract_date(date)
        return model_type, formulas, date

    # Define the funtion for extracting model type codecs
    def extract_model_type(self, model_type):
        # check for the exact match in the prompt provided
        for code, description in model_type_codes.items():
            if description.lower() in self.prompt.lower():
                model_type.append(code)
                break
        # check for the length of the model type if it is 0 then check for the specific substring provided in the prompt
        if (len(model_type) == 0):
            for code, description in model_type_codes.items():
                words = description.lower().split()
                if (any(word in self.prompt.lower() for word in words)):
                    #print('xxxx', description)
                    model_type.append(code)
        return model_type

    # define the function for extracting date
    def extract_date(self, date):

        # check for the date that have start,mid or end in the prompt
        matches = re.findall(
            r"\b(?:start|mid|end) of \w+\s+\d{4}\b", self.prompt)
        month_mapping = {name.lower(): index for index,
                         name in enumerate(calendar.month_name) if name}
        if (matches):
            if matches:
                date = matches[0]
                # cases for the differnt type and synonym writing in the prompt
                if 'start of' in date:
                    date = date.replace("start of", "1st")
                elif 'starting' in date:
                    date = date.replace("starting", "1st")
                elif 'mid of' in date:
                    date = date.replace("mid of", "15th")
                elif 'end of' in date:
                    date = date.replace("end of", "")
                    month, year = date.split()
                    # Get the last day of the month as differnt months have different end date liske 27th, 28th,30th or 31st
                    last_day = calendar.monthrange(
                        int(year), month_mapping[month.lower()])[1]
                    # Replace the date with the month's last day
                    date = f"{last_day} {month} {year}"
                elif 'ending' in date:
                    date = date.replace("ending", "")
                    month, year = date.split()
                    # Get the last day of the month as differnt months have different end date liske 27th, 28th,30th or 31st
                    last_day = calendar.monthrange(
                        int(year), month_mapping[month.lower()])[1]
                    # Replace the date with the month's last day
                    date = f"{last_day} {month} {year}"
                date_obj = parse(date, fuzzy=True)
                date = date_obj.strftime("%Y-%m-%d")
        else:
            # check for the date that have normal dates like 1st,2nd or kind of numeric and word format in the prompt
            matches = re.findall(
                r"\b\d{1,2}(?:st|nd|rd|th)?\s+(?:of\s+)?\w+\s+\d{4}\b", self.prompt)
            if (matches):
                date = matches[0]
                date_obj = parse(date, fuzzy=True)
                date = date_obj.strftime("%Y-%m-%d")
            else:
                date = None
                print("No date found in the string.")
        return date

    # Function to convert extracted information into a request body
    def create_request_body(self, model_type, formulas, date):

        request_body = {
            "modelTypeCodes": [model_type],
            "booleanFormulas": formulas,
            "dates": [date]
        }
        return request_body


def main():
    prompt = input("Enter the prompt")
    if (prompt.strip()):
        promptconverter = NlpPromptConverter(prompt)
        model_type, formulas, date = promptconverter.extract_info()
        for i in range (len(model_type)):
            request_body = promptconverter.create_request_body(
                model_type[i], formulas, date)
            print(json.dumps(request_body, indent=2))
            print("Enter ESC to return back")

        # Add a loop to keep the program running until the user presses Esc
        while True:
            if keyboard.is_pressed("esc"):
                break
    else:
        print("Please Enter a valid prompt")
        main()

if __name__ == "__main__":
    main()
