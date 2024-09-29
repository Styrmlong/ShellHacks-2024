import google.generativeai as genai
import os
import json
from flask import Flask
from flask import request
import requests
from flask import jsonify
from SECRETS import GOOGLE_API_KEY
from google.cloud import aiplatform
from google.api_core.client_options import ClientOptions

PROJECT_ID = "88509990376"
LOCATION = "us-east1"

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

#Need to add chatty to extension to ge it running correctly (note: add the applicable weblinks file)
@app.route("/chatty", methods=['GET'])
def chatty():
    print("Request:", request.args)
    genai.configure(api_key=GOOGLE_API_KEY)

    prompt_data=""

    for arg in request.args:
        print("ARG:",arg)
        if arg in ["years_in_college","field_of_study","gender_self_describe",
                    "florida_resident","first_gen_college_student","race_self_describe",
                    "mean_yearly_income","expected_yearly_scholarships","housing"]:
            prompt_data+=arg+":"+request.args[arg]+" "
            print("prompt:",prompt_data)
        else:
            return "Unknown Parameter: "+arg,400
    try:
        # call the gemini-1.5-flash
        model = genai.GenerativeModel("gemini-1.5-flash")
        print("Hey! This is Chat! I can only answer questions in English...for now! I'm due to fight the owl soon.") #Insert Black Panther Chibi
        print("I can help suggest scholarship resources and answer questions related to deadlines!")
        print("Please select what you want to talk to me about from the options below!")
        def questions(choice):
            #Done this way to allow buttons to point out more easily and force a choice
            match choice:
                case "Jobs": 
                    print("I see that you've chosen to talk about job opportunities.")
                    return "Jobs"
                case "Scholarships":
                    print("I see that you've chosen to talk about scholarship opportunities.")
                    return "Scholarships"
                case "Deadlines":
                    print("I see that you've chosen to talk about deadlines.")
                    return "Deadlines"
                case _:
                    return "I'm sorry. I did not understand what you wanted. Please try again."

        def get_next_responses(history, prompt_data, choice):
            """
            Generates the top 3 most likely responses using Gemini.

            Args:
                history: A dictionary containing the context of the conversation
                prompt_data: Data related to user.
                choice: The user's previous choice.

            Returns:
                A list of the top 3 most likely responses.
            """
        
        
        prompt = f"""
            history=[
                    {"role": "user", "parts": "Hello"},
                    {"role": "model", "parts": "Hey! This is Chat! I can only answer questions in English...for now! I'm due to fight the owl soon."},
                    {"role": "model", "parts": "I can help suggest scholarship resources and answer questions related to deadlines!"},
                    {"role": "model", "parts": "Please select what you want to talk to me about from the options below!"}
            ]
            User details: {prompt_data}
            User's last choice: {choice}

            Generate 3 possible responses that are relevant to the conversation:
        """

        # Create the instance for prediction
        instance = {"content": prompt}

        # Set the endpoint for Gemini
        endpoint = "projects/{}/locations/{}/endpoints/{}".format(
            PROJECT_ID, LOCATION, "chatty")

        # Make the prediction request
        response = client.predict(
            endpoint=endpoint, instances=[instance], parameters={"temperature": 1}
        )

        # Extract the responses from the prediction results
        responses = [prediction["content"] for prediction in response.predictions]

        # Return the top 3 responses
        return responses[:3]

        def user_select_response(responses):
            """
            Presents the user with the top 3 responses and allows them to select one.

            Args:
                responses: A list of the top 3 most likely responses.

            Returns:
                The user's selected response.
            """

        print("Here are 3 possible responses:")
        for i, response in enumerate(responses):
            print(f"{i+1}. {response}")

        while True:
            try:
                user_choice = int(input("Choose a response (1-3): "))
                if 1 <= user_choice <= 3:
                    return responses[user_choice - 1]
                else:
                    print("Invalid choice, please enter a number between 1 and 3.")
            except ValueError:
                print("Invalid input, please enter a number.")
  
    except Exception as e:
        print("Error:",e)
        return str(e), 400
        

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)