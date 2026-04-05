Here are the step by step instructions to run this:  

I am on windows enviroment I am using python and pip in command , you might have to use python3  and pip3 as you are on mac and you might have to build virtual environment using follwoing command  
python3 -m venv venv  
source venv/bin/activate  

I am using My Gemini API key you might you have to use yours if my doesnot work for you ( even though its sensitive data , but you may try out )  
You will change 2 lines in code to use your gemini api key , following 2 lines  
GEMINI_API_KEY = "paste your key here"  
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=paste your key here"  

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
Then you will see Json  
{
  "text": "string"
}  
To enter your input : replace the "string" word with your prompt for LLM , you can try variety of those to check responses.


If there are issues in your python env , try this     
Open Terminal and run: python3 -m venv myenv ( This is for mac , in windows you write python not python3 )  
2)If you use bash or zsh: myenv/bin/activate ---> ( This is for mac , in my windows it is venv\Scripts\activate )  
If you use fish shell instead of bash or zsh: source myenv/bin/activate.fish
