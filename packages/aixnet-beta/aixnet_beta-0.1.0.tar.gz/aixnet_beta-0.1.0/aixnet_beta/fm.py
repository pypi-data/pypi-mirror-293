# fm.py

import requests
import json
from typing import Dict, Any

class OpenAIClient:
    """
    A client class for interacting with the OpenAI API.
    """

    def __init__(self, api_key: str):
        """
        Initializes the OpenAIClient with the authorization key.

        Args:
            api_key (str): The authorization API key for OpenAI.
        """
        self.api_url = "https://pxkmb0mj4g.execute-api.us-east-1.amazonaws.com/dev/chat/completions"
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def invoke_api(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Invokes the OpenAI API with the given payload using a POST request.

        Args:
            payload (Dict[str, Any]): The JSON payload to send with the POST request.

        Returns:
            Dict[str, Any]: The JSON response from the API.
        """
        try:
            # Send the POST request to the API
            response = requests.post(self.api_url, headers=self.headers, data=json.dumps(payload))

            # Raise an exception if the request was unsuccessful
            response.raise_for_status()

            # Parse the JSON response
            return response.json()

        except requests.exceptions.RequestException as e:
            # Print any errors that occur
            print(f"An error occurred: {e}")
            return {}
