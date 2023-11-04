import openai

class Utils:
    def __init__(self) -> None:
        self.base_context = "context/default.txt"
        self.base_api_key = "YOUR APIKEY"

    def get_context(self) -> str:
        with open(self.base_context, "r") as f:
            return f.read()

    def get_separated_lines(self) -> list:
        return self.get_context().split("\n")


class Context:
    def __init__(self) -> None:
        pass

    def chat(self, user_prompt: str) -> str:
        openai.api_key = Utils().base_api_key

        prompt = f"{Utils().get_context()}\n> {user_prompt}\nAI:"

        completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
        )

        data = completion.choices[0].message
        return data['content']