from jsonrpcclient import request, Response
from jsonrpcclient.clients.http_client import HTTPClient
import os, json, jsonschema


#go into the top right corner, hit your user name, hit edit profile, then go to API and extract your API key and insert it here.
api_key = 'your api key'

class NonValidatingClient(HTTPClient):
   # A custom HTTPClient that grabs and parses the response string before it gets validated
   def __init__(self, *args, **kwargs) -> None:
       super().__init__(*args, **kwargs)

   def send_message(
       self, request: str, response_expected: bool, **kwargs
   ) -> Response:
       """
       Transport the message to the server and return the response.
       Args:
           request: The JSON-RPC request string.
           response_expected: Whether the request expects a response.
       Returns:
           A Response object.
       """
       response = self.session.post(self.endpoint, data=request.encode(), **kwargs)
       with open('List_of_snatched.txt', 'w') as List_of_snatched:
           resJSON = json.JSONDecoder().decode(response.text)
           resJSON["jsonrpc"] = 2.0
           List_of_snatched.write(json.JSONEncoder().encode(resJSON["result"]))
       return Response(json.JSONEncoder().encode(resJSON)) # @TODO: Actually fix this response to make it valid

   def request(
       self,
       method_name: str,
       *args,
       trim_log_values: bool = False,
       validate_against_schema: bool = True,
       id_generator = None,
       **kwargs
   ) -> Response:
       """
       Send a request by passing the method and arguments.
       >>> client.request("cat", name="Yoko")
       <Response[1]
       Args:
           method_name: The remote procedure's method name.
           args: Positional arguments passed to the remote procedure.
           kwargs: Keyword arguments passed to the remote procedure.
           trim_log_values: Abbreviate the log entries of requests and responses.
           validate_against_schema: Validate response against the JSON-RPC schema.
           id_generator: Iterable of values to use as the "id" part of the request.
       """
       try:
           super().request(method_name,
                           *args,
                           trim_log_values,
                           validate_against_schema,
                           id_generator,
                           **kwargs)
       except jsonschema.exceptions.ValidationError:
           # Just discard this error as we already handle it in send_message
           pass
       return None


client = NonValidatingClient("https://api.broadcasthe.net/")
client.request("getUserSnatchlist", key=api_key, results=4000)
