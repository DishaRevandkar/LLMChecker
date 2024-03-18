from googleapiclient.discovery import build
import openai
from keywords import extract_keywords
from searchquery import generate_dynamic_search_query
from searchresultranker import rank_search_results

openai.api_key = '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'
google_api_key = 'AIzaSyCKJunNxqmxF-NUHXWBOdXkHqffNHF-S8s'
google_cse_id = 'f73f963bbb8984659'



def perform_google_custom_search(query, api_key, cse_id):
    try:
        # Creates a service object for interacting with the Google Custom Search JSON API
        service = build('customsearch', 'v1', developerKey=api_key)

        result = service.cse().list(q=query, cx=cse_id).execute()

        return result  # Return the entire result object for further processing

    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    user_prompt = input("Enter your prompt: ")

    ai_answer = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_prompt}
        ])["choices"][0]["message"]["content"]

    keywords = extract_keywords(user_prompt, ai_answer)
    search_query = generate_dynamic_search_query(keywords)

    print("\nGenerated Answer:", ai_answer)
    print("\nExtracted Keywords:", keywords)
    print(f"\nGenerated Search Query: {search_query}")

    search_results = perform_google_custom_search(search_query, google_api_key, google_cse_id)

    if search_results:
        ranked_results = rank_search_results(search_results, user_prompt, ai_answer)

        print("\nRanked Search Results:")
        for idx, (item, relevance_score, page_rank, combined_score) in enumerate(ranked_results, start=1):
            title = item.get('title', '')
            snippet = item.get('snippet', '')
            display_link = item.get('link', '')

            print(f"\nResult {idx}:")
            print(f"Title: {title}")
            print(f"Snippet: {snippet}")
            print(f"Display Link: {display_link}")
            print(f"Relevance Score: {relevance_score}")
            print(f"Page Rank: {page_rank}")
            print(f"Combined Score: {combined_score}")

            print("\n")

    else:
        print("No search results found.")


if __name__ == "__main__":
    main()
