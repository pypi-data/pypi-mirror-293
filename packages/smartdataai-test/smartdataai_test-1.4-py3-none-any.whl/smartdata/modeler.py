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

from .config import Config
from .memory import Memory  # Import Memory from memory.py
from .custom_agent import *

global config
config = dict(Config.__dict__)

class SmartData:
    def __init__(self, df_list, llm = None, show_detail = config['SHOW_DETAIL'], memory_size = config['MEMORY_SIZE'], 
                 max_iterations = config['MAX_ITERATIONS'], max_execution_time = config['MAX_EXECUTION_TIME']):
        
        # Use ChatGPT 4o-mini by default
        if llm is None:
            chat_llm = ChatOpenAI(temperature=config['TEMP_CHAT'], model=config['CHAT_MODEL'])
            self.llm = chat_llm
        else:
            self.llm = llm
        
        self.df_list = df_list
        self.memory_size = memory_size
        self.max_iterations = max_iterations
        self.max_execution_time = max_execution_time
        self.show_detail = show_detail
        # self.image_fig_list_name = 'image_fig_list'
        self.image_fig_list = []
        self.check_plot_substring_list = config['CHECK_PLOT_SUBSTRING_LIST']
        self.check_plot_error_substring_list = config['CHECK_PLOT_ERROR_SUBSTRING_LIST']
        self.add_on_library_list = config["ADD_ON_LIBRARY_LIST"]
        self.model = None
        self.memory = Memory()
        self.message_count = 1
        # self.create_model()

    def create_model(self):
        df = self.df_list
        prefix_df = config['DEFAULT_PREFIX_SINGLE_DF']

        prompt, agent_executor = custom_create_pandas_dataframe_agent(llm = self.llm,df = df,
            verbose=self.show_detail,
            return_intermediate_steps = True,
            agent_type="tool-calling",
            allow_dangerous_code=True,
            prefix = prefix_df,
            max_iterations = self.max_iterations,
            max_execution_time=self.max_execution_time,
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
            question_with_history = f"My question is: {question}. Below is the our previous conversation in chronological order, from the earliest to the latest.: {self.memory.recall_last_conversation(self.memory_size)}."
        
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
        if any(error_substring in str(answer) for error_substring in config['AGENT_STOP_SUBSTRING_LIST']):
            answer = config['AGENT_STOP_ANSWER']

        return answer, self.image_fig_list, response, code_list, code_list_plot

    def remember_conversation(self, question, answer):
        self.memory.remember(key = self.message_count, role = 'Human', value = question)
        self.memory.remember(key = self.message_count, role = 'AI', value = answer)
        self.message_count = self.message_count + 1

    def recall_all_conversation(self):
        return self.memory.recall_all()

    def recall_last_conversation(self,number_last_conversation):
        return self.memory.recall_last_conversation(number_last_conversation)

    def clear_all_conversation(self):
        return self.memory.clear_all_conversation()
    
    def extract_code_from_response(self, response):
        code_list = []
        try:
            last_response = response['intermediate_steps'][-1]
            if (len(last_response)>1 and len(str(last_response[1])) == 0) or (len(last_response)==1) or ((len(last_response)>1) and (not any(substring in str(last_response[1]).lower() for substring in self.check_plot_error_substring_list))):
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