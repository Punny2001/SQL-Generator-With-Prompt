class Utility:

    @classmethod
    def clean_unexpected_message(self, message: str):
        if message.startswith("```sql") and message.endswith("```"):
            return message[len("```sql"):-len("```")].strip()
        elif message.startswith("```") and message.endswith("```"):
            return message[len("```"):-len("```")]
        elif message.startswith("SQL Query: "):
            return message[len("SQL Query: "):]
        else:
            return message

    @classmethod
    def load_text_file(self, path):
        with open(path, "r") as f:
            return f.read()
        
    @classmethod
    def load_json_file(self, path):
        import json

        with open(path, "r") as f:
            return json.load(f)