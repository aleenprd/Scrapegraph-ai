"""
ParseNodeDepthK Module
"""
import re
from typing import List, Optional, Tuple
from .base_node import BaseNode
from ..utils.convert_to_md import convert_to_md
from langchain_community.document_transformers import Html2TextTransformer

class ParseNodeDepthK(BaseNode):
    """
    A node responsible for parsing HTML content from a series of documents.

    This node enhances the scraping workflow by allowing for targeted extraction of
    content, thereby optimizing the processing of large HTML documents.

    Attributes:
        verbose (bool): A flag indicating whether to show print statements during execution.

    Args:
        input (str): Boolean expression defining the input keys needed from the state.
        output (List[str]): List of output keys to be updated in the state.
        node_config (dict): Additional configuration for the node.
        node_name (str): The unique identifier name for the node, defaulting to "Parse".
    """

    def __init__(
        self,
        input: str,
        output: List[str],
        node_config: Optional[dict] = None,
        node_name: str = "ParseNodeDepthK",
    ):
        super().__init__(node_name, "node", input, output, 1, node_config)

        self.verbose = (
            False if node_config is None else node_config.get("verbose", False)
        )

    def execute(self, state: dict) -> dict:
        """
        Executes the node's logic to parse the HTML documents content.

        Args:
            state (dict): The current state of the graph. The input keys will be used to fetch the
                            correct data from the state.

        Returns:
            dict: The updated state with the output key containing the parsed content chunks.

        Raises:
            KeyError: If the input keys are not found in the state, indicating that the
                        necessary information for parsing the content is missing.
        """

        self.logger.info(f"--- Executing {self.node_name} Node ---")
        
        # Interpret input keys based on the provided input expression
        input_keys = self.get_input_keys(state)
        # Fetching data from the state based on the input keys
        input_data = [state[key] for key in input_keys]

        documents = input_data[0]
        
        for doc in documents:
            document_md = Html2TextTransformer(ignore_links=True).transform_documents(doc["document"])
            #document_md = convert_to_md(doc["document"])
            doc["document"] = document_md[0].page_content
        
        state.update({self.output[0]: documents})
        
        return state
