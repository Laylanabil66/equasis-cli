#!/usr/bin/env python3
"""
Output Formatter - Handles different output formats for vessel, fleet, and search data
"""

import json
from typing import List
from dataclasses import asdict

from .parser import EquasisVesselData
from .client import SimpleVesselInfo, FleetInfo


class OutputFormatter:
    """Handle different output formats"""

    @staticmethod
    def format_vessel_info(vessel_data: EquasisVesselData, output_format: str = 'table', detail_level: str = 'summary'):
        """Format comprehensive vessel information"""
        if output_format == 'json':
            return json.dumps({
                'basic_info': asdict(vessel_data.basic_info),
                'overview': vessel_data.overview,
                'management': [asdict(c) for c in vessel_data.management],
                'classification': [asdict(c) for c in vessel_data.classification],
                'geographical': [asdict(g) for g in vessel_data.geographical],
                'inspections': [asdict(i) for i in vessel_data.inspections],
                'historical_names': [asdict(h) for h in vessel_data.historical_names],
                'historical_flags': [asdict(h) for h in vessel_data.historical_flags],
                'historical_companies': [asdict(h) for h in vessel_data.historical_companies]
            }, indent=2)
        elif output_format == 'csv':
            # Basic CSV format for compatibility
            basic = vessel_data.basic_info
            return f"{basic.imo},{basic.name},{basic.flag},{basic.vessel_type or ''},{basic.dwt or ''},{basic.gross_tonnage or ''},{basic.year_built or ''}"
        else:  # table format
            return OutputFormatter._format_comprehensive_table(vessel_data, detail_level)

    @staticmethod
    def _format_comprehensive_table(vessel_data: EquasisVesselData, detail_level: str = 'summary'):
        """Format comprehensive vessel data as a table"""
        basic = vessel_data.basic_info
        output = f"""
Vessel Information (Comprehensive):
===================================
IMO Number:    {basic.imo}
Name:          {basic.name}
Flag:          {basic.flag} ({basic.flag_code or 'N/A'})
Call Sign:     {basic.call_sign or 'N/A'}
MMSI:          {basic.mmsi or 'N/A'}
Type:          {basic.vessel_type or 'N/A'}
Gross Tonnage: {basic.gross_tonnage or 'N/A'}
DWT:           {basic.dwt or 'N/A'}
Year Built:    {basic.year_built or 'N/A'}
Status:        {basic.status or 'N/A'}
Last Update:   {basic.last_update or 'N/A'}
"""

        # Add overview section
        if vessel_data.overview:
            output += "\nOverview:\n" + "-" * 9 + "\n"
            for key, value in vessel_data.overview.items():
                formatted_key = key.replace('_', ' ').title()
                output += f"{formatted_key}: {value}\n"

        # Add management companies
        if vessel_data.management:
            output += f"\nManagement Companies ({len(vessel_data.management)}):\n" + "-" * 30 + "\n"
            for company in vessel_data.management:
                output += f"• {company.name} ({company.role})\n"
                if company.date_effect and detail_level == 'detailed':
                    output += f"  Since: {company.date_effect}\n"

        # Add classification
        if vessel_data.classification:
            output += f"\nClassification ({len(vessel_data.classification)}):\n" + "-" * 16 + "\n"
            for cls in vessel_data.classification:
                output += f"• {cls.society} - {cls.status}\n"
                if cls.date_effect and detail_level == 'detailed':
                    output += f"  {cls.date_effect}\n"

        # Add recent inspections
        if vessel_data.inspections:
            recent_count = min(3, len(vessel_data.inspections)) if detail_level == 'summary' else len(vessel_data.inspections)
            output += f"\nRecent PSC Inspections ({recent_count} of {len(vessel_data.inspections)}):\n" + "-" * 35 + "\n"
            for inspection in vessel_data.inspections[:recent_count]:
                output += f"• {inspection.date}: {inspection.psc_organization}\n"
                if inspection.detention != 'No detention':
                    output += f"  ⚠️  Detention: {inspection.detention}\n"

        # Add historical data summary
        if vessel_data.historical_names and detail_level == 'summary':
            output += f"\nHistorical Names ({len(vessel_data.historical_names)} total):\n" + "-" * 22 + "\n"
            for name in vessel_data.historical_names[:3]:
                output += f"• {name.name} ({name.date_effect})\n"
            if len(vessel_data.historical_names) > 3:
                output += f"  ... and {len(vessel_data.historical_names) - 3} more\n"

        # Detailed historical data
        elif vessel_data.historical_names and detail_level == 'detailed':
            output += f"\nHistorical Names ({len(vessel_data.historical_names)}):\n" + "-" * 18 + "\n"
            for name in vessel_data.historical_names:
                output += f"• {name.name} (since {name.date_effect})\n"

        if vessel_data.historical_flags and detail_level == 'detailed':
            output += f"\nHistorical Flags ({len(vessel_data.historical_flags)}):\n" + "-" * 18 + "\n"
            for flag in vessel_data.historical_flags:
                output += f"• {flag.flag} (since {flag.date_effect})\n"

        return output

    @staticmethod
    def format_simple_vessel_list(vessels: List[SimpleVesselInfo], output_format: str = 'table'):
        """Format simple vessel list for search results"""
        if output_format == 'json':
            return json.dumps([vessel.__dict__ for vessel in vessels], indent=2)
        elif output_format == 'csv':
            lines = ['IMO,Name,Flag,Type,DWT,GRT,YearBuilt,Status']
            for vessel in vessels:
                lines.append(f"{vessel.imo},{vessel.name},{vessel.flag},{vessel.vessel_type},{vessel.dwt or ''},{vessel.grt or ''},{vessel.year_built or ''},{vessel.status or ''}")
            return '\n'.join(lines)
        else:  # table format
            output = f"\nSearch Results ({len(vessels)} vessels found):\n" + "=" * 40 + "\n"
            for vessel in vessels:
                output += f"IMO: {vessel.imo} | Name: {vessel.name} | Flag: {vessel.flag} | Type: {vessel.vessel_type}\n"
            return output

    @staticmethod
    def format_fleet_info(fleet: FleetInfo, output_format: str = 'table'):
        """Format fleet information for output"""
        if output_format == 'json':
            return json.dumps({
                'company': fleet.company_name,
                'total_vessels': fleet.total_vessels,
                'vessels': [vessel.__dict__ for vessel in fleet.vessels]
            }, indent=2)
        elif output_format == 'csv':
            lines = ['IMO,Name,Flag,Type,DWT,GRT,YearBuilt,Status']
            for vessel in fleet.vessels:
                lines.append(f"{vessel.imo},{vessel.name},{vessel.flag},{vessel.vessel_type},{vessel.dwt or ''},{vessel.grt or ''},{vessel.year_built or ''},{vessel.status or ''}")
            return '\n'.join(lines)
        else:  # table format
            output = f"\nFleet Information: {fleet.company_name}\n"
            output += f"Total Vessels: {fleet.total_vessels}\n"
            output += "=" * 50 + "\n"
            for vessel in fleet.vessels:
                output += f"IMO: {vessel.imo} | Name: {vessel.name} | Flag: {vessel.flag} | Type: {vessel.vessel_type}\n"
            return output