import asyncio
import json
import traceback

import typer
import websockets
from rich import print

from galadriel.config import config
from galadriel.sdk.llm import Llm
from galadriel.sdk.entities import InferenceRequest

llm = Llm()

node_app = typer.Typer(
    name="node",
    help="Galadriel tool to manage node",
    no_args_is_help=True,
)

MAX_RETRIES = 5
BACKOFF_MIN = 1  # Minimum backoff time in seconds


async def process_request(
    request: InferenceRequest,
    websocket,
    llm_base_url: str,
    debug: bool,
    send_lock: asyncio.Lock,
):
    """
    Handles a single inference request and sends the response back in chunks.
    """
    try:
        if debug:
            print(f"REQUEST {request.id} START")
        async for chunk in llm.execute(request, llm_base_url):
            if debug:
                print(f"Sending chunk: {chunk}")
            async with send_lock:
                await websocket.send(chunk.to_json())
        if debug:
            print(f"REQUEST {request.id} END")
    except Exception as e:
        if debug:
            traceback.print_exc()
        print(f"Error occurred while processing inference request: {e}")


async def connect_and_process(uri: str, headers: dict, llm_base_url: str, debug: bool):
    """
    Establishes the WebSocket connection and processes incoming requests concurrently.
    """
    send_lock = asyncio.Lock()

    async with websockets.connect(uri, extra_headers=headers) as websocket:
        print(f"Connected to {uri}")
        while True:
            try:
                message = await websocket.recv()
                data = json.loads(message)
                request = InferenceRequest.from_dict(data)

                asyncio.create_task(
                    process_request(request, websocket, llm_base_url, debug, send_lock)
                )
            except websockets.ConnectionClosed as e:
                print(f"Connection closed: {e}. Exiting loop.")
                break
            except Exception as e:
                if debug:
                    traceback.print_exc()
                print(f"Error occurred while processing message: {e}")
                break


async def retry_connection(rpc_url: str, api_key: str, llm_base_url: str, debug: bool):
    """
    Attempts to reconnect to the Galadriel server with exponential backoff.
    """
    uri = f"{rpc_url}/ws"
    headers = {"Authorization": f"Bearer {api_key}"}
    retries = 0
    backoff_time = BACKOFF_MIN

    while retries < MAX_RETRIES:
        try:
            await connect_and_process(uri, headers, llm_base_url, debug)
            retries = 0  # Reset retries on successful connection
            backoff_time = BACKOFF_MIN  # Reset backoff time
        except websockets.ConnectionClosedError as e:
            retries += 1
            print(f"WebSocket connection closed: {e}. Retrying...")
        except Exception as e:
            retries += 1
            if debug:
                traceback.print_exc()
            print(
                f"Connection failed ({retries}/{MAX_RETRIES}). Retrying in {backoff_time} seconds..."
            )

        # Exponential backoff before retrying
        await asyncio.sleep(backoff_time)
        backoff_time = min(backoff_time * 2, 60)  # Cap backoff time to 60 seconds

        if retries >= MAX_RETRIES:
            print("Max retries reached. Exiting...")
            break


@node_app.command("run", help="Run the Galadriel node")
def node_run(
    rpc_url: str = typer.Option(config.GALADRIEL_RPC_URL, help="RPC url"),
    api_key: str = typer.Option(config.GALADRIEL_API_KEY, help="API key"),
    llm_base_url: str = typer.Option(
        config.GALADRIEL_LLM_BASE_URL, help="LLM base url"
    ),
    debug: bool = typer.Option(False, help="Enable debug mode"),
):
    """
    Entry point for running the node with retry logic and connection handling.
    """
    asyncio.run(retry_connection(rpc_url, api_key, llm_base_url, debug))
