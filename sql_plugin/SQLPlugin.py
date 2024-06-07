from semantic_kernel.functions import kernel_function
import aioodbc
from typing import Annotated
import jaydebeapi

class SQLPlugin:
    @kernel_function(description="Returns SQL schema for the databases.", name="GetSQLSchemas")
    def get_sql_schemas(self):
        """Get the schemas for the database"""

        schema = """Use the following SQL Schema Views and their associated definitions when you need to fetch information from a database:

        vGetAllCategories View. Use this to get details about the categories available.
        CREATE VIEW [SalesLT].[vGetAllCategories] WITH SCHEMABINDING AS -- Returns the CustomerID, first name, and last name for the specified customer. WITH CategoryCTE([ParentProductCategoryID], [ProductCategoryID], [Name]) AS ( SELECT [ParentProductCategoryID], [ProductCategoryID], [Name] FROM SalesLT.ProductCategory WHERE ParentProductCategoryID IS NULL UNION ALL SELECT C.[ParentProductCategoryID], C.[ProductCategoryID], C.[Name] FROM SalesLT.ProductCategory AS C INNER JOIN CategoryCTE AS BC ON BC.ProductCategoryID = C.ParentProductCategoryID ) SELECT PC.[Name] AS [ParentProductCategoryName], CCTE.[Name] as [ProductCategoryName], CCTE.[ProductCategoryID] FROM CategoryCTE AS CCTE JOIN SalesLT.ProductCategory AS PC ON PC.[ProductCategoryID] = CCTE.[ParentProductCategoryID]

        vProductAndDescription View. Use this to get details about the products and their associated descriptions.
        CREATE VIEW [SalesLT].[vProductAndDescription] WITH SCHEMABINDING AS -- View (indexed or standard) to display products and product descriptions by language. SELECT p.[ProductID] ,p.[Name] ,pm.[Name] AS [ProductModel] ,pmx.[Culture] ,pd.[Description] FROM [SalesLT].[Product] p INNER JOIN [SalesLT].[ProductModel] pm ON p.[ProductModelID] = pm.[ProductModelID] INNER JOIN [SalesLT].[ProductModelProductDescription] pmx ON pm.[ProductModelID] = pmx.[ProductModelID] INNER JOIN [SalesLT].[ProductDescription] pd ON pmx.[ProductDescriptionID] = pd.[ProductDescriptionID]
        
        Do not use any other tables / views, other than those defined above."""

        return schema

    @kernel_function(description="Runs an SQL query against the SQL Database to extract information.", name="RunSQLQuery")
    async def run_sql_query(self, query: Annotated[str, "The SQL query to run against the DB"]):
        """Sends an SQL Query to the SQL Databases and returns to the result.
        
        Args:
            query: The query to run against the DB.
            
        Returns:
            The response"""

        connection_string = "CONNECTION STRING"
        async with await aioodbc.connect(dsn=connection_string) as sql_db_client:
            async with sql_db_client.cursor() as cursor:
                await cursor.execute(query)

                columns = [column[0] for column in cursor.description]

                rows = await cursor.fetchall()
                results = [
                    dict(zip(columns, returned_row)) for returned_row in rows
                ]

        return results
