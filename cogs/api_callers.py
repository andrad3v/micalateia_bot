from .utils.apis.api_mangadex import get_last_chapters, search_manga_by_title


def call_api(api_name, endpoint, params=None):
    """
    Calls the specified API with the given endpoint and parameters.
    
    :param api_name: The name of the API to call (e.g., 'mangadex', 'mangafox', 'mangaplus').
    :param endpoint: The endpoint to call (e.g., '/manga', '/chapter').
    :param params: Optional parameters to include in the API call.
    :return: The JSON response from the API call.
    """

    match api_name:
        case "mangadex":
            match endpoint:
                case "search":
                    return search_manga_by_title(params[0])
                case "list_chapters":
                    return get_last_chapters(params[0], params[1])
                case _:
                    raise ValueError(f"Endpoint '{endpoint}' not supported.")

        case _:
            raise ValueError(f"API '{api_name}' not supported.")