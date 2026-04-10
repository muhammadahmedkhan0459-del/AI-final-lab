from fastapi import FastAPI
from pydantic import BaseModel
import requests
import time
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_analyzer import PatternRecognizer, Pattern

app = FastAPI(title="LLM Security Gateway Demo")

class UserInput(BaseModel):
    text: str

GEMINI_API_KEY = "xxx"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=xxx"

BLOCK_THRESHOLD   = 5
WARNING_THRESHOLD = 3
PII_CONFIDENCE    = 0.7

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

pk_phone = PatternRecognizer(
    supported_entity="PK_PHONE",
    patterns=[
        Pattern(
            name="pk_phone",
            regex=r"(\+92|0)[0-9]{10}",
            score=0.8
        )
    ]
)
api_key = PatternRecognizer(
    supported_entity="API_KEY",
    patterns=[
        Pattern(
            name="api_key",
            regex=r"AIza[0-9A-Za-z\-_]{35}",
            score=0.9
        )
    ]
)
internal_id = PatternRecognizer(
    supported_entity="INTERNAL_ID",
    patterns=[
        Pattern(
            name="internal_id",
            regex=r"EMP-[0-9]{4}",
            score=0.85
        )
    ]
)

analyzer.registry.add_recognizer(pk_phone)
analyzer.registry.add_recognizer(api_key)
analyzer.registry.add_recognizer(internal_id)

@app.get("/")
def root():
    return {"message": "Good-Connected"}

@app.post("/secure-gateway")
def secure_gateway(input: UserInput):
    user_text = input.text

    total_start = time.time()

    score = 0
    if "ignore previous instructions" in user_text.lower():
        score += 3
    if "jailbreak" in user_text.lower():
        score += 3
    if "pretend you are" in user_text.lower():
        score += 2
    if "forget everything" in user_text.lower():
        score += 2
    if "you are now" in user_text.lower():
        score += 1

    if score >= BLOCK_THRESHOLD:
        return {
            "status": "Blocked",
            "score": score,
            "original_text": user_text,
            "processed_text": None,
            "gemini_response": None,
            "latency_seconds": round(time.time() - total_start, 4)
        }

    status = "Warning" if score >= WARNING_THRESHOLD else "Allowed"

    try:
        results = analyzer.analyze(text=user_text, language="en")
        anonymized_input = anonymizer.anonymize(
            text=user_text,
            analyzer_results=results
        )
        processed_text = anonymized_input.text
        print(results)
    except Exception as e:
        processed_text = user_text

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": processed_text}
                ]
            }
        ]
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(GEMINI_API_URL, json=payload, headers=headers)
        data = response.json()
        print("GEMINI RAW RESPONSE:", data)
        gemini_response = data["candidates"][0]["content"]["parts"][0]["text"]
                #data = {
    #"candidates": [
     #   {
      #      "content": {
       #         "parts": [
        #            {
         #               "text": "reponse"
          #          }
           #     ],
            #    "role": "model"
         #   },
          #  "finishReason": "STOP",
           # "index": 0
        #}
    #]
#}
    except Exception as e:
        gemini_response = f"Gemini error: {str(e)}"

    try:
        results2 = analyzer.analyze(text=gemini_response, language="en")
        anonymized_output = anonymizer.anonymize(
            text=gemini_response,
            analyzer_results=results2
        )
        gemini_response = anonymized_output.text
    except Exception as e:
        gemini_response = gemini_response

    return {
        "status": status,
        "score": score,
        "original_text": user_text,
        "processed_text": processed_text,
        "gemini_response": gemini_response,
        "latency_seconds": round(time.time() - total_start, 4)
    }
