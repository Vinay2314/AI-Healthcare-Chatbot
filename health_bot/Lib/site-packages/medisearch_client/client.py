"""MediSearch API client code."""

from typing import Generator, Union

import json
import websocket


class MediSearchClient:
  """Sample client for the MediSearch API."""

  def __init__(self, api_key: str):
    self.api_key = api_key
    self.url = "wss://public.backend.medisearch.io:443/ws/medichat/api"
    self.interrupted = False

  def send_user_message(
      self,
      conversation: list[str],
      conversation_id: str,
      should_stream_response: bool = False,
      language: str = "English"
  ) -> Union[Generator[dict[str, str], None, None], list[dict[str, str]]]:
    """Send a user message to the MediSearch API.

    Note that the conversation must be a list of strings, where the user and the 
    chatbot messages alternate. E.g., [user_message_1, chatbot_message_1,
    user_message_2, ...]. The last message in the conversation must be a 
    user message. 

    Args:
        conversation: The conversation so far between the user and MediSearch.
        conversation_id: The unique id of the conversation.
        should_stream_response: Whether to stream the result the in chunks or
          not. If False, the entire llm_response together with the articles will
          be returned. Otherwise, we will return a generator of responses.
        language: Expected language of the reponse. Defaults to "English".
          Must be one of "English", "French", "Spanish", "German", "Hindi",
          "Chinese", "Japanese", "Slovak", "Arabic".

    Returns:
        A generator of responses from the MediSearch API. The responses are
        dictionaries containing MediSearch events and their data. The generator
        will yield responses until the conversation is over. The last response
        will be either an "articles" event or an "error" event.
    """

    if not conversation:
      raise ValueError("Conversation cannot be empty.")

    payload = {
        "event": "user_message",
        "conversation": conversation,
        "key": self.api_key,
        "id": conversation_id,
        "settings": {
            "language": language
        }
    }
    socket = websocket.create_connection(self.url)
    self._send_payload(payload, socket)
    response_iter = self._response_iterator(socket)
    if should_stream_response:
      return response_iter

    responses = list(response_iter)
    socket.close()
    # Filter all llm_response events except for the last one.
    return self._filter_llm_responses(responses)

  def _reconnect(self,
                 socket: websocket.WebSocket,
                 attempts: int = 4) -> websocket.WebSocket:
    """Reconnect to the MediSearch API.

    Args:
        socket: The websocket connection to the MediSearch API.
        attempts: Number of attempts to reconnect. Defaults to 4.
    """
    for _ in range(attempts):
      try:
        socket = websocket.create_connection(self.url)
        return socket
      except Exception as _:  # pylint: disable=broad-except
        pass
    raise RuntimeError(
        "Failed to reconnect to the WebSocket server after multiple attempts.")

  def _filter_llm_responses(
      self, responses: list[dict[str, str]]) -> list[dict[str, str]]:
    """Remove all but the last llm_response event from the responses."""
    seen_llm_response = False
    filtered_responses = []

    for resp in reversed(responses):
      if resp["event"] == "llm_response" and not seen_llm_response:
        seen_llm_response = True
        filtered_responses.append(resp)
      elif resp["event"] != "llm_response":
        filtered_responses.append(resp)

    return list(reversed(filtered_responses))

  def _send_payload(self, payload: dict[str, str],
                    socket: websocket.WebSocket) -> None:
    if not socket.connected:
      socket = self._reconnect(socket=socket)
    try:
      socket.send(json.dumps(payload))
    except websocket.WebSocketConnectionClosedException as _:
      raise websocket.WebSocketConnectionClosedException(
          ("WebSocket connection lost. Please reinitialize the client or check"
           " the server status."))

  def _response_iterator(self, socket: websocket.WebSocket):
    while True:
      if not socket.connected:
        self._reconnect(socket=socket)
      if self.interrupted:
        break
      data = json.loads(socket.recv())
      yield data
      if "event" in data and (data["event"] == "articles" or
                              data["event"] == "error"):
        break
    self.interrupted = False
    socket.close()
