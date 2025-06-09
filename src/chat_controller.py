import openai
import logging
import json
import os


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

CURRENT_PATH = os.getcwd()
SYSTEM_PROMPT_PATH = f"{CURRENT_PATH}/prompts/system_message.txt"
FEW_SHOT_EXAMPLES_PATH = f"{CURRENT_PATH}/prompts/examples/few_shot_examples.json"
DATA_SCHEMA_PATH = f"{CURRENT_PATH}/data/schema/database_schema.sql"
TABLE_DESCRIPTIONS_PATH = f"{CURRENT_PATH}/data/schema/table_descriptions.json"

class ChatController:

    def __init__(self, config):
        openai.api_key = config.api_key
        self.model_name = config.model_name
        self.temperature = config.temperature
        self.max_tokens = config.max_tokens
    
        self.prepare_messages = self.prepare_messages()

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
        
        
    def prepare_messages(self):

        with open(SYSTEM_PROMPT_PATH, "r") as f:
            system_message = f.read()

            with open(DATA_SCHEMA_PATH, "r") as schema:
                table_schema = schema.read()
            
            with open(TABLE_DESCRIPTIONS_PATH, "r") as desc:
                table_description_json = json.load(desc)
                table_description_text = """
                    Table: {table}
                    Description: {description}
                """
                column_description_text = """
                    Column Name: {column}
                    Description: {description}
                    Possible Value: {example_data}
                """
                for table_key, table_value in table_description_json.items():
                    table_description_text = table_description_text.format(table=table_key, description=table_value['description'])
                    
                    column_description_text = "\n".join(
                        column_description_text.format(
                            column=col_key, 
                            description=col_value['description'], 
                            example_data=", ".join(str(data) for data in col_value['example_data'])
                            ) 
                        for col_key, col_value in table_value['columns_name'].items()
                        )

            system_message = system_message.format(table_schema=table_schema, table_description=table_description_text, column_description=column_description_text)

        with open(FEW_SHOT_EXAMPLES_PATH, "r") as f:
            few_shot_examples = json.load(f)
            

        messages: list[dict] = [{"role": "system", "content": system_message}]

        for example in few_shot_examples:
            messages.append({
                "role": "user",
                "content": example['question']
            })

            messages.append({
                "role": "assistant",
                "content": example['query']
            })

        return messages
