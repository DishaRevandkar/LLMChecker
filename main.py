from googleapiclient.discovery import build
import openai
from keywords import extract_keywords
from searchquery import generate_dynamic_search_query
from searchqueryoptimizer import extract_sentences_from_snippet

openai.api_key = 'useyourkey'
google_api_key = 'useyourkey'
google_cse_id = 'useyourkey'


def perform_google_custom_search(query, api_key, cse_id):
    try:
        # Creates a service object for interacting with the Google Custom Search JSON API
        service = build('customsearch', 'v1', developerKey=api_key)

        result = service.cse().list(q=query, cx=cse_id).execute()

        # Extract and print search results
        for item in result.get('items', []):
            title = item.get('title', '')
            snippet = item.get('snippet', '')
            display_link = item.get('displayLink', '')

            print(f"Title: {title}")
            print(f"Snippet: {snippet}")
            print(f"Display Link: {display_link}")

            sentences = extract_sentences_from_snippet(snippet)
            print("Meaningful Sentences:")
            for sentence in sentences:
                print(f"- {sentence}")

            print("\n")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    user_prompt = input("Enter your prompt: ")

    ai_answer = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_prompt}
        ])["choices"][0]["message"]["content"]

    # Extracts important keywords
    keywords = extract_keywords(user_prompt, ai_answer)

    # Generates a dynamic search query
    search_query = generate_dynamic_search_query(keywords)

    print("\nGenerated Answer:", ai_answer)
    print("Extracted Keywords:", keywords)
    print(f"Generated Search Query: {search_query}")
    perform_google_custom_search(search_query, google_api_key, google_cse_id)
