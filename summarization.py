import openai

openai.api_key = ''


def generate_summary_prompt(search_results):
    summary_prompt = "Generate a summary of the search results. Be elaborate:\n"
    for item in search_results:
        summary_prompt += f"- {item.get('title', '')}\n{item.get('snippet', '')}\n"
    return summary_prompt


def generate_summary(search_results):
    summary_prompt = generate_summary_prompt(search_results)
    summary_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": summary_prompt}
        ],
        temperature=0.7,
        max_tokens=150
    )
    summary_text = summary_response.choices[0].message.content.strip()
    return summary_text
