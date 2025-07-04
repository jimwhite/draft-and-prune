#!/usr/bin/env python3
import re
from typing import Tuple, Optional, Union
from abc import ABC, abstractmethod


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

        # Solver output pattern 'one of answer choices'
        elif reasoning_method == "one-step" or reasoning_method == "two-step" or reasoning_method == "three-step":
            if answers is not None:
                response_clean = response_text.strip()
                # Try to match by answer string
                # for i, answer_choice in enumerate(answers):
                #     if answer_choice.strip() == response_clean:
                #         is_correct = i == label_idx
                #         if is_correct:
                #             return True, None
                #         else:
                #             return False, 'semantic error'
                # Try to match by index (solver output is index as string or int)
                if response_clean.isdigit():
                    idx = int(response_clean)
                    is_correct = idx == label_idx
                    if 0 <= idx < len(answers):
                        if is_correct:
                            return True, None
                        else:
                            return False, 'semantic error'
        
        return False, 'semantic error'

    def _extract_cot_conclusion(self, response_text: str, answers: Optional[list] = None) -> Optional[str]:
        """
        Extract the chosen answer from CoT response text using various patterns.
        """

        # Define patterns to check in order of preference
        patterns = [
            (r"Final Answer:\s*\{([^}]+)\}", "Final Answer with braces"),
            (r"Final Answer:\s*(.+)", "Final Answer without braces"),
            (r"Conclusion:\s*\{([^}]+)\}", "Conclusion with braces"),
            (r"Conclusion:\s*(.+)", "Conclusion without braces")
        ]
        
        for pattern, description in patterns:
            match = re.search(pattern, response_text, re.IGNORECASE)
            if match:
                extracted_answer = match.group(1).strip()
                return extracted_answer
        
        # No match found
        return None


class ProofWriter_AnswerExtractor(AnswerExtractor):
    """Answer extractor specifically tailored for ProofWriter dataset format"""
    
    def extract_answer(self, response_text: Union[str, Optional[bool]], label: str, reasoning_method: str = "cot") -> Tuple[bool, str]:
        """
        Extract answer from response text and check if it matches the correct label.
        
        Args:
            response_text: The model's response text containing reasoning and answer
            label: The correct answer option letter (A, B, C)
        
        Returns:
            Tuple[bool, str]: (True if the extracted answer matches the label, result message)
        """       
        if reasoning_method == "cot":
            keywords = ['A', 'B', 'C', 'True', 'False', 'Unknown']
            positions = {word: response_text.rfind(word) for word in keywords}

            valid_positions = {k: v for k, v in positions.items() if v != -1}
            
            if not valid_positions:
                return False, 'answer not found in choices'

            target = max(valid_positions.items(), key=lambda x: x[1])[0]
            if (label == 'A' and (target == 'A' or target == 'True')) \
            or (label == 'B' and (target == 'B' or target == 'False')) \
            or (label == 'C' and (target == 'C' or target == 'Unknown')):
                return True, None
            else:
                return False, 'semantic error'
            
        if isinstance(response_text, str) and ('Traceback' in response_text or 'error' in response_text.lower()):
            return False, 'syntax error'
        
        if reasoning_method == "one-step" or reasoning_method == "two-step" or reasoning_method == "three-step":
            if (label == 'A' and response_text == True) \
            or (label == 'B' and response_text == False) \
            or (label == 'C' and response_text == None):
                return True, None
            else:
                return False, 'semantic error'


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
        if reasoning_method == "cot":
            keywords = ['A', 'B', 'C', 'True', 'False', 'Uncertain']
            positions = {word: response_text.rfind(word) for word in keywords}

            valid_positions = {k: v for k, v in positions.items() if v != -1}
            
            if not valid_positions:
                return False, 'answer not found in choices'

            target = max(valid_positions.items(), key=lambda x: x[1])[0]
            if (label == 'A' and (target == 'A' or target == 'True')) \
            or (label == 'B' and (target == 'B' or target == 'False')) \
            or (label == 'C' and (target == 'C' or target == 'Uncertain')):
                return True, None
            else:
                return False, 'semantic error'
            
        if isinstance(response_text, str) and ('Traceback' in response_text or 'error' in response_text.lower()):
            return False, 'syntax error'
        
        if reasoning_method == "one-step" or reasoning_method == "two-step" or reasoning_method == "three-step":
            if (label == 'A' and response_text == True) \
            or (label == 'B' and response_text == False) \
            or (label == 'C' and response_text == None):
                return True, None
            else:
                return False, 'semantic error'