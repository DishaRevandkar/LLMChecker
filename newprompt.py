def generate_summary_prompt(original_prompt, filtered_results):
    if filtered_results:
        all_snippets = '\n'.join([item.get('snippet', '') for item, _, _, _ in filtered_results])

        summary_paragraph = f"Original Prompt: {original_prompt}\n\n"
        summary_paragraph += "Summary of Search Results:\n\n"
        summary_paragraph += f"{all_snippets}\n"

        return summary_paragraph
    else:
        return "No filtered search results found."
