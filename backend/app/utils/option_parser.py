def extract_option_number(query: str):

    query = query.lower()

    if "option 1" in query or "first" in query:
        return 1

    elif "option 2" in query or "second" in query:
        return 2

    elif "option 3" in query or "third" in query:
        return 3

    return None
