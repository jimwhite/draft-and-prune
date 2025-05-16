#!/usr/bin/env python3
import argparse

from config import ReasonerConfig
from reasoners import TwoStepReasoner
from data_loaders import AR_LSAT_DatasetLoader
from answer_extractors import AR_LSAT_AnswerExtractor

def main():
    """Main entry point for the script"""
    parser = argparse.ArgumentParser(
        description="Partitioned-Neural-Symbolic-Reasoning",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Required arguments
    parser.add_argument("--api_key", help="Google API key for accessing Gemini models")
    parser.add_argument("--test_file", help="Path to the test file")
    
    # Optional arguments
    parser.add_argument("--limit", type=int, metavar="N",
                        help="Limit the number of samples to process")
    parser.add_argument("--model", default="gemini-1.5-pro", 
                        help="Specify the model name to use")
    parser.add_argument("--dataset", default="AR-LSAT",
                        choices=["AR-LSAT"], 
                        help="Specify the dataset to use")
    parser.add_argument("--temperature", type=float, default=0.0,
                        help="Temperature for model generation")
    parser.add_argument("--max-repairs", type=int, default=3,
                        help="Maximum number of repairs for API calls")
    parser.add_argument("--test-delay", type=int, default=5,
                        help="Delay (seconds) between test cases")
    parser.add_argument("--reasoning-method", default="two-step",
                        choices=["CoT", "one-step", "two-step", "three-step"],
                        help="Reasoning method to use")
    parser.add_argument("--shots", type=str, default='zero',
                        choices=["zero", "one", "two", "three"],
                        help="Number of shots to use")
    
    args = parser.parse_args()

    # Create configuration with command line arguments
    config = ReasonerConfig(
        reasoning_method=args.reasoning_method,
        api_key=args.api_key,
        dataset=args.dataset,
        model_name=args.model,
        data_path=args.test_file,
        temperature=args.temperature,
        max_repairs=args.max_repairs,
        inter_test_case_delay=args.test_delay,
        limit=args.limit,
        shots=args.shots,
        result_filename_template=f"{args.dataset}_{args.reasoning_method}_results_{args.model}_{args.shots}_shot_COT.json"
    )

    # Create dataset loader based on format
    if args.dataset.lower() == "ar-lsat":
        # reasoner = AR_LSAT_Reasoner(config)
        data_loader = AR_LSAT_DatasetLoader()
        answer_extractor = AR_LSAT_AnswerExtractor()
    else:
        raise ValueError(f"Unsupported dataset: {args.dataset}")
    
    if config.reasoning_method == "one-step":
        # reasoner = DirectReasoner(config, data_loader, answer_extractor)
        raise ValueError(f"Unsupported reasoning method: {config.reasoning_method}")
    elif config.reasoning_method == "two-step":
        reasoner = TwoStepReasoner(config, data_loader, answer_extractor)
    elif config.reasoning_method == "three-step":
        # reasoner = ThreeStepReasoner(config, data_loader, answer_extractor)
        raise ValueError(f"Unsupported reasoning method: {config.reasoning_method}")
    else:
        raise ValueError(f"Unsupported reasoning method: {config.reasoning_method}") 


    limit_msg = f" with limit {args.limit}" if args.limit else ""
    print(f"Running all tests from {args.dataset}{limit_msg} using {args.reasoning_method} reasoning")
    reasoner.run_all_tests()


if __name__ == "__main__":
    main() 