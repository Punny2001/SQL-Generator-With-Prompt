import openai
import logging
import json
import os
from src.utils import Utility


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

CURRENT_PATH = os.getcwd()
SYSTEM_PROMPT_PATH = f"{CURRENT_PATH}/prompts/system_message.txt"
BASE_PROMPT_PATH = f"{CURRENT_PATH}/prompts/base_prompt.txt"
FEW_SHOT_TEMPLATE_PATH= f"{CURRENT_PATH}/prompts/few_shot_template.txt"
FEW_SHOT_EXAMPLES_PATH = f"{CURRENT_PATH}/prompts/examples/few_shot_examples.json"
DATABASE_SCHEMA_PATH = f"{CURRENT_PATH}/data/schema/database_schema.sql"
TABLE_DESCRIPTIONS_PATH = f"{CURRENT_PATH}/data/schema/table_descriptions.json"

class ChatController:

    def __init__(self, config):
        openai.api_key = config.api_key
        self.model_name = config.model_name
        self.temperature = config.temperature
        self.max_tokens = config.max_tokens

    def generate_response(self, messages: list[dict]):
        if not openai.api_key:
            error = "OpenAI API doesn't existed, please provide an API key."
            logger.error(error)
            return error
        
        try:
            response = openai.chat.completions.create(
                messages=messages,
                model=self.model_name,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )

            return response

        except Exception as e:
            error = f"An unexpected error while calling an API call: {e}"
            logger.exception(error)
            return error
        
    def retrieve_sql_statement(self, response):
        if response:
            return response.choices[0].message.content
        else:
            return None
        
        
    def prepare_messages(self, database_type):

        system_message = Utility.load_text_file(SYSTEM_PROMPT_PATH)
        database_schema = Utility.load_text_file(DATABASE_SCHEMA_PATH)
        table_descriptions = Utility.load_json_file(TABLE_DESCRIPTIONS_PATH)
        base_prompt = Utility.load_text_file(BASE_PROMPT_PATH)
        few_shot_template = Utility.load_text_file(FEW_SHOT_TEMPLATE_PATH)
        few_shot_examples = Utility.load_json_file(FEW_SHOT_EXAMPLES_PATH)

        messages = [
            {"role": "system", "content": system_message.format(database_type=database_type)},
            {
                "role": "user", 
                "content": f"{base_prompt.format(database_type=database_type)}"
                f"Database Schema:\n```sql\n{database_schema}\n```\n\n"
                f"Table Descriptions:\n```json\n{json.dumps(table_descriptions, indent=2)}\n```\n\n"
                f"Few-shot examples:\n"
            }
        ]

        print(messages)

        for example in few_shot_examples:
            messages.append({
                "role": "user",
                "content": few_shot_template.format(question=example['question'], query=example['query'])
            })

        return messages
