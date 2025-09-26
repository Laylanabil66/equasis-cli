#!/usr/bin/env python3
"""
Equasis CLI Tool - A command-line interface for accessing Equasis maritime data

This package provides programmatic access to vessel and fleet information
from the Equasis database through a clean, scriptable CLI interface.
"""

from .main import main
from .client import EquasisClient, SimpleVesselInfo, FleetInfo
from .parser import EquasisParser, EquasisVesselData, VesselBasicInfo
from .formatter import OutputFormatter

__version__ = "1.0.0"
__author__ = "rhinonix"
__email__ = "rhinonix.github.exclaim769@slmail.me"

# Public API
__all__ = [
    'main',
    'EquasisClient',
    'EquasisParser',
    'EquasisVesselData',
    'VesselBasicInfo',
    'SimpleVesselInfo',
    'FleetInfo',
    'OutputFormatter'
]