# BMW_NLP_TASK

NLP Prompt Converter

This Python script is designed to convert natural language prompts into a structured request body for a specific task. It utilizes various natural language processing techniques to extract relevant information from the prompt.
Dependencies

The First requirement is to have python 3.11.xx installed and the python variable to be set in the system

The script requires the following dependencies:

    dateutil.parser from the dateutil library
    word_tokenize from the nltk.tokenize module
    stopwords from the nltk.corpus module
    calendar module
    abbreviations from a custom module called abbreviations
    model_type_codes from a custom module called model_type_codes
    json module
    re module
    nltk library (requires additional downloads, see instructions below)
    numpy library
    keyboard library

Make sure to install these dependencies before running the script.
Installation

    Clone the repository(https://github.com/Abhinav2903/BMW_NLP_TASK.git) or download the script file or unzip form the zip folder provided.

    Install the required dependencies using the following command:

pip install python-dateutil nltk numpy
pip install keyboard

Download the additional resources for NLTK by running the following commands:

    python -m nltk.downloader averaged_perceptron_tagger
    python -m nltk.downloader maxent_ne_chunker
    python -m nltk.downloader words

    Place the custom modules (abbreviations.py and model_type_codes.py) in the same directory as the script.

Usage

    Run the script using the following command:

    python .\nlp_solution.py

    Enter a natural language prompt when prompted by the script.

    The script will extract relevant information from the prompt, such as model type, boolean formulas, and date.

    The script will then create a request body in JSON format based on the extracted information.

    The generated request body will be displayed in the console.

    Enter Esc to return back from the prompt.

    Repeat the process for additional prompts.

    Additionaly a .exe file is also created using pyinstaller.To install pyinstaller use  
    
    pip install pyinstaller

    pyinstaller --onefile .\nlp_solution.py create the nlp_solution.exe file in dist folder

    Just double click and run the .exe and test for the prompt, if nothing happen press enter than some libraries might download and will work accordingly

    Enter Esc to Close the prompt.

    Repeat the process for additional prompts.

    To Run the test cases run the following command:

    python .\nlp_solution_test.py

