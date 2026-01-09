"""
Integrations module for xnLinkFinder
Integrate with popular security tools
"""

from .nuclei_integration import NucleiIntegration
from .ffuf_integration import FFUFIntegration

__all__ = ['NucleiIntegration', 'FFUFIntegration']
