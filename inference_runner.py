import requests
from typing import List, Dict, Any
from config_loader import PromptConfig, ModelConfig, ConfigLoader

class InferenceRunner:
    def __init__(self, prompts: List[PromptConfig], models: List[ModelConfig]):
        self.prompts = prompts
        self.models = models
        self.outputs = []

    def run_inference(self):
        for prompt in self.prompts:
            for model_name in prompt.models:
                model = next((m for m in self.models if m.key == model_name), None)
                if model:
                    for run in range(prompt.runVolume):
                        output = self.send_request(model, prompt.prompt, prompt.conversationHistory)
                        self.outputs.append({
                            "prompt_key": prompt.key,
                            "model_key": model.key,
                            "run_number": run + 1,
                            "output": output
                        })

    def run_single_prompt_inference(self, prompt_key: str):
        prompt = next((p for p in self.prompts if p.key == prompt_key), None)
        if prompt:
            for model_name in prompt.models:
                model = next((m for m in self.models if m.key == model_name), None)
                if model:
                    output = self.send_request(model, prompt.prompt, prompt.conversationHistory)
                    self.outputs.append({
                        "prompt_key": prompt.key,
                        "model_key": model.key,
                        "run_number": 1,
                        "output": output
                    })

    def send_request(self, model: ModelConfig, prompt_text: str, conversation_history: List[Dict[str, str]] = None) -> str:
        headers = {}
        if model.apiKey and model.apiKeyHeader:
            headers[model.apiKeyHeader] = model.apiKey
        payload = {"prompt": prompt_text}
        if conversation_history:
            payload["conversation_history"] = conversation_history
        response = requests.post(model.url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json().get("output", "")
        else:
            return f"Error: {response.status_code}"

    def get_outputs(self) -> List[Dict[str, Any]]:
        return self.outputs
