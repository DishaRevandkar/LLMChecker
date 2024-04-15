from googleapiclient.discovery import build
import openai
from keywords import extract_keywords
from searchquery import generate_dynamic_search_query
from clustering import cluster_search_results, get_page_rank
from summarization import generate_summary
from factualitypredictor import predict_factuality
import textwrap

openai.api_key = ''
google_api_key = ''
google_cse_id = ''
max_page_rank = 50000


def perform_google_custom_search(query, api_key, cse_id):
    try:
        service = build('customsearch', 'v1', developerKey=api_key)

        result = service.cse().list(q=query, cx=cse_id).execute()

        filtered_results = [item for item in result.get('items', []) if
                            get_page_rank(item.get('displayLink', '')) <= max_page_rank]

        clustered_results = cluster_search_results(filtered_results)

        max_cluster_id = max(clustered_results, key=lambda x: len(clustered_results[x]))

        print(f"\nSelected Group of Search Results {max_cluster_id}:")
        for item in clustered_results[max_cluster_id]:
            title = item.get('title', '')
            snippet = item.get('snippet', '')
            display_link = item.get('displayLink', '')

            snippet_wrapped = textwrap.fill(snippet, width=100)

            print(f"Title: {title}")
            print(f"Snippet: {snippet_wrapped}")
            print(f"Display Link: {display_link}")
            print()

        return clustered_results[max_cluster_id]

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

    keywords = extract_keywords(user_prompt, ai_answer)

    search_query = generate_dynamic_search_query(keywords)

    print("\nGenerated Answer:", ai_answer)
    print("Extracted Keywords:", keywords)
    print(f"Generated Search Query: {search_query}")

    search_results = perform_google_custom_search(search_query, google_api_key, google_cse_id)

    summary_text = generate_summary(search_results)

    print("\nGenerated Summary:")
    print(textwrap.fill(summary_text, width=75))

    prediction = predict_factuality(summary_text, ai_answer)
    print("\nFactuality Prediction:", prediction)
