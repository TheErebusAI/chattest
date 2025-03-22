import os
from typing import List, Dict, Any

class ReportingModule:
    def __init__(self, results: List[Dict[str, Any]], log_dir: str = 'outputs/logs/'):
        self.results = results
        self.log_dir = log_dir

    def output_results(self):
        for result in self.results:
            if 'success_rate' in result:
                print(f"Prompt: {result['prompt_key']}, Test: {result['test']}, Success Rate: {result['success_rate']:.2f}, Result: {result['result']}")
            else:
                print(f"Prompt: {result['prompt_key']}, Model: {result['model_key']}, Run: {result['run_number']}, Test: {result['test']}, Result: {result['result']}")

    def log_results(self):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        log_file = os.path.join(self.log_dir, 'test_results.log')
        with open(log_file, 'w') as f:
            for result in self.results:
                if 'success_rate' in result:
                    f.write(f"Prompt: {result['prompt_key']}, Test: {result['test']}, Success Rate: {result['success_rate']:.2f}, Result: {result['result']}\n")
                else:
                    f.write(f"Prompt: {result['prompt_key']}, Model: {result['model_key']}, Run: {result['run_number']}, Test: {result['test']}, Result: {result['result']}\n")
