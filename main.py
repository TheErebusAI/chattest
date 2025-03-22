import argparse
import sys
from config_loader import ConfigLoader, load_model_config
from inference_runner import InferenceRunner
from evaluation_component import EvaluationComponent
from reporting_module import ReportingModule

def main():
    parser = argparse.ArgumentParser(description="chattest framework")
    parser.add_argument('--prompt_key', type=str, required=True, help='Key of the prompt to test')
    parser.add_argument('--verbosity', type=int, default=1, help='Verbosity level of the output')
    args = parser.parse_args()

    try:
        # Load configurations
        config_loader = ConfigLoader()
        prompts = config_loader.load_prompts()
        models = load_model_config()

        # Filter prompts based on the provided prompt key
        selected_prompts = [prompt for prompt in prompts if prompt.key == args.prompt_key]
        if not selected_prompts:
            print(f"No prompt found with key: {args.prompt_key}")
            sys.exit(1)

        # Run inference
        inference_runner = InferenceRunner(selected_prompts, models)
        inference_runner.run_inference()
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
