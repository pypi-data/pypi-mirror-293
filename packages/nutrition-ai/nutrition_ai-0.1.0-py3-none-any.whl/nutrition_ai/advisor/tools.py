import enum
from PIL import Image
import io
import base64
import requests
from nutrition_ai.advisor import types
from nutrition_ai.advisor import constants


class ToolType(str, enum.Enum):
    SEARCHINGREDIENTMATCHES = "SearchIngredientMatches"
    DETECTMEALLOGSREQUIRED = "DetectMealLogsRequired"
    VISUALFOODEXTRACTION = "VisualFoodExtraction"


def _pil_to_base64(image: Image) -> str:
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


def visual_food_extraction(
    thread_id: str, image: Image, message: str | None = None, header: dict = {}
) -> types.AdvisorResponse:
    """
    Extracts visual food information from an image and sends it to the AI advisor.

    Args:
        thread_id (str): The ID of the conversation thread.
        image (Image): The image containing the food to be analyzed.
        message (str, optional): An optional message to accompany the image. Defaults to None.
        header (dict, optional): The authorization header. Defaults to an empty dictionary.

    Returns:
        types.AdvisorResponse: The response from the AI advisor containing the extracted food information.
    """

    url = f"{constants.THREAD_URL}/{thread_id}/messages/tools/vision/{ToolType.VISUALFOODEXTRACTION.value}"
    image_str = _pil_to_base64(image)

    resp = requests.post(
        url,
        headers=header,
        json={"image": constants.BASE64_IMAGE + image_str, "message": message},
    )
    r = types.AdvisorResponse.model_validate(resp.json())
    return r


def search_ingredient_matches(
    thread_id: str, message_id: str, header: dict = {}
) -> types.AdvisorResponse:
    """
    Searches for ingredient matches using the AI advisor.

    Args:
        thread_id (str): The ID of the conversation thread.
        message_id (str): The ID of the message to search for ingredient matches.
        header (dict, optional): The authorization header. Defaults to an empty dictionary.

    Returns:
        types.AdvisorResponse: The response from the AI advisor containing the ingredient matches.
    """

    url = f"{constants.THREAD_URL}/{thread_id}/messages/tools/target/{ToolType.SEARCHINGREDIENTMATCHES.value}"
    resp = requests.post(url, headers=header, json={"messageId": message_id})
    r = types.AdvisorResponse.model_validate(resp.json())
    return r


def detect_meal_logs_required(
    thread_id: str,
    message_id: str,
    tool_call_id: str,
    run_id: str,
    data: str,
    header: dict = {},
) -> types.AdvisorResponse:
    """
    Detects the required meal logs for a given conversation thread.

    Args:
        thread_id (str): The ID of the conversation thread.
        message_id (str): The ID of the message to detect meal logs for.
        tool_call_id (str): The ID of the tool call.
        run_id (str): The ID of the run.
        data (str): The data to be sent in the request.
        header (dict, optional): The authorization header. Defaults to an empty dictionary.

    Returns:
        types.AdvisorResponse: The response from the AI advisor containing the detected meal logs.
    """

    url = f"{constants.THREAD_URL}/{thread_id}/messages/{message_id}/respond"
    resp = requests.post(
        url,
        headers=header,
        json={"data": data, "toolCallId": tool_call_id, "runId": run_id},
    )
    r = types.AdvisorResponse.model_validate(resp.json())
    return r


def list_tools(header: dict = {}) -> types.ToolInfoList:
    """
    Retrieves a list of available tools from the AI advisor.

    Args:
        header (dict, optional): The authorization header. Defaults to an empty dictionary.

    Returns:
        types.ToolInfoList: The response containing the list of available tools.
    """
    url = f"{constants.TOOLS_URL}"
    resp = requests.get(url, headers=header)
    r = types.ToolInfoList(tools=[types.ToolInfo(**item) for item in resp])
    return r
