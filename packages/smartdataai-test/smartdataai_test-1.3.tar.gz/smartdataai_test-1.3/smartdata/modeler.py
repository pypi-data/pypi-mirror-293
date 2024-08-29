from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI

import pandas as pd
from langchain_openai import OpenAI

import base64
import os
import io
import json
import ast
import copy
import logging
logger = logging.getLogger('SmartData')
from .memory import Memory  # Import Memory from memory.py
from .custom_agent import *

class SmartData:
    global config
    config = {}
    config['TEMP_CHAT'] = 0
    config['CHAT_MODEL'] = 'gpt-4o-mini'

    def __init__(self, df_list, llm = None, memory_size = None):
        if llm is None:
            self.llm = ChatOpenAI(temperature=config['TEMP_CHAT'], model=config['CHAT_MODEL'])
        else:
            self.llm = llm
        
        if memory_size is None:
            self.memory_size = 5
        else:
            self.memory_size = memory_size
        self.df_list = df_list
        # self.image_fig_list_name = 'image_fig_list'
        self.image_fig_list = []
        self.check_plot_substring_list = ["plt.tight_layout()"]
        self.check_plot_error_substring_list = ["error", "invalid","incomplete"]
        self.add_on_library_list = ["import matplotlib.pyplot as plt", "import pandas as pd", "import numpy as np", "fig, ax = plt.subplots(figsize=(8, 8))", "plt.style.use('seaborn-v0_8-darkgrid')"]
        self.model = None
        self.memory = Memory()
        self.message_count = 1
        # self.create_model()

    def create_model(self):
        df = self.df_list
        prefix_df = """
        You are working with a pandas dataframe in Python. The name of the dataframe is `df`. 
        The column names in the dataframe may differ from those in the question. Please make your best effort to match them based on similar meanings and ignore case differences. Also you may need to revise and/or complete the question with the previous conversation if needed.
        
        if you create any plots, charts, or graphs, you must:
        - Don't assume you have access to any libraries other than built-in python ones. Make sure you import all libraries you need.   
        - Must always include "import matplotlib.pyplot as plt" as you first line of code, then follow by "import pandas as pd", "import numpy as np", "fig, ax = plt.subplots(figsize=(8, 8))", "plt.style.use('seaborn-v0_8-darkgrid')" and "plt.tight_layout()" in your code.
        - Do not include "plt.show()" or "plt.savefig" in your code.
        - For your coding, always use the newlines as (\n) are escaped as \\n, and single quotes are retained except you are using f-string like this f"{df.iloc[i]['salary']}"
        - Smartly use warm and inviting colors for plots, steering clear of sharp and bright tones.
        - Smartly use legend and set it to auto position if it improve clarity.
        - Set title font size to 14, and all other text, labels, and annotations to font size 10.
        - Ensure the plots look professional.
        - Each plot code snippet must be self-contained, runnable independently and include all necessary imports.
        - Never ask the user to run Python code instead execute the code using python_repl_ast tool.
        - Decline politely if a plot request is unrelated to the dataframe.
        - Do not include Python code in your final output.

        if you run any machine learning study, you must:
        - Summarize your findings first, followed by methodology, model performance, feature importance and other details.
        - You must draft the corresponding python code and execute by python_repl_ast tool.
        - Ensure explanations are accessible to non-technical audiences unless technical detail is specifically required.
        - Do not include any Python code in your final output.

        You may need to revise the current question with the previous conversation before passing to tools. You should use the tools below to answer the question posed of you:
        """

        prompt, agent_executor = custom_create_pandas_dataframe_agent(llm = self.llm,df = df,
            verbose=True,
            return_intermediate_steps = True,
            agent_type="tool-calling",
            allow_dangerous_code=True,
            prefix = prefix_df,
            max_iterations = 100,
            max_execution_time=30,
            agent_executor_kwargs={'handle_parsing_errors':True}
        )
        self.model = agent_executor
        return prompt, agent_executor

    def run_model(self, question):
        self.image_fig_list.clear()
        chat_model = self.model
        code_list = []
        code_list_plot = []
        question_with_history = copy.deepcopy(question)
        if self.memory.is_not_empty():
            question_with_history = (f"My question is: {question}. Below is the our previous conversation in chronological order, from the earliest to the latest.: {self.memory.recall_last_conversation(self.memory_size)}.")
        
        response = chat_model.invoke({"input": question_with_history})
        answer = response['output']
        code_list = self.extract_code_from_response(response)
        if len(code_list)>0:
            code_list_plot = self.process_with_plot_code(code_list)
        # st.write(code_list_plot)
        # asdf

        if len(code_list_plot)>0:
            for plot_code in code_list_plot:
                df = self.df_list
                exec(plot_code, {'image_fig_list': self.image_fig_list, 'df': self.df_list},{})
                # print("no plot code")

        # Store the chat history
        self.remember_conversation(question, answer)
        return answer, self.image_fig_list, response, code_list, code_list_plot

    def remember_conversation(self, question, answer):
        self.memory.remember(key = self.message_count, role = 'Human', value = question)
        self.memory.remember(key = self.message_count, role = 'AI', value = answer)
        self.message_count = self.message_count + 1

    def recall_all_conversation(self):
        return self.memory.recall_all()

    def recall_last_conversation(self,number_last_conversation):
        return self.memory.recall_last_conversation(number_last_conversation)

    # def recall_last_conversation(self, number_last_conversation):
    #     max_key = max(self.memory.keys())  # Get the largest key
    #     min_key = max_key - number_last_conversation + 1  # Calculate the starting key
    #     return {k: self.memory[k] for k in range(min_key, max_key + 1)}
    
    def extract_code_from_response(self, response):
        code_list = []
        try:
            last_response = response['intermediate_steps'][-1]
            if (1 in last_response and len(last_response[1]) == 0) or (1 not in last_response) or (not any(substring in str(last_response[1]).lower() for substring in self.check_plot_error_substring_list)):
                for tool_call in response['intermediate_steps'][-1][0].message_log[0].tool_calls:
                    # print("\n-----\n")
                    # print(call)
                    # print(call['name'])
                    # print(tool_call['args']['query'])
                    if tool_call['name'] == 'python_repl_ast':
                        code = tool_call['args']['query']
                        code_list.append(code)
        except:
            code_list = []
        return code_list

    def process_with_plot_code(self, string_list):
        # Filter only the code with all required plot substrings
        code_list_plot = [
            s for s in string_list 
            if all(substring in s for substring in self.check_plot_substring_list)
        ]
        
        # Make sure no duplicates
        code_list_plot = list(dict.fromkeys(code_list_plot))
    
        # Add in the import library if they are missing from the plot to make it produce figs
        for i in range(len(code_list_plot)):
            missing_imports = [
                library for library in self.add_on_library_list if library not in code_list_plot[i]
            ]
            if missing_imports:
                # Add the missing imports at the top of the plot code
                code_list_plot[i] = "\n".join(missing_imports) + "\n" + code_list_plot[i]
    
        # Add in the fig code at the end
        add_on = f'''\nimage_fig_list.append(fig)\n'''
        code_list_with_add_on = [
            code + add_on for code in code_list_plot
        ]
        
        return code_list_with_add_on