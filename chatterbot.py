import json
from difflib import get_close_matches
from api import super_chatter_bot
from colorama import Fore, Style, init

init(autoreset=True)


def load_knowledge_base(file_path: str) -> dict:
    """Load the knowledge base from a JSON file."""
    try:
        with open(file_path, 'r') as file:
            data: dict = json.load(file)

        return data
    except FileNotFoundError:
        print(f"Error: Knowledge base file '{file_path}' not found.")
        return {}
    
def save_knowledge_base(file_path: str, data: dict) -> None:
    """Save the knowledge base to a JSON file."""
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: list) -> str | None:
    """Find the best matching question from the knowledge base."""
    matches = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else ""

def get_answer(user_question: str, knowledge_base: dict) -> str | None:
    for question in knowledge_base["questions"]:
        if question["question"] == user_question:
            return question["answer"]
        
def chatterbot():
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')
    while True:
        user_input: str = input(f"{Fore.CYAN}You: {Style.RESET_ALL}").lower()

        if user_input.lower() == 'quit':
            print(f"{Fore.YELLOW}Chatterbot: Goodbye!{Style.RESET_ALL}")
            break
        best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer: str | None = get_answer(best_match, knowledge_base)
            print(f"{Fore.GREEN}Chatterbot: {answer}{Style.RESET_ALL}")

        else:
            print(f"{Fore.MAGENTA}Chatterbot: I don't have that in my knowledge base. Let me check with my AI brain...{Style.RESET_ALL}")
            ai_response: str = Super_chatter_bot_response(user_input)
            print(f"{Fore.GREEN}Chatterbot: {ai_response}{Style.RESET_ALL}")

            save_to_kb: str = input(f"\n{Fore.YELLOW}Would you like me to remember this for next time? (yes/no): {Style.RESET_ALL}")
            if save_to_kb.lower() == "yes":
                knowledge_base["questions"].append({
                    "question": user_input,
                    "answer": ai_response
                })
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print(f"{Fore.BLUE}Chatterbot: Got it! I've added this to my knowledge base.{Style.RESET_ALL}") 
def Super_chatter_bot_response(prompt: str) -> str:
    system_prompt = f"""You are a friendly chatbot cooking assistant. Provide one recipe using these ingredients. Keep your responses concise, helpful, and conversational.
Answer in 1-5 sentences maximum. Be direct and to the point.

User question: {prompt}"""
    response: str = super_chatter_bot(system_prompt)
    return response
if __name__ == "__main__":
    chatterbot()