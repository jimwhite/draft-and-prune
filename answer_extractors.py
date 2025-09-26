#!/usr/bin/env python3
import re
from typing import Tuple, Optional, List, Dict, Union
from abc import ABC, abstractmethod
from collections import Counter

class AnswerExtractor(ABC):
    """Base class for answer extractors"""
    
    @abstractmethod
    def extract_answer(self, response_text: str, label: str) -> Tuple[bool, str]:
        """Extract the answer from the response text"""
        pass
    

class AR_LSAT_AnswerExtractor(AnswerExtractor):
    """Answer extractor specifically tailored for AR-LSAT dataset format"""
    
    def extract_answer(self, response_text: str, label: str, answers: Optional[list] = None, reasoning_method: str = "cot") -> Tuple[bool, str]:
        """
        Extract answer from response text and check if it matches the correct label.
        
        Args:
            response_text: The model's response text containing reasoning and answer
            label: The correct answer option index (0, 1, 2, 3, 4) or letter (A, B, C, D, E)
            answers: List of answer choices (optional, for content matching)
        
        Returns:
            Tuple[bool, str]: (True if the extracted answer matches the label, result message)
        """
        if 'Traceback' in response_text or 'error' in response_text:
            return False, 'syntax error'

        # Convert label to index if it's a letter
        if isinstance(label, str) and label.upper() in ['A', 'B', 'C', 'D', 'E']:
            label_idx = ord(label.upper()) - ord('A')
        elif isinstance(label, int) or label.isdigit():
            label_idx = int(label)
        else:
            return False, 'invalid label format'

        # CoT pattern "Conclusion: {answer}"
        if reasoning_method == "cot":
            cot_answer = self._extract_cot_conclusion(response_text, answers)
            if cot_answer is not None:
                # Find the index of the extracted answer in the choices
                if answers is not None:
                    for i, choice in enumerate(answers):
                        if choice.strip() == cot_answer.strip():
                            is_correct = i == label_idx
                            if is_correct:
                                return True, None
                            else:
                                return False, 'semantic error'
                return False, 'answer not found in choices'
        elif reasoning_method == "one-step" or reasoning_method == "two-step" or reasoning_method == "three-step" or reasoning_method == "combined":
            raise ValueError(f"Unsupported reasoning method: {reasoning_method}")

    def _extract_cot_conclusion(self, response_text: str, answers: Optional[list] = None) -> Optional[str]:
        """
        Extract the chosen answer from CoT response text using various patterns.
        """

        # Define patterns to check in order of preference
        # Put more specific patterns first to avoid greedy matching issues
        patterns = [
            (r"\$\\boxed\{([A-E])\}\$", "LaTeX boxed answer (letter only)"),  # New pattern for Gemini-2.5-Flash
            (r"The correct option is:\s*\[([0-4])\]", "The correct option is with brackets and number"),  # New pattern for [X] format
            (r"The correct option is:\s*([0-4])\b", "The correct option is (number only)"),  # New pattern for numbers
            (r"The correct option is:\s*([A-E])\b", "The correct option is (letter only)"),
            (r"Final Answer:\s*\[([0-4])\]", "Final Answer with brackets and number"),  # New pattern
            (r"Final Answer:\s*([0-4])\b", "Final Answer (number only)"),  # New pattern
            (r"Final Answer:\s*\{([^}]+)\}", "Final Answer with braces"),
            (r"Final Answer:\s*([A-E])\b", "Final Answer (letter only)"),
            (r"Final Answer:\s*(.+)", "Final Answer without braces"),
            (r"Conclusion:\s*\[([0-4])\]", "Conclusion with brackets and number"),  # New pattern
            (r"Conclusion:\s*([0-4])\b", "Conclusion (number only)"),  # New pattern
            (r"Conclusion:\s*\{([^}]+)\}", "Conclusion with braces"),
            (r"The correct option is:\s*(.+)", "The correct option is"),
            (r"Conclusion:\s*(.+)", "Conclusion without braces")
        ]
        
        for pattern, description in patterns:
            match = re.search(pattern, response_text, re.IGNORECASE)
            if match:
                extracted_answer = match.group(1).strip()
                
                # Handle numeric indices (0, 1, 2, 3, 4)
                if extracted_answer.isdigit() and answers:
                    numeric_idx = int(extracted_answer)
                    if 0 <= numeric_idx < len(answers):
                        return answers[numeric_idx]
                
                # Handle single letter answers (A, B, C, D, E)
                if extracted_answer.upper() in ['A', 'B', 'C', 'D', 'E'] and answers:
                    # Convert letter to index and return the corresponding full answer
                    letter_idx = ord(extracted_answer.upper()) - ord('A')
                    if 0 <= letter_idx < len(answers):
                        return answers[letter_idx]
                
                # Check if the extracted answer matches any full answer option
                if answers and extracted_answer in answers:
                    return extracted_answer
                
                # If no answers list provided, return the extracted answer as-is
                if not answers:
                    return extracted_answer
                    
                # If we have answers but no match, try partial matching for robustness
                if answers:
                    for answer in answers:
                        if extracted_answer.lower() in answer.lower():
                            return answer
                
                # If this pattern didn't work, continue to the next pattern
                continue
        
        # No match found
        return None


class ProofWriter_AnswerExtractor(AnswerExtractor):
    """Answer extractor specifically tailored for FOLIO dataset format"""
    
    def extract_answer(self, response_text: Union[str, Optional[bool]], label: str, reasoning_method: str = "cot") -> Tuple[bool, str]:
        """
        Extract answer from response text and check if it matches the correct label.
        
        Args:
            response_text: The model's response text containing reasoning and answer
            label: The correct answer option letter (A, B, C)
        
        Returns:
            Tuple[bool, str]: (True if the extracted answer matches the label, result message)
        """       
        is_valid, return_value = self._extract_single_answer(response_text, reasoning_method)
        if is_valid:
            if self._judge_answer(return_value, label, reasoning_method):
                return True, None
            else:
                return False, 'semantic error'
        else:
            return False, return_value

    def _extract_single_answer(self, response_text: Union[str, Optional[bool]], reasoning_method: str = "cot") -> Tuple[bool, str]:
        """Extract answers from one response text"""
        if reasoning_method == "cot":
            keywords = ['A', 'B', 'C', 'True', 'False', 'Unknown']
            positions = {word: response_text.rfind(word) for word in keywords}

            valid_positions = {k: v for k, v in positions.items() if v != -1}
            
            if not valid_positions:
                return False, 'answer not found in choices'

            target = max(valid_positions.items(), key=lambda x: x[1])[0]
            if target == 'A' or target == 'True':
                return True, 'A'
            elif target == 'B' or target == 'False':
                return True, 'B'
            elif target == 'C' or target == 'Unknown':
                return True, 'C'
            else:
                return False, 'semantic error'
            
        # if isinstance(response_text, str) and ('Traceback' in response_text or 'error' in response_text.lower()):
            # return False, 'syntax error'
        
        if reasoning_method == "one-step" or reasoning_method == "two-step" or reasoning_method == "three-step":
            raise ValueError(f"Unsupported reasoning method: {reasoning_method}")
            
    def _judge_answer(self, extract_answer: List[str], label: str, reasoning_method: str = "cot") -> bool:
        """Determine whether the extracted answer is correct"""
        return extract_answer == label


class FOLIO_AnswerExtractor(AnswerExtractor):
    """Answer extractor specifically tailored for FOLIO dataset format"""
    
    def extract_answer(self, response_text: Union[str, Optional[bool]], label: str, reasoning_method: str = "cot") -> Tuple[bool, str]:
        """
        Extract answer from response text and check if it matches the correct label.
        
        Args:
            response_text: The model's response text containing reasoning and answer
            label: The correct answer option letter (A, B, C)
        
        Returns:
            Tuple[bool, str]: (True if the extracted answer matches the label, result message)
        """       
        is_valid, return_value = self._extract_single_answer(response_text, reasoning_method)
        if is_valid:
            if self._judge_answer(return_value, label, reasoning_method):
                return True, None
            else:
                return False, 'semantic error'
        else:
            return False, return_value

    def _extract_single_answer(self, response_text: Union[str, Optional[bool]], reasoning_method: str = "cot") -> Tuple[bool, str]:
        """Extract answers from one response text"""
        if reasoning_method == "cot":
            keywords = ['A', 'B', 'C', 'True', 'False', 'Uncertain']
            positions = {word: response_text.rfind(word) for word in keywords}

            valid_positions = {k: v for k, v in positions.items() if v != -1}
            
            if not valid_positions:
                return False, 'answer not found in choices'

            target = max(valid_positions.items(), key=lambda x: x[1])[0]
            if target == 'A' or target == 'True':
                return True, 'A'
            elif target == 'B' or target == 'False':
                return True, 'B'
            elif target == 'C' or target == 'Uncertain':
                return True, 'C'
            else:
                return False, 'semantic error'
            
        if isinstance(response_text, str) and ('Traceback' in response_text or 'error' in response_text.lower()):
            return False, 'syntax error'
        
        if reasoning_method == "one-step" or reasoning_method == "two-step" or reasoning_method == "three-step":
            raise ValueError(f"Unsupported reasoning method: {reasoning_method}")
            
    def _judge_answer(self, extract_answer: List[str], label: str, reasoning_method: str = "cot") -> bool:
        """Determine whether the extracted answer is correct"""
        return extract_answer == label


class ProntoQA_AnswerExtractor(AnswerExtractor):
    """Answer extractor specifically tailored for ProntoQA dataset format"""
    
    def extract_answer(self, response_text: Union[str, Optional[bool]], label: str, reasoning_method: str = "cot") -> Tuple[bool, str]:
        """
        Extract answer from response text and check if it matches the correct label.
        
        Args:
            response_text: The model's response text containing reasoning and answer
            label: The correct answer option letter (A, B)
        
        Returns:
            Tuple[bool, str]: (True if the extracted answer matches the label, result message)
        """       
        is_valid, return_value = self._extract_single_answer(response_text, reasoning_method)
        if is_valid:
            if self._judge_answer(return_value, label, reasoning_method):
                return True, None
            else:
                return False, 'semantic error'
        else:
            return False, return_value

    def _extract_single_answer(self, response_text: Union[str, Optional[bool]], reasoning_method: str = "cot") -> Tuple[bool, str]:
        """Extract answers from one response text"""
        if reasoning_method == "cot":
            keywords = ['A', 'B', 'True', 'False']
            positions = {word: response_text.rfind(word) for word in keywords}

            valid_positions = {k: v for k, v in positions.items() if v != -1}
            
            if not valid_positions:
                return False, 'answer not found in choices'

            target = max(valid_positions.items(), key=lambda x: x[1])[0]
            if target == 'A' or target == 'True':
                return True, 'A'
            elif target == 'B' or target == 'False':
                return True, 'B'
            else:
                return False, 'semantic error'
            
        if isinstance(response_text, str) and ('Traceback' in response_text or 'error' in response_text.lower()):
            return False, 'syntax error'
        
        if reasoning_method == "one-step" or reasoning_method == "two-step" or reasoning_method == "three-step":
            raise ValueError(f"Unsupported reasoning method: {reasoning_method}")
            
    def _judge_answer(self, extract_answer: List[str], label: str, reasoning_method: str = "cot") -> bool:
        """Determine whether the extracted answer is correct"""
        return extract_answer == label
    
    
class LogicalDeduction_AnswerExtractor(AnswerExtractor):
    """Answer extractor specifically tailored for LogicalDeduction dataset format"""
    
    def extract_answer(self, response_text: str, label: str, reasoning_method: str = "cot") -> Tuple[bool, str]:
        """
        Extract answer from response text and check if it matches the correct label.
        
        Args:
            response_text: The model's response text containing reasoning and answer
            label: The correct answer option letter (A, B, C, D, E, F, G)
        
        Returns:
            Tuple[bool, str]: (True if the extracted answer matches the label, result message)
        """       
        is_valid, return_value = self._extract_single_answer(response_text, reasoning_method)
        if is_valid:
            if self._judge_answer(return_value, label, reasoning_method):
                return True, None
            else:
                return False, 'semantic error'
        else:
            return False, return_value

    def _extract_single_answer(self, response_text: str, reasoning_method: str = "cot") -> Tuple[bool, str]:
        """Extract answers from one response text"""
        if reasoning_method == "cot":
            keywords = ['A)', 'B)', 'C)', 'D)', 'E)', 'F)', 'G)']
            positions = {word: response_text.rfind(word) for word in keywords}

            valid_positions = {k: v for k, v in positions.items() if v != -1}
            
            if not valid_positions:
                return False, 'answer not found in choices'

            target = max(valid_positions.items(), key=lambda x: x[1])[0]
            if target == 'A)':
                return True, 'A'
            elif target == 'B)':
                return True, 'B'
            elif target == 'C)':
                return True, 'C'
            elif target == 'D)':
                return True, 'D'
            elif target == 'E)':
                return True, 'E'
            elif target == 'F)':
                return True, 'F'
            elif target == 'G)':
                return True, 'G'
            else:
                return False, 'semantic error'
            
        if isinstance(response_text, str) and ('Traceback' in response_text or 'error' in response_text.lower()):
            return False, 'syntax error'
        
        if reasoning_method == "one-step" or reasoning_method == "two-step" or reasoning_method == "three-step":
            raise ValueError(f"Unsupported reasoning method: {reasoning_method}")
            
        return False, 'semantic error'
            
    def _judge_answer(self, extract_answer: str, label: str, reasoning_method: str = "cot") -> bool:
        """Determine whether the extracted answer is correct"""
        return extract_answer == label