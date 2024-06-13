from semantic_kernel.functions import kernel_function
from typing import Annotated
from azure.core.credentials import AzureKeyCredential

from azure.search.documents.models import VectorizableTextQuery
from azure.search.documents.aio import SearchClient
import os


class AISearchPlugin:
    """A plugin that allows for the execution of AI Search queries against a text input."""

    @staticmethod
    def system_prompt() -> str:
        return """Use the AI Search to return documents that have been indexed, that might be relevant for a piece of text to aid understanding. Documents ingested here could be relevant to anything, so AI Search should always be used. Always provide references to any documents you use."""

    @kernel_function(
        description="Runs an hybrid semantic search against some text to return relevant documents that are indexed within AI Search.",
        name="RunAISearchOnText",
    )
    async def run_ai_search_on_text(
        self, text: Annotated[str, "The text to run a semantic search against."]
    ) -> list[dict]:
        """Sends an text query to AI Search and uses Semantic Ranking to return a result.

        Args:
        ----
            text (str): The text to run the search against.

        Returns:
        ----
            list[dict]: The response from the search that is ranked according to relevancy.
        """

        credential = AzureKeyCredential(os.environ["AI_SEARCH_API_KEY"])

        search_client = SearchClient(
            endpoint=os.environ["AI_SEARCH_ENDPOINT"],
            index_name="< YOUR INDEX NAME >",
            credential=credential,
        )

        vector_query = VectorizableTextQuery(
            text=text,
            k_nearest_neighbors=5,
            fields="< YOUR VECTOR FIELDS e.g. title_vector,chunk_vector >",
        )

        results = await search_client.search(
            top=2,
            query_type="semantic",
            semantic_configuration_name="< YOUR SEMANTIC CONFIG NAME >",
            search_text=text,
            select="< FIELDS TO RETURN e.g. title,chunk>",
            vector_queries=[vector_query],
        )

        documents = [
            document async for result in results.by_page() async for document in result
        ]
        return documents
