from .python_analyzer import detect_code_smells as detect_python_smells, analyze_complexity as analyze_python_complexity
from .javascript_analyzer import detect_code_smells as detect_javascript_smells, analyze_complexity as analyze_javascript_complexity

__all__ = [
    'detect_python_smells',
    'analyze_python_complexity', 
    'detect_javascript_smells',
    'analyze_javascript_complexity'
]