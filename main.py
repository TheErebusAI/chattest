import argparse
import sys
from config_loader import ConfigLoader
from inference_runner import InferenceRunner
from evaluation_component import EvaluationComponent
from reporting_module import ReportingModule

def main():
    parser = argparse.ArgumentParser(description="chattest framework")
    parser.add_argument('--prompt_key', type=str, required=True, help='Key of the prompt to test')
    parser.add_argument('--verbosity', type=int, default=1, help='Verbosity level of the output')
    parser.add_argument('--conversation_history', type=str, help='Path to JSON file containing conversation history')
    args = parser.parse_args()

    try:
        # Load configurations
        config_loader = ConfigLoader()
        prompts = config_loader.load_prompts()
        models = config_loader.load_models()

        # Filter prompts based on the provided prompt key
        selected_prompts = [prompt for prompt in prompts if prompt.key == args.prompt_key]
        if not selected_prompts:
            print(f"No prompt found with key: {args.prompt_key}")
            sys.exit(1)

        # Load conversation history if provided
        if args.conversation_history:
            with open(args.conversation_history, 'r') as f:
                conversation_history = json.load(f)
            for prompt in selected_prompts:
                prompt.conversationHistory = conversation_history

        # Run inference
        inference_runner = InferenceRunner(selected_prompts, models)
        inference_runner.run_single_prompt_inference(args.prompt_key)
        outputs = inference_runner.get_outputs()

        # Evaluate outputs
        evaluation_component = EvaluationComponent(outputs, selected_prompts)
        evaluation_component.evaluate()
        evaluation_component.aggregate_results()
        results = evaluation_component.get_results()

        # Report results
        reporting_module = ReportingModule(results)
        reporting_module.output_results()
        reporting_module.log_results()

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
