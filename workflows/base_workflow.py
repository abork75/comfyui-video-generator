# -*- coding: utf-8 -*-
"""
Base Workflow Interface
All workflow types must implement this interface
"""

from abc import ABC, abstractmethod

class BaseWorkflow(ABC):
    """Abstract base class for workflow types"""
    
    @abstractmethod
    def validate_item(self, item, config):
        """
        Validate workflow-specific item requirements
        
        Args:
            item: FLOW item dict
            config: Full config dict
            
        Raises:
            ValueError: If validation fails
        """
        pass
    
    @abstractmethod
    def prepare_params(self, item, pair, config, target_resolution):
        """
        Prepare workflow-specific parameters
        
        Args:
            item: FLOW item dict
            pair: Frame pair dict
            config: Full config dict
            target_resolution: (width, height) tuple
            
        Returns:
            dict: Parameters for backend execution
        """
        pass
    
    @abstractmethod
    def get_template_path(self, config):
        """
        Get workflow template path
        
        Args:
            config: Full config dict
            
        Returns:
            Path: Path to workflow JSON template
        """
        pass
    
    def get_name(self):
        """Get workflow name"""
        return self.__class__.__name__.replace('Workflow', '').lower()