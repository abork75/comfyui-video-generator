"""
Base class for transition generation backends
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class TransitionBackend(ABC):
    """
    Abstract base class for transition generation backends
    
    All backends (local, cloud, etc.) inherit from this
    """
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def generate(
        self, 
        start_frame: Path, 
        end_frame: Path, 
        params: Dict
    ) -> Optional[Path]:
        """
        Generate transition video between two frames
        
        Args:
            start_frame: Path to starting image
            end_frame: Path to ending image
            params: Generation parameters (prompts, duration, etc.)
            
        Returns:
            Path to generated video file, or None if failed
        """
        pass
    
    @abstractmethod
    def estimate_cost(self, params: Dict) -> Dict:
        """
        Estimate cost for this generation
        
        Args:
            params: Generation parameters
            
        Returns:
            Dict with cost info:
            {
                'cost_usd': float,
                'credits': int (if applicable),
                'backend': str
            }
        """
        pass
    
    @abstractmethod
    def estimate_time(self, params: Dict) -> int:
        """
        Estimate generation time in seconds
        
        Args:
            params: Generation parameters
            
        Returns:
            Estimated time in seconds
        """
        pass
    
    def validate_params(self, params: Dict) -> bool:
        """
        Validate generation parameters
        
        Args:
            params: Parameters to validate
            
        Returns:
            True if valid, False otherwise
        """
        required = ['width', 'height', 'fps', 'duration', 'pos_prompt', 'neg_prompt']
        
        for key in required:
            if key not in params:
                logger.error(f"Missing required parameter: {key}")
                return False
        
        return True
    
    def get_info(self) -> Dict:
        """
        Get backend information
        
        Returns:
            Dict with backend details
        """
        return {
            'name': self.name,
            'type': self.__class__.__name__
        }