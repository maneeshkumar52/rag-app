def format_response(response):
    # Format the response from the OpenAI model
    return response.strip()

def log_error(error_message):
    # Log error messages to a file or console
    print(f"Error: {error_message}")

def validate_query(query):
    # Validate the input query
    if not query or len(query) < 3:
        raise ValueError("Query must be at least 3 characters long.")
    return query

def extract_keywords(text):
    # Extract keywords from the given text
    # This is a placeholder for a more complex keyword extraction logic
    return text.split()[:5]  # Return first 5 words as keywords

def prepare_data_for_db(data):
    # Prepare data for storage in the database
    return {key: value for key, value in data.items() if value is not None}