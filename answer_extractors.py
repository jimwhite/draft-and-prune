#!/usr/bin/env python3
import re
from typing import Tuple, Optional
from abc import ABC, abstractmethod
class AnswerExtractor(ABC):
    """Base class for answer extractors"""
    
    @abstractmethod
    def extract_answer(self, response_text: str, label: str) -> Tuple[bool, str]:
        """Extract the answer from the response text"""
        pass

class AR_LSAT_AnswerExtractor(AnswerExtractor):
    """Answer extractor specifically tailored for AR-LSAT dataset format"""
    
    def extract_answer(self, response_text: str, label: str) -> Tuple[bool, str]:
        """
        Extract answer from response text and check if it matches the correct label.
        
        Args:
            response_text: The model's response text containing reasoning and answer
            label: The correct answer option (A, B, C, D, or E)
        
        Returns:
            Tuple[bool, str]: (True if the extracted answer matches the label, result message)
        """
        if 'Traceback' in response_text:
            return False, 'syntax error'
        
        # Z3 pattern - "Option X is correct"
        answer_match = re.search(r"Option\s+([A-E])\s+is\s+correct", response_text, re.IGNORECASE)
        if answer_match:
            chosen_option = answer_match.group(1)
            print(f"Answer match found: {chosen_option}")
            
            # Convert numeric label to letter if needed
            if isinstance(label, int) or label.isdigit():
                # Convert 0-based index to letter (0->A, 1->B, etc.)
                label_idx = int(label)
                label_letter = chr(ord('A') + label_idx)
                is_correct = chosen_option == label_letter
            else:
                is_correct = chosen_option == label
            
            return is_correct, None
        else:
            return False, 'semantic error'

# class CoTAnswerExtractor(AnswerExtractor):
#     """Answer extractor for Chain-of-Thought style reasoning"""
    
#     def extract_answer(self, response_text: str) -> Tuple[Optional[str], Optional[str]]:
#         if not response_text:
#             return None, None
                
#         # CoT often concludes with simple statements like "Therefore, the answer is X"
#         answer_match = re.search(r"(?:Therefore|Thus|Hence|So|In conclusion),?\s+(?:the )?(?:answer|option|choice) (?:is|should be|would be|must be)(?:\s*:)?\s*(?:option)?\s*([A-E])", 
#                                 response_text, re.IGNORECASE)
        
#         if answer_match:
#             chosen_option = answer_match.group(1).upper()
#             return response_text, chosen_option
        
#         # Try with boxed format
#         answer_match = re.search(r"\$\\boxed\{([A-E])\}\$", response_text)
#         if answer_match:
#             chosen_option = answer_match.group(1)
#             return response_text, chosen_option
            
#         # Try to find a explicit statement in the last paragraph
#         paragraphs = response_text.split('\n\n')
#         if paragraphs:
#             last_paragraph = paragraphs[-1]
#             answer_match = re.search(r"(?:answer|option|choice) (?:is|should be|would be)(?:\s*:)?\s*([A-E])", 
#                                     last_paragraph, re.IGNORECASE)
#             if answer_match:
#                 chosen_option = answer_match.group(1).upper()
#                 return response_text, chosen_option
        
#         # No matches found
#         print(f"Warning: Could not find any answer pattern in the CoT response.")
#         return response_text, None 
