def generate_summary(text: str, model) -> str:
    try:
        summary_prompt = f"""
        Provide a brief summary (maximum 400 words) of the following story segment,
        capturing key plot points, character developments, and ending to maintain continuity:

        {text}
        """
        summary = model.generate_content(summary_prompt).text
        return summary
    except Exception as e:
        return f"Summary unavailable: {str(e)}"