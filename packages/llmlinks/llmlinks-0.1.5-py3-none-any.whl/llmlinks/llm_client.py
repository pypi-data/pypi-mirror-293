# %%
from typing import Any
from .llm.openai_model import OpenAILLM
from .llm.google_model import GoogleLLM
from .llm.anthropic_model import AnthropicLLM

class LLMClient:
    
    def __init__(
            self,
            llm_name,
            ):
        # OpenAI
        if llm_name == 'gpt-4o-2024-08-06':
            self.llm = OpenAILLM(model = llm_name)
        elif llm_name == 'gpt-4o-2024-05-13':
            self.llm = OpenAILLM(model = llm_name)
        elif llm_name == 'gpt-4o-mini-2024-07-18':
            self.llm = OpenAILLM(model = llm_name)
        elif llm_name == 'gpt-4-turbo-2024-04-09':
            self.llm = OpenAILLM(model = llm_name)
        elif llm_name == 'gpt-4-0125-preview':
            self.llm = OpenAILLM(model = llm_name)
        # Google
        elif llm_name == 'gemini-1.0-pro':
            self.llm = GoogleLLM(model = llm_name)
        elif llm_name == 'gemini-1.5-pro':
            self.llm = GoogleLLM(model = llm_name)
        elif llm_name == 'gemini-1.5-flash':
            self.llm = GoogleLLM(model = llm_name)
        # Anthropic
        elif llm_name == 'claude-3-5-sonnet-20240620':
            self.llm = AnthropicLLM(model = llm_name)
        elif llm_name == 'claude-3-opus-20240229':
            self.llm = AnthropicLLM(model = llm_name)
        
        else:
            raise ValueError(f'Unknown LLM: {llm_name}')

    def __call__(self) -> Any:
        pass


if __name__ == "__main__":
    llm_name = 'gpt-4o-2024-08-06'
    llm = LLMClient(llm_name)
    print(llm("Hello, world!"))
