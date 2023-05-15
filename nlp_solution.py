
# Define all the import  that are needed for the task to be completed
from abbrevations import abbreviations;
from model_type_codecs import model_type_codes;
import json;
import re;
# import nltk
# nltk.download('punkt')
# from nltk.corpus import stopwords;
# from nltk.tokenize import word_tokenize;
from dateutil.parser import parse;
import calendar

# Define the class that handles all the functions and 
class NlpPromptConverter:


    def __init__(self,prompt):
        self.prompt = prompt
        self.date_mapping = {
        "start": "1st",
        "mid": "15th",
        "end": {
            27: ["February"],
            30: ["April", "June", "September", "November"],
            31: ["January", "March", "May", "July", "August", "October", "December"]
    }
        }

    # # # Define function for removal of stop words
    # def remove_stop_words(self):
    #     stop_words = set(stopwords.words('english'))
    #     words = word_tokenize(self.prompt)
    #     filter_word_set =  [word for word in words if word.lower() not in stop_words]
    #     self.prompt = ' '.join(filter_word_set);
    #     print("stop words removal ",self.prompt)

    # Define function to evaluate boolean formula have to modify accordingly
    def evaluate_formula(self):
        for abbreviation, meaning in abbreviations.items():
            formula = formula.replace(abbreviation, meaning)
        boolean_formula = eval(formula)
        return boolean_formula;

    # define the function to extract relevant information from the prompt provided
    def extract_info(self):
        model_type = []
        formulas = []
        date = None
        
        matches = re.findall(r"\b\S+[+-]\b", self.prompt)
        for match in matches:
            if match[:-1] in abbreviations:
                formulas.append(match)
        
        model_type = self.extract_model_type(model_type)
        # formulas = self.evaluate_formula()
        date = self.extract_date(date)
        return model_type, formulas, date;

    # Define the funtion for extracting model type codecs
    def extract_model_type(self,model_type):
        # check for the exact match in the prompt provided
        for code,description in model_type_codes.items():
            if description.lower() in self.prompt.lower():
                model_type.append(code)
                break;
        # check for the length of the model type if it is 0 then check for the specific substring provided in the prompt
        if(len(model_type)==0):
            for code,description in model_type_codes.items():    
                words = description.lower().split() 
                if (any( word in self.prompt.lower() for word in words)):
                    print('xxxx', description)
                    model_type.append(code)
        return model_type;

    # define the function for extracting date
    def extract_date(self,date):

        # check for the date that have start,mid or end in the prompt
        matches = re.findall(r"\b(?:start|mid|end) of \w+\s+\d{4}\b", self.prompt)
        month_mapping = {name.lower(): index for index, name in enumerate(calendar.month_name) if name}
        if(matches):
            if matches:
                date = matches[0]
                # cases for the differnt type and synonym writing in the prompt
                if 'start of' in date:
                    date = date.replace("start of","1st")
                elif 'starting' in date:
                    date = date.replace("starting","1st")    
                elif 'mid of' in date:
                    date = date.replace("mid of","15th")
                elif 'end of' in date:
                    date = date.replace("end of", "")
                    month, year = date.split()
                    # Get the last day of the month as differnt months have different end date liske 27th, 28th,30th or 31st  
                    last_day = calendar.monthrange(int(year), month_mapping[month.lower()])[1]
                    # Replace the date with the month's last day
                    date = f"{last_day} {month} {year}"
                elif 'ending' in date:
                    date = date.replace("ending", "")
                    month, year = date.split()
                     # Get the last day of the month as differnt months have different end date liske 27th, 28th,30th or 31st  
                    last_day = calendar.monthrange(int(year), month_mapping[month.lower()])[1]
                    # Replace the date with the month's last day
                    date = f"{last_day} {month} {year}"   
                date_obj = parse(date, fuzzy=True)
                date = date_obj.strftime("%Y-%m-%d")  
        else:
            # check for the date that have normal dates like 1st,2nd or kind of numeric and word format in the prompt
            matches = re.findall(r"\b\d{1,2}(?:st|nd|rd|th)?\s+(?:of\s+)?\w+\s+\d{4}\b", self.prompt)
            if(matches):
                date = matches[0]
                date_obj = parse(date, fuzzy=True)
                date = date_obj.strftime("%Y-%m-%d")
            else:
                print("No date found in the string.")
        return date;



    # Function to convert extracted information into a request body
    def create_request_body(self,model_type, formulas, date):
        # model_type, formulas, date = self.extract_info()

        evaluated_formulas = []
        for formula in formulas:
            result = self.evaluate_formula(formula)
            evaluated_formulas.append(result)

        request_body = {
            "modelTypeCodes": [model_type],
            "booleanFormulas": evaluated_formulas,
            "dates": [date]
        }
        return request_body



def main():
    prompt = input("Enter the prompt")    
    if(prompt.strip()):
        promptconverter = NlpPromptConverter(prompt)
        # promptconverter.remove_stop_words()
        model_type, formulas, date = promptconverter.extract_info()
        request_body = promptconverter.create_request_body(model_type, formulas, date)
        print(json.dumps(request_body, indent=2))
    else:
        print("Please Enter a valid prompt")

if __name__ == "__main__":
    main()






