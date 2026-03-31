Here are the step by step instructions to run this:

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

6)Then open : 127.0.0.1:8000/docs in your browser , you will see swagger UI , click on /secure-gateway endpoint and click Try it out

