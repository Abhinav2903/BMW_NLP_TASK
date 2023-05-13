
# Define all the import  that are needed for the task to be completed
from abbrevations import abbreviations;
from model_type_codecs import model_type_codes;
import json;
import re;

# Define the class that handles all the functions and 
class NlpPromptConverter:


    def __init__(self,prompt):
        self.prompt = prompt

    # Define function to evaluate boolean formula have to modify accordingly
    def evaluate_formula(self,formula):
        for abbreviation, meaning in abbreviations.items():
            formula = formula.replace(abbreviation, meaning)
        boolean_formula = eval(formula)
        return boolean_formula;
    
    # define the function to extract relevant information from the prompt provided
    def extract_info(self):
        model_type = self.extract_model_type()
        formulas = self.evaluate_formula(formula)
        date = self.extract_date()
        return model_type, formulas, date;

    # Define the funtion for extracting model type codecs
    def extract_model_type(self):
        for code, description in model_type_codes.items():
            if description.lower() in self.prompt.lower():
                model_type = code
                break
        return model_type;

    # define the function for extracting date
    def extract_date(self):
        matches = re.findall(r"\b\d{4}-\d{2}-\d{2}\b", self.prompt)
        if matches:
            date = matches[0]
        return date;

    # Function to convert extracted information into a request body
    def create_request_body(self,model_type, formulas, date):
        model_type, formulas, date = self.extract_info(self.prompt)

        evaluated_formulas = []
        for formula in formulas:
            result = self.evaluate_formula(formula)
            evaluated_formulas.append(result)

        request_body = self.create_request_body(model_type, evaluated_formulas, date)
        return request_body



def main():
    prompt = input("Enter the prompt")
    if(prompt!= None):
        promptconverter = NlpPromptConverter(prompt)
        model_type, formulas, date = promptconverter.extract_info()

        request_body = promptconverter.create_request_body(model_type, formulas, date)
        print(json.dumps(request_body, indent=2))

if __name__ == "__main__":
    main()






