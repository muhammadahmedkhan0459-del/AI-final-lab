Here are the step by step instructions to run this:

# I am on windows enviroment I am using python and pip in command , you might have to use python3  and pip3 and you might have to build virtual environment using follwoing command
# python3 -m venv venv
# source venv/bin/activate


# I am using My Gemini API key you might you have to use yours if my doesnot work for you ( even though its sensitive data , but you may try out )
# You will change 2 lines in code to use your gemini api key , following 2 lines
# GEMINI_API_KEY = "<Your key>"
# GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=<Your key>"

1)Clone the repo:
git clone https://github.com/muhammadahmedkhan0459-del/AI-mid-lab.git

2) Navigate to folder
cd AI-mid-lab

3) Installed required dependencies
pip install fastapi uvicorn requests presidio-analyzer presidio-anonymizer spacy

4)Installed required dependencies ( you can also install en_core_web_lg in place of en_core_web_sm)
python -m spacy download en_core_web_sm

5) Run app 
uvicorn main:app --reload

If this fails:
Try:
python3 -m uvicorn main:app --reload

6)Then open : 127.0.0.1:8000/docs in your browser , you will see swagger UI , click on /secure-gateway endpoint and click Try it out 
 Then you will see Json " str : text " 
 To enter your input : replace the "text" word with your prompt for LLM , you can try variety of those to check responses.

