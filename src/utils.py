class Utility:

    @classmethod
    def clean_unexpected_message(self, message: str):
        if message.startswith("```sql") and message.endswith("```"):
            return message[len("```sql"):-len("```")].strip()
        elif message.startswith("```") and message.endswith("```"):
            return message[len("```"):-len("```")]
        else:
            return message

    @classmethod
    def load_text_file(self, path):
        with open(path, "r") as f:
            return f.read()