# Databricks notebook source
# MAGIC %pip install --force-reinstall typing-extensions==4.5
# MAGIC %pip install  --force-reinstall semantic-kernel

# COMMAND ----------

# MAGIC %pip install azure-search
# MAGIC %pip install azure-search-documents
# MAGIC %pip install aioodbc
# MAGIC %pip install jaydebeapi

# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------

# Copyright (c) Microsoft. All rights reserved.

import asyncio
import logging

from semantic_kernel.connectors.ai.open_ai import (
    AzureAISearchDataSource,
    AzureChatCompletion,
    AzureChatPromptExecutionSettings,
    ExtraBody,
)
from semantic_kernel.connectors.memory.azure_cognitive_search.azure_ai_search_settings import AzureAISearchSettings
from semantic_kernel.contents import ChatHistory
from semantic_kernel.functions import KernelArguments
from semantic_kernel.kernel import Kernel
from semantic_kernel.prompt_template import InputVariable, PromptTemplateConfig
from sql_plugin.SQLPlugin import SQLPlugin
from semantic_kernel.connectors.ai.function_call_behavior import FunctionCallBehavior
from semantic_kernel.planners.function_calling_stepwise_planner import (
    FunctionCallingStepwisePlanner,
    FunctionCallingStepwisePlannerOptions,
)

kernel = Kernel()
logging.basicConfig(level=logging.DEBUG)

# COMMAND ----------

# fields_mapping = {
#     "titleField": "metadata_storage_name",
#     "contentFields": ["content"],
#     "vectorFields": ["vector"],
# }
# embedding_dependency = {
#     "type": "DeploymentName",
#     "deploymentName": "text-embedding-ada-002"
# }
# azure_ai_search_settings = AzureAISearchSettings(api_key="API KEY", endpoint="ENDPOINT", index_name="my-search-index", fields_mapping=fields_mapping, query_type="vector", embedding_dependency=embedding_dependency)

# COMMAND ----------

# az_source = AzureAISearchDataSource.from_azure_ai_search_settings(azure_ai_search_settings)
# extra = ExtraBody(data_sources=[az_source])
service_id = "chat-gpt"
# req_settings = AzureChatPromptExecutionSettings(service_id=service_id, extra_body=extra)

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

sql_db_plugin = kernel.add_plugin(SQLPlugin(), plugin_name="SQLDB")

# COMMAND ----------

options = FunctionCallingStepwisePlannerOptions(
    max_iterations=10,
    max_tokens=4000
)

planner = FunctionCallingStepwisePlanner(service_id=service_id, options=options)

# COMMAND ----------

question = "Find 5 of the different categories that exist witin the sales data."
response = await planner.invoke(kernel, question)

# COMMAND ----------

print(f"Q: {question}\nA: {response.final_answer}\n")

# COMMAND ----------

print(f"Chat history: {response.chat_history}\n")

# COMMAND ----------

