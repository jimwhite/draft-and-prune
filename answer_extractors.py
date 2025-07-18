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
    
    @abstractmethod
    def extract_answer_with_majority_vote(self, response_texts: List[str], label: str, answers: Optional[list] = None, reasoning_method: str = "cot") -> Tuple[bool, str]:
        """Extract answers from multiple response texts and perform majority voting"""
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

        # Solver output pattern - handle list format like [2] or [0, 1, 2, 3, 4]
        elif reasoning_method == "one-step" or reasoning_method == "two-step" or reasoning_method == "three-step" or reasoning_method == "combined":
            if answers is not None:
                response_clean = response_text.strip()
                
                # Try to extract list format from solver output
                list_match = re.search(r'\[([^\]]*)\]', response_clean)
                if list_match:
                    list_content = list_match.group(1).strip()
                    if list_content:  # Non-empty list
                        # Parse the list content
                        try:
                            # Handle comma-separated integers
                            if ',' in list_content:
                                indices = [int(x.strip()) for x in list_content.split(',') if x.strip().isdigit()]
                            else:
                                # Single integer
                                indices = [int(list_content)] if list_content.isdigit() else []
                            
                            if indices:
                                # Check if the correct label is in the list
                                if label_idx in indices:
                                    # If only one answer and it's correct, that's perfect
                                    if len(indices) == 1:
                                        return True, None
                                    else:
                                        # Multiple answers including the correct one
                                        return False, 'multiple answers'
                                else:
                                    # Correct answer not in the list
                                    return False, 'semantic error'
                            else:
                                # Empty list or invalid content
                                return False, 'empty or invalid list'
                        except ValueError:
                            return False, 'invalid list format'
                    else:
                        # Empty list []
                        return False, 'empty list'
                
                # Fallback: Try to match by index (solver output is index as string or int)
                if response_clean.isdigit():
                    idx = int(response_clean)
                    is_correct = idx == label_idx
                    if 0 <= idx < len(answers):
                        if is_correct:
                            return True, None
                        else:
                            return False, 'semantic error'
        
        return False, 'semantic error'

    def extract_answer_with_majority_vote(self, response_texts: List[str], label: str, answers: Optional[list] = None, reasoning_method: str = "cot") -> Tuple[bool, str]:
        """
        Extract answers from multiple response texts, filter for single-length answers, and perform majority voting.
        
        Args:
            response_texts: List of model response texts
            label: The correct answer option index (0, 1, 2, 3, 4) or letter (A, B, C, D, E)
            answers: List of answer choices (optional, for content matching)
            reasoning_method: The reasoning method used
        
        Returns:
            Tuple[bool, str]: (True if the majority vote matches the label, result message)
        """
        if not response_texts:
            return False, 'no responses provided'
        
        # Convert label to index if it's a letter
        if isinstance(label, str) and label.upper() in ['A', 'B', 'C', 'D', 'E']:
            label_idx = ord(label.upper()) - ord('A')
        elif isinstance(label, int) or label.isdigit():
            label_idx = int(label)
        else:
            return False, 'invalid label format'
        
        # Extract single-length answers from all responses
        single_answers = []
        error_stats = Counter()
        
        for response_text in response_texts:
            if 'Traceback' in response_text or 'error' in response_text:
                error_stats['syntax error'] += 1
                continue
                
            # Extract answer based on reasoning method
            extracted_answer = self._extract_single_answer(response_text, answers, reasoning_method)
            if extracted_answer is not None:
                single_answers.append(extracted_answer)
            else:
                error_stats['extraction failed'] += 1
        
        # Check if we have any valid single answers
        if not single_answers:
            most_common_error = error_stats.most_common(1)[0][0] if error_stats else 'no valid answers'
            return False, f'no single answers found: {most_common_error}'
        
        # Perform majority voting
        answer_counts = Counter(single_answers)
        majority_answer, majority_count = answer_counts.most_common(1)[0]
        
        # Check if there's a clear majority (more than half)
        total_votes = len(single_answers)
        if majority_count > total_votes / 2:
            is_correct = majority_answer == label_idx
            confidence = majority_count / total_votes
            
            if is_correct:
                return True, f'majority vote correct: {majority_answer} ({majority_count}/{total_votes}, {confidence:.2%})'
            else:
                return False, f'majority vote incorrect: {majority_answer} vs {label_idx} ({majority_count}/{total_votes}, {confidence:.2%})'
        else:
            # No clear majority - return the most common answer but indicate tie
            is_correct = majority_answer == label_idx
            confidence = majority_count / total_votes
            
            if is_correct:
                return True, f'plurality vote correct: {majority_answer} ({majority_count}/{total_votes}, {confidence:.2%})'
            else:
                return False, f'plurality vote incorrect: {majority_answer} vs {label_idx} ({majority_count}/{total_votes}, {confidence:.2%})'

    def _extract_single_answer(self, response_text: str, answers: Optional[list] = None, reasoning_method: str = "cot") -> Optional[int]:
        """
        Extract a single answer index from response text, returning None if not a single answer.
        
        Args:
            response_text: The model's response text
            answers: List of answer choices (optional)
            reasoning_method: The reasoning method used
        
        Returns:
            Optional[int]: The answer index if single answer found, None otherwise
        """
        # CoT pattern "Conclusion: {answer}"
        if reasoning_method == "cot":
            cot_answer = self._extract_cot_conclusion(response_text, answers)
            if cot_answer is not None and answers is not None:
                # Find the index of the extracted answer in the choices
                for i, choice in enumerate(answers):
                    if choice.strip() == cot_answer.strip():
                        return i
                return None
        
        # Solver output pattern - handle list format like [2] or [0, 1, 2, 3, 4]
        elif reasoning_method in ["one-step", "two-step", "three-step", "combined"]:
            if answers is not None:
                response_clean = response_text.strip()
                
                # Try to extract list format from solver output
                list_match = re.search(r'\[([^\]]*)\]', response_clean)
                if list_match:
                    list_content = list_match.group(1).strip()
                    if list_content:  # Non-empty list
                        # Parse the list content
                        try:
                            # Handle comma-separated integers
                            if ',' in list_content:
                                indices = [int(x.strip()) for x in list_content.split(',') if x.strip().isdigit()]
                            else:
                                # Single integer
                                indices = [int(list_content)] if list_content.isdigit() else []
                            
                            # Only return if it's a single answer
                            if len(indices) == 1:
                                idx = indices[0]
                                if 0 <= idx < len(answers):
                                    return idx
                            return None  # Multiple answers or invalid range
                        except ValueError:
                            return None
                    else:
                        return None  # Empty list
                
                # Fallback: Try to match by index (solver output is index as string or int)
                if response_clean.isdigit():
                    idx = int(response_clean)
                    if 0 <= idx < len(answers):
                        return idx
        
        return None

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

    def extract_answer_with_majority_vote(self, response_texts: List[str], label: str, answers: Optional[list] = None, reasoning_method: str = "cot") -> Tuple[bool, str]:
        raise NotImplementedError("Majority vote is not implemented for ProofWriter.")


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

    def extract_answer_with_majority_vote(self, response_texts: List[str], label: str, answers: Optional[list] = None, reasoning_method: str = "cot") -> Tuple[bool, str]:
        raise NotImplementedError("Majority vote is not implemented for FOLIO.")
