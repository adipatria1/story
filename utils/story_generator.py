from typing import Optional
from .config import init_gemini, AVAILABLE_MODELS, EXPERTISE_LEVELS, TONE_STYLES
from .prompt_builder import build_story_prompt
from .summary_generator import generate_summary
import time

class StoryGenerator:
    def __init__(self, model_name: str = 'gemini-2.0-flash-exp', api_key: Optional[str] = None):
        if model_name not in AVAILABLE_MODELS:
            raise ValueError(f"Model {model_name} not supported")
        self.model = init_gemini(model_name, api_key)
        self.model_name = model_name
        self.api_key = api_key

    def validate_inputs(self, expertise: str, tone: str):
        if expertise not in EXPERTISE_LEVELS:
            raise ValueError(f"Expertise level '{expertise}' not supported")
        if tone not in TONE_STYLES:
            raise ValueError(f"Tone style '{tone}' not supported")

    def generate_story_chunk(
        self,
        topic: str,
        expertise: str,
        tone: str,
        context: Optional[str] = None,
        part_number: int = 1,
        total_parts: int = 1,
        previous_parts: list[str] = None
    ) -> str:
        try:
            self.validate_inputs(expertise, tone)
            prompt = build_story_prompt(
                topic, expertise, tone, context,
                part_number, total_parts, previous_parts
            )
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating story part {part_number}: {str(e)}"

    def generate_complete_story(
        self,
        topic: str,
        expertise: str,
        tone: str,
        context: Optional[str] = None,
        total_parts: int = 3
    ) -> str:
        story_parts = []
        summaries = []

        for part in range(1, total_parts + 1):
            chunk = self.generate_story_chunk(
                topic, expertise, tone, context,
                part, total_parts, summaries
            )
            story_parts.append(chunk)

            if part < total_parts:
                summary = generate_summary(chunk, self.model)
                summaries.append(summary)
                time.sleep(2)  # Add small delay between requests

        return "\n\n".join(story_parts)