# Databricks notebook source
# MAGIC %pip install --force-reinstall typing-extensions==4.5
# MAGIC %pip install  --force-reinstall semantic-kernel

# COMMAND ----------

# MAGIC %pip install azure-search
# MAGIC %pip install azure-search-documents
# MAGIC %pip install aioodbc

# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------

# Copyright (c) Microsoft. All rights reserved.

import logging

from semantic_kernel.connectors.ai.open_ai import (
    AzureChatCompletion,
)
from semantic_kernel.kernel import Kernel
from sql_plugin.sql_plugin import SQLPlugin
from ai_search_plugin.ai_search_plugin import AISearchPlugin
from semantic_kernel.planners.function_calling_stepwise_planner import (
    FunctionCallingStepwisePlanner,
    FunctionCallingStepwisePlannerOptions,
)

kernel = Kernel()
logging.basicConfig(level=logging.DEBUG)

# COMMAND ----------

service_id = "gpt-4"

# COMMAND ----------

# When using data, use the 2024-02-15-preview API version.
chat_service = AzureChatCompletion(
    service_id="chat-gpt",
    deployment_name="gpt-4",
    endpoint="ENDPOINT",
    api_key="API KEY",
)
kernel.add_service(chat_service)

# COMMAND ----------

kernel.add_plugin(SQLPlugin(), plugin_name="SQLDB")

# COMMAND ----------

kernel.add_plugin(AISearchPlugin(), plugin_name="AISearch")

# COMMAND ----------

options = FunctionCallingStepwisePlannerOptions(max_iterations=10, max_tokens=4000)

planner = FunctionCallingStepwisePlanner(service_id=service_id, options=options)

# COMMAND ----------

question = "Find 5 of the different categories that exist within the sales data?"
full_prompt = f"""Here is some additional information that you might find useful in determining which functions to call to fulfill the user question. 

AI Search Information:
{AISearchPlugin.system_prompt()}

SQL Database Information:
{SQLPlugin.system_prompt()}

User Question:
{question}"""

question = "Find 5 of the different categories that exist within the sales data."
response = await planner.invoke(kernel, full_prompt)

# COMMAND ----------

print(f"Q: {question}\nA: {response.final_answer}\n")

# COMMAND ----------

print(f"Chat history: {response.chat_history}\n")

# COMMAND ----------
