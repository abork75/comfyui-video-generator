# -*- coding: utf-8 -*-
"""
Logger Utilities - Formatted console output
"""

from colorama import Fore, Style, init

init(autoreset=True)


class Logger:
    """
    Simple logger for batch transitions
    Provides formatted console output with colors
    """
    
    def __init__(self):
        pass
    
    def header(self, message):
        """Print header (big section)"""
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"{message:^70}")
        print(f"{'='*70}{Style.RESET_ALL}\n")
    
    def section(self, message):
        """Print section (medium separator)"""
        print(f"\n{Fore.YELLOW}{'─'*70}")
        print(f"{message}")
        print(f"{'─'*70}{Style.RESET_ALL}")
    
    def success(self, message):
        """Print success message (green)"""
        print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")
    
    def info(self, message):
        """Print info message (default color)"""
        print(f"  {message}")
    
    def warning(self, message):
        """Print warning message (yellow)"""
        print(f"{Fore.YELLOW}⚠ {message}{Style.RESET_ALL}")
    
    def error(self, message):
        """Print error message (red)"""
        print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")
    
    def debug(self, message):
        """Print debug message (magenta)"""
        print(f"{Fore.MAGENTA}[DEBUG] {message}{Style.RESET_ALL}")