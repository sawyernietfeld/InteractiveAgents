from flask import Flask, request, jsonify
from flask_cors import CORS
import autogen

# Initialize the Flask application
app = Flask(__name__)
CORS(app)  # This is to allow cross-origin requests

import autogen
import openai
import os

config_list = [
    {
        "api_type": "open_ai",
        "api_base": "http://localhost:1234/v1",
        "api_key": "NULL",
    }
]

llm_config={
    "request_timeout": 600,
    "seed": 42,
    "config_list": config_list,
    "temperature": 0.3
}

user_proxy = autogen.UserProxyAgent(
   name="Admin",
   system_message="A human admin. Interact with the planner to discuss the plan. Plan sign-off needs to be approved by this admin.",
   code_execution_config=False,
)
LifeCoach = autogen.AssistantAgent(
    name="LifeCoach",
    llm_config=llm_config,
    system_message='''Life Coach. You follow an approved plan. You are a dedicated professional & expert who guides individuals towards enhancing their quality of life, fostering personal success, and discovering joy and connection.
    You provide personalized support and strategies to help clients navigate life's challenges and achieve their goals.
    By creating supportive and motivating guidance, a life coach empowers clients to unlock their full potential and embrace a fulfilling life.
    Pass questions back to the planner or admin for the user to answer if additional information or context is needed.
''',
)

Planner = autogen.AssistantAgent(
    name="Planner",
    system_message='''Planner. Suggest a plan. Revise the plan based on feedback from admin and critic, until admin approval.
The plan may involve a Life Coach who can provide guidance in life.
Explain the plan first. Be clear which step is performed by a Life Coach, and which steps wont, if any.
Pass questions back to the admin for the user to answer if additional information or context is needed.
''',
    llm_config=llm_config,
)
critic = autogen.AssistantAgent(
    name="Critic",
    system_message="Critic. Double check plan, claims, and the advice quality and provide feedback. Check whether the plan includes positive, actionable information that allows the users a good chance at success. Think deeply about this. If it doesn't, send the ask back to the planner and experts.",
    llm_config=llm_config,
)
groupchat = autogen.GroupChat(agents=[user_proxy, LifeCoach, Planner, critic], messages=[], max_round=6)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# Define a route to receive commands from the UI
@app.route('/send-command', methods=['POST'])
def send_command():
    data = request.json
    command = data.get('command')

    # Pass the 'manager' object to the function
    response = process_command(command, manager)

    return jsonify({'response': response})

def process_command(command, manager):
    print("Received command:", command)
    # Initiate chat with the received command instead of a hardcoded message
    user_proxy.initiate_chat(
        manager,
        message=command
    )
    # Process the message
    manager.process_round()  # Process the message
    response = manager.groupchat.get_latest_response()  # Get the latest response from the chat
    print("Response:", response)
    return response

# This part starts the server
if __name__ == '__main__':
    app.run(port=5000)
