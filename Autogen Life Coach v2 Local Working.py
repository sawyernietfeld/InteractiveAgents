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
groupchat = autogen.GroupChat(agents=[user_proxy, LifeCoach, Planner, critic], messages=[], max_round=50)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

user_proxy.initiate_chat(
    manager,
    message="""
Build a straightforward plan for the day that takes the human toward his objectives of: 1)Being a successful entrepreneur in a domain he has passion and a skillset for, 2)Enjoys life and it has meaning and connection, and 3)Had a healthy mental, physical, environmental, and emotional state of mind. Be concise.
""",
)