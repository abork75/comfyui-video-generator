# -*- coding: utf-8 -*-
"""
Config Validator - Smart validation based on FLOW content

This validator:
1. Parses FLOW to understand what features are used
2. Validates ONLY required settings (flow-aware)
3. Auto-populates missing defaults (backwards compatibility)
4. Returns clear errors and warnings

Example:
    from config_validator import validate_and_prepare_config
    
    config = validate_and_prepare_config(raw_config)
    # Ready to use!
"""

from pathlib import Path
from flow_parser import parse_flow


class ValidationResult:
    """Result of config validation"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []
        self.config = None
    
    def is_valid(self):
        return len(self.errors) == 0
    
    def add_error(self, message):
        self.errors.append(message)
    
    def add_warning(self, message):
        self.warnings.append(message)
    
    def add_info(self, message):
        self.info.append(message)
    
    def print_summary(self):
        """Print validation summary"""
        from colorama import Fore, Style
        
        if self.errors:
            print(f"\n{Fore.RED}❌ ERRORS ({len(self.errors)}):{Style.RESET_ALL}")
            for e in self.errors:
                print(f"  • {e}")
        
        if self.warnings:
            print(f"\n{Fore.YELLOW}⚠️  WARNINGS ({len(self.warnings)}):{Style.RESET_ALL}")
            for w in self.warnings:
                print(f"  • {w}")
        
        if self.info:
            print(f"\n{Fore.CYAN}ℹ️  INFO:{Style.RESET_ALL}")
            for i in self.info:
                print(f"  • {i}")
        
        if not self.errors and not self.warnings:
            print(f"\n{Fore.GREEN}✅ Config validation passed!{Style.RESET_ALL}")


def validate_and_prepare_config(config):
    """
    Main validation function - validates and prepares config
    
    Args:
        config: Raw config dict
    
    Returns:
        ValidationResult with prepared config
    
    Raises:
        SystemExit if validation fails
    """
    
    result = ValidationResult()
    
    # Make a copy to modify
    import copy
    config = copy.deepcopy(config)
    
    # ============================================================
    # BASIC VALIDATION (always required)
    # ============================================================
    
    if 'project_folder' not in config:
        result.add_error("Missing required key: 'project_folder'")
    else:
        project_folder = Path(config['project_folder'])
        if not project_folder.exists():
            result.add_error(f"Project folder doesn't exist: {project_folder}")
    
    if 'flow' not in config:
        result.add_error("Missing required key: 'flow'")
    
    if not result.is_valid():
        result.config = config
        return result  # Stop early if basic validation fails
    
    # ============================================================
    # PARSE FLOW (to understand what's used)
    # ============================================================
    
    try:
        parser = parse_flow(config['flow'])
    except Exception as e:
        result.add_error(f"Failed to parse FLOW: {e}")
        result.config = config
        return result
    
    all_files = parser.get_all_files()
    transition_pairs = parser.get_transition_pairs()
    
    # ============================================================
    # FLOW-AWARE VALIDATION
    # ============================================================
    
    # Check which backends are used
    backends_used = set()
    for flow_file in all_files:
        backend = flow_file.config.get('backend', 'local')
        backends_used.add(backend)
    
    result.add_info(f"Backends used: {', '.join(backends_used)}")
    
    # Validate cloud backend (only if used)
    if 'cloud' in backends_used:
        import os
        
        # Check both config and environment variable
        api_key_in_config = config.get('comfy_icu_api_key', '')
        api_key_in_env = os.getenv('COMFY_ICU_API_KEY', '')
        
        if not api_key_in_config and not api_key_in_env:
            result.add_error("Cloud backend is used but COMFY_ICU_API_KEY is not set (check environment variables or config)")
        elif api_key_in_env:
            result.add_info("Using COMFY_ICU_API_KEY from environment variable")
        else:
            result.add_info("Using comfy_icu_api_key from config")
        
        # Check workflow ID
        if not config.get('comfy_icu_workflow_id'):
            result.add_error("Cloud backend is used but 'comfy_icu_workflow_id' is missing")
    
    # Check for chain feature
    has_chain = any('chain' in item for item in config['flow'] if isinstance(item, dict))
    
    if has_chain:
        # Auto-populate chain defaults
        if 'chain_transition_mode' not in config:
            config['chain_transition_mode'] = 'auto'
            result.add_info("Added default chain_transition_mode='auto'")
    
    # ============================================================
    # AUTO-POPULATE COMMON DEFAULTS
    # ============================================================
    
    defaults = {
        'debug_log': True,
        'default_backend': 'local',
        'default_duration': 16,
        'default_fps': 8,
        'default_steps': 25,
        'default_cfg': 2.5,
        'default_seed': -1,
        'default_positive_prompt': '',
        'default_negative_prompt': '',
        'skip_existed': True,
        'skip_ar_validation': False,
        'aspect_ratio_tolerance': 0.02,
        'aspect_ratio_strategy': 'most_common',
        'min_width': 256,
        'min_height': 256,
        'max_width': 1024,
        'max_height': 1024,
        'image_quality': 95,
    }
    
    added_defaults = []
    
    for key, default_value in defaults.items():
        if key not in config:
            config[key] = default_value
            added_defaults.append(key)
    
    if added_defaults:
        result.add_info(f"Added {len(added_defaults)} default values")
    
    # ============================================================
    # VALIDATE POSTPROCESSING (if enabled)
    # ============================================================
    
    pp_config = config.get('postprocessing', {})
    
    if pp_config.get('enabled', False):
        enabled_processors = []
        
        if pp_config.get('full_concat'):
            enabled_processors.append('full_concat')
        
        if pp_config.get('numbered_flow'):
            enabled_processors.append('numbered_flow')
        
        if not enabled_processors:
            result.add_warning("Postprocessing enabled but no processors selected")
        else:
            result.add_info(f"Postprocessing: {', '.join(enabled_processors)}")
    
    # ============================================================
    # VALIDATE FILE EXISTENCE (warnings only)
    # ============================================================
    
    project_folder = Path(config['project_folder'])
    chains_folder = project_folder / 'transitions' / 'chains'
    missing_files = []
    
    for flow_file in all_files:
        # ✅ Check location based on file type
        if flow_file.config.get('_is_chain', False):
            file_path = chains_folder / flow_file.filename
        else:
            file_path = project_folder / flow_file.filename
        
        # ✅ Check existence (outside if/else!)
        if not file_path.exists():
            missing_files.append(flow_file.filename)
    
    if missing_files:
        result.add_warning(f"Missing {len(missing_files)} source file(s) - will fail at runtime")
    
    # ============================================================
    # FINAL RESULT
    # ============================================================
    
    result.config = config
    return result


def build_config_from_globals(global_vars):
    """
    Build config dict from RUN file globals()
    
    Extracts only config-relevant variables (uppercase constants)
    and maps them to config dict structure.
    
    Args:
        global_vars: Result of globals() call
    
    Returns:
        Clean config dict
    
    Example:
        config = build_config_from_globals(globals())
    """
    
    config = {}
    
    # Direct mappings (uppercase variable → lowercase key)
    direct_mappings = {
        'PROJECT_FOLDER': 'project_folder',
        'FLOW': 'flow',
        'GENERIC_PROMPTS': 'generic_prompts',
        
        # Debug
        'DEBUG_LOG': 'debug_log',
        
        # Defaults
        'DEFAULT_BACKEND': 'default_backend',
        'DEFAULT_DURATION': 'default_duration',
        'DEFAULT_FPS': 'default_fps',
        'DEFAULT_STEPS': 'default_steps',
        'DEFAULT_CFG': 'default_cfg',
        'DEFAULT_SEED': 'default_seed',
        'DEFAULT_POSITIVE_PROMPT': 'default_positive_prompt',
        'DEFAULT_NEGATIVE_PROMPT': 'default_negative_prompt',
        
        # Resolution
        'MIN_WIDTH': 'min_width',
        'MIN_HEIGHT': 'min_height',
        'MAX_WIDTH': 'max_width',
        'MAX_HEIGHT': 'max_height',
        'DEFAULT_RESOLUTION': 'default_resolution',
        'FORCE_RESOLUTION': 'force_resolution',
        
        # Flags
        'SKIP_MISSING': 'skip_missing',
        'SKIP_EXISTED': 'skip_existed',
        'IMAGE_QUALITY': 'image_quality',
        'ASPECT_RATIO_TOLERANCE': 'aspect_ratio_tolerance',
        'ASPECT_RATIO_STRATEGY': 'aspect_ratio_strategy',
        
        # Postprocessing
        'POSTPROCESSING': 'postprocessing',
        
        # Local backend
        'CONFIG_PATH': 'config_path',
        'WORKFLOWS_PATH': 'workflows_path',
        'COMFYUI_OUTPUT_FOLDER': 'comfyui_output_folder',
        
        # Cloud backend
        'COMFY_ICU_WORKFLOW_ID': 'comfy_icu_workflow_id',
        'WORKFLOW_TEMPLATE_PATH': 'workflow_template_path',
    }
    
    # Extract variables
    for var_name, config_key in direct_mappings.items():
        if var_name in global_vars:
            config[config_key] = global_vars[var_name]
    
    return config


def validate_config_or_exit(config_or_globals):
    """
    Convenience function - validate and exit if errors
    
    Args:
        config_or_globals: Raw config dict OR globals() from RUN file
    
    Returns:
        Validated and prepared config dict
    """
    
    # Check if it's globals() (has __name__, __file__, etc.)
    if '__name__' in config_or_globals and '__file__' in config_or_globals:
        # Build config from globals
        config = build_config_from_globals(config_or_globals)
    else:
        # Already a config dict
        config = config_or_globals
    
    result = validate_and_prepare_config(config)
    
    result.print_summary()
    
    if not result.is_valid():
        print("\n❌ Config validation failed! Fix errors above.")
        exit(1)
    
    return result.config