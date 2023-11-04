import time
from utils import Context
from utils import Utils

def start_chat(user_message: str) -> str:
    return Context().chat(user_message)

if __name__ == "__main__":
    init_utils = Utils().get_separated_lines()


    print(init_utils[2])
    while True:
        user_input = input("🐼.... ")

        if user_input != "exit":
            print("Processando...", end='', flush=True)
            for _ in range(10):
                time.sleep(0.1)
                print(".", end='', flush=True)
            print()  # Nova linha após a animação de progresso
            print(start_chat(user_input))
        else:
            break
