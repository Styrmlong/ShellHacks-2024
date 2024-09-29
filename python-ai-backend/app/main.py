import google.generativeai as genai
import os
import json
from flask import Flask
from flask import request
import requests
from flask import jsonify
from SECRETS import GOOGLE_API_KEY


app = Flask(__name__)


@app.route("/")
def index():
    return { 'status' : 'ok' }

# Allowed Parameters:
#    years_in_college
#    field_of_study
#    gender_self_describe
#    florida_resident
#    first_gen_college_student
#    race_self_describe
#    mean_yearly_income
#    expected_yearly_scholarships
#    housing

#Need to add /prompt to extension to ge it running correctly (note: add the applicable weblinks file)
@app.route("/prompt", methods=['GET'])
def prompt():
    print("Request:", request.args)
    genai.configure(api_key=GOOGLE_API_KEY)

    prompt_data=""

    for arg in request.args:
        print("ARG:",arg)
        if arg in ["years_in_college","field_of_study","gender_self_describe",
                    "florida_resident","first_gen_college_student","race_self_describe",
                    "mean_yearly_income","expected_yearly_scholarships","housing","essay_prompt","essay_title","essay_content"]:
            prompt_data+=arg+":"+request.args[arg]+" "
            print("prompt:",prompt_data)
        else:
            return "Unknown Prameter: "+arg,400
    try:
        # call the gemini-1.5-flash
        model = genai.GenerativeModel("gemini-1.5-flash")
        print("Generating content...")
        response = model.generate_content(["Give me a sample essay for scholarships using these parameters.", prompt_data])
        print(response)
        if response.text:
            return response.text, 200
        else:
            return "Error", 408 
    except Exception as e:
        print("Error:",e)
        return str(e), 400
        

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

