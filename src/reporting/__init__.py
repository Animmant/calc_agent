"""
Модуль для генерації звітів та PDF документів.
"""

from .pdf_generator import generate_debug_pdf, generate_math_notebook_pdf

__all__ = ['generate_debug_pdf', 'generate_math_notebook_pdf'] 