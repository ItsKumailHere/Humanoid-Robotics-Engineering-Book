# Validation System for RAG Responses
# Ensures accurate and reliable responses from the RAG chatbot

from typing import List, Dict, Any
from dataclasses import dataclass
import logging

@dataclass
class ValidationResult:
    """Represents the result of a validation check"""
    is_valid: bool
    confidence_score: float
    errors: List[str]
    warnings: List[str]
    metadata: Dict[str, Any]

class ContentValidator:
    """Validates content accuracy and reliability for RAG system"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def validate_response_content(self, 
                                 response: str, 
                                 source_chunks: List[Dict[str, Any]], 
                                 query: str) -> ValidationResult:
        """Validate that the response is accurate and based on the source content"""
        
        errors = []
        warnings = []
        metadata = {}
        
        # Check 1: Does the response contain information from the sources?
        source_text = " ".join([chunk['text'] for chunk in source_chunks])
        has_source_support = self._check_response_source_support(response, source_text)
        
        if not has_source_support:
            errors.append("Response contains information not found in source materials")
        
        # Check 2: Check for hallucinations
        hallucination_detected = self._check_for_hallucinations(response, source_chunks)
        if hallucination_detected:
            errors.append("Potential hallucination detected in response")
        
        # Check 3: Check for contradiction with source material
        contradiction_detected = self._check_for_contradictions(response, source_chunks)
        if contradiction_detected:
            errors.append("Response contradicts source material")
        
        # Calculate confidence score based on validation checks
        confidence_score = self._calculate_confidence_score(
            has_source_support, 
            not hallucination_detected, 
            not contradiction_detected
        )
        
        # Determine if response is valid
        is_valid = len(errors) == 0 and confidence_score >= 0.7
        
        metadata['source_support'] = has_source_support
        metadata['hallucination_detected'] = hallucination_detected
        metadata['contradiction_detected'] = contradiction_detected
        
        return ValidationResult(
            is_valid=is_valid,
            confidence_score=confidence_score,
            errors=errors,
            warnings=warnings,
            metadata=metadata
        )
    
    def _check_response_source_support(self, response: str, source_text: str) -> bool:
        """Check if the response is supported by the source text"""
        # This is a simplified check - in practice, this would use more sophisticated NLP
        response_lower = response.lower()
        source_lower = source_text.lower()
        
        # Check if a significant portion of the response content appears in the source
        response_words = set(response_lower.split())
        source_words = set(source_lower.split())
        
        if len(response_words) == 0:
            return False
        
        # Calculate overlap
        common_words = response_words.intersection(source_words)
        overlap_ratio = len(common_words) / len(response_words)
        
        # Consider it supported if at least 30% of the response content appears in sources
        return overlap_ratio >= 0.3
    
    def _check_for_hallucinations(self, response: str, source_chunks: List[Dict[str, Any]]) -> bool:
        """Check if the response contains hallucinated information"""
        # This is a simplified check - real implementation would be more sophisticated
        source_text = " ".join([chunk['text'] for chunk in source_chunks])
        
        # Look for specific indicators of hallucination
        hallucination_indicators = [
            "according to the textbook",
            "the book mentions", 
            "as stated in chapter",
            "the text says"
        ]
        
        # Check if response makes claims about specific statements in the text
        # when those statements don't appear in the sources
        response_lower = response.lower()
        
        for indicator in hallucination_indicators:
            if indicator in response_lower:
                # If the response claims specific statements from the text,
                # verify they exist in the source
                # This is a placeholder - real implementation would be more thorough
                return False  # Placeholder return
        
        return False
    
    def _check_for_contradictions(self, response: str, source_chunks: List[Dict[str, Any]]) -> bool:
        """Check if the response contradicts the source material"""
        # This is a simplified check - real implementation would use NLP
        source_text = " ".join([chunk['text'] for chunk in source_chunks])
        
        # Placeholder implementation - in reality, this would use more sophisticated
        # contradiction detection algorithms
        return False
    
    def _calculate_confidence_score(self, 
                                   has_source_support: bool, 
                                   no_hallucinations: bool, 
                                   no_contradictions: bool) -> float:
        """Calculate a confidence score based on validation results"""
        score = 0.0
        
        if has_source_support:
            score += 0.4
        if no_hallucinations:
            score += 0.3
        if no_contradictions:
            score += 0.3
        
        return score

class QueryValidator:
    """Validates user queries for the RAG system"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def validate_query(self, query: str) -> ValidationResult:
        """Validate that the query is appropriate for the RAG system"""
        errors = []
        warnings = []
        metadata = {}
        
        # Check query length
        if len(query.strip()) == 0:
            errors.append("Query cannot be empty")
        elif len(query.strip()) < 3:
            errors.append("Query is too short")
        elif len(query) > 500:
            warnings.append("Query is very long, consider being more specific")
        
        # Check for potentially inappropriate content
        has_inappropriate_content = self._check_inappropriate_content(query)
        if has_inappropriate_content:
            errors.append("Query may contain inappropriate content")
        
        # Determine validity
        is_valid = len(errors) == 0
        
        # Calculate confidence (not really applicable for queries, but included for consistency)
        confidence_score = 1.0 if is_valid else 0.0
        
        return ValidationResult(
            is_valid=is_valid,
            confidence_score=confidence_score,
            errors=errors,
            warnings=warnings,
            metadata=metadata
        )
    
    def _check_inappropriate_content(self, query: str) -> bool:
        """Check for potentially inappropriate content in the query"""
        # This is a simple implementation - in practice, you'd use more sophisticated content filtering
        inappropriate_indicators = [
            "hack",
            "exploit",
            "bypass",
            "circumvent"
        ]
        
        query_lower = query.lower()
        for indicator in inappropriate_indicators:
            if indicator in query_lower:
                return True
        
        return False

# Global instances
content_validator = ContentValidator()
query_validator = QueryValidator()