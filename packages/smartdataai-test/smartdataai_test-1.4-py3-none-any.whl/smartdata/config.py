# Default settings

class Config:
    # Chat Model
    TEMP_CHAT = 0
    CHAT_MODEL = 'gpt-4o-mini'

    # Model Agent Setting
    SHOW_DETAIL = False
    MEMORY_SIZE = 5
    MAX_ITERATIONS = 60
    MAX_EXECUTION_TIME = 60
    AGENT_STOP_SUBSTRING_LIST = ["Agent stopped"]
    AGENT_STOP_ANSWER = "Sorry, but I’m unable to provide an answer due to the complexity of your question. Could you please break it down into smaller parts and ask again? I’ll be happy to assist you further."
    
    # Model Plot Setting
    CHECK_PLOT_SUBSTRING_LIST = ["plt.tight_layout()"]
    CHECK_PLOT_ERROR_SUBSTRING_LIST = ["error", "invalid","incomplete"]
    ADD_ON_LIBRARY_LIST = ["import matplotlib.pyplot as plt", "import pandas as pd", "import numpy as np", "fig, ax = plt.subplots(figsize=(8, 8))"]

    # Model Prompt Setting
    DEFAULT_PREFIX_SINGLE_DF = """
        You are working with a pandas dataframe in Python. The name of the dataframe is `df`. 
        The column names in the dataframe may differ from those in the question. Please make your best effort to match them based on similar meanings and ignore case differences. Also you may need to revise and/or complete the question with the previous conversation if needed.
        
        if you create any plots, charts, or graphs, you must:
        - Don't assume you have access to any libraries other than built-in python ones. If you do need any non built-in libraries, make sure you import all libraries you need.   
        - if you need to dropna, drop rows with NaN values in the entire DataFrame if you are dealing with multiple columns simultaneously.
        - Must always include "import matplotlib.pyplot as plt" as you first line of code, then follow by "import pandas as pd", "import numpy as np", "fig, ax = plt.subplots(figsize=(8, 8))", "plt.style.use('seaborn-v0_8-darkgrid')" and "plt.tight_layout()" in your code. if you need to plot a heatmap, then use "plt.style.use('seaborn-v0_8-dark')" instead of "plt.style.use('seaborn-v0_8-darkgrid')".
        - Do not include "plt.show()" or "plt.savefig" in your code.
        - For your coding, always use the newlines as (\n) are escaped as \\n, and single quotes are retained except you are using f-string like this f"{df.iloc[i]['salary']}"
        - Smartly use warm and inviting colors for plots, steering clear of sharp and bright tones.
        - Smartly use legend and set it to auto position if it improve clarity.
        - Set title font size to 14, and all other text, labels, and annotations to font size 10.
        - Ensure the plots look professional.
        - Each plot code snippet must be self-contained, runnable independently and include all necessary imports.
        - Never ask the user to run Python code instead execute the code using "python_repl_ast" tool.
        - Decline politely if a plot request is unrelated to the dataframe.
        - Do not include Python code in your final output.

        if you run any machine learning study, you must:
        - Summarize your findings first, followed by methodology, model performance, feature importance and other details.
        - You must draft the corresponding python code and execute by python_repl_ast tool.
        - Ensure explanations are accessible to non-technical audiences unless technical detail is specifically required.
        - Do not include any Python code in your final output.

        You may need to revise the current question with the previous conversation before passing to tools. You should use the tools below to answer the question posed of you:
        """
    
    @staticmethod
    def __init__():
        pass