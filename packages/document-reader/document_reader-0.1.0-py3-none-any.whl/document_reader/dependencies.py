from langchain_openai import AzureChatOpenAI

import os



OPENAI_API_MODEL = os.getenv("OPENAI_API_MODEL")
OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION")
OPENAI_API_DEPLOYMENT_GPT4_TURBO_VISION= os.getenv("OPENAI_API_DEPLOYMENT_GPT4_TURBO_VISION")
OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")
AZURE_ENDPOINT= os.getenv("AZURE_ENDPOINT")


llm_gpt4_vision = AzureChatOpenAI(
    model=OPENAI_API_MODEL,
    deployment_name=OPENAI_API_DEPLOYMENT_GPT4_TURBO_VISION,
    openai_api_version=OPENAI_API_VERSION,
    azure_endpoint=AZURE_ENDPOINT,
    openai_api_key=OPENAI_API_KEY,
    temperature=0.0,
    max_tokens=256,  # output tokens
    model_kwargs={
        "extra_body": {
            "enhancements": {
                "ocr": {"enabled": True},  # recognize text in images
                "grounding": {"enabled": True},  # highlight important parts
            }
        }
    },
    
)