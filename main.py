from config.chat_config import ChatConfig
from config.database_config import DatabaseConfig
from src.chat_controller import ChatController
from src.db_controller import DatabaseController
from dotenv import load_dotenv

load_dotenv(override=True)

chat_config = ChatConfig()
database_config = DatabaseConfig()
chat_controller = ChatController(chat_config)
database_controller = DatabaseController(database_config)

prepare_messages: list[dict] = chat_controller.prepare_messages(database_type='postgresql')

input_prompt = str(input("Insert your message: "))

prepare_messages.append({
    "role": "user",
    "content": input_prompt
})

response = chat_controller.generate_response(prepare_messages)
query = chat_controller.retrieve_sql_statement(response)
data = database_controller.execute_query(query, include_cols=True)


print(f"Executable Query: {query}")
# print(f"Fetched Data: {data}")
# print(type(data))
# print(data)
