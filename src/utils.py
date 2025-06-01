class Utility:

    @classmethod
    def clean_unexpected_message(message: str):
        if message.startswith("```sql") and message.endswith("```"):
            return message[len("```sql"):-len("```")].strip()
        elif message.startswith("```") and message.endswith("```"):
            return message[len("```"):-len("```")]
        else:
            return message
