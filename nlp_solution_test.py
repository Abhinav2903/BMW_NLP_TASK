import unittest
from nlp_solution import NlpPromptConverter

class NlpPromptConverterTest(unittest.TestCase):

    def test_extract_model_type(self):
        prompt = "I am planning to order the BMW M8 with a sunroof or panorama glass roof sky lounge, and the M Sport Package on 12th April 2018. Is this configuration possible?"
        prompt_converter = NlpPromptConverter(prompt)
        model_type = prompt_converter.extract_model_type([])
        self.assertEqual(model_type, ["DZ01"])

    def test_evaluate_formula(self):
        prompt = "Hello, is the X7 xDrive40i available without a panorama glass roof and with the EU Comfort Package. I need the vehicle on the 8th of November 2024."
        prompt_converter = NlpPromptConverter(prompt)
        formulas = prompt_converter.evaluate_formula([])
        self.assertEqual(formulas, ["-S402A+P7LGA"])

    def test_extract_date(self):
        prompt = "I need the car delivered by the end of October 2024."
        prompt_converter = NlpPromptConverter(prompt)
        date = prompt_converter.extract_date(None)
        self.assertEqual(date, "2024-10-31")

    def test_create_request_body(self):
        prompt = "I want to order a BMW iX with right-hand drive configuration. I will be ordering it at the start of October 2022."
        prompt_converter = NlpPromptConverter(prompt)
        model_type = "21CF"
        formulas = ["+RL"]
        date = "2022-10-01"
        request_body = prompt_converter.create_request_body(model_type, formulas, date)
        expected_body = {
            "modelTypeCodes": ["21CF"],
            "booleanFormulas": ["+RL"],
            "dates": ["2022-10-01"]
        }
        self.assertEqual(request_body, expected_body)

if __name__ == "__main__":
    unittest.main()
