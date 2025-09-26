#!/usr/bin/env python3
"""
Interactive Shell for Equasis CLI
Provides a REPL-style interface with slash command syntax similar to Claude Code
"""

import cmd
import re
import os
import sys
import logging
from typing import Dict, Optional, Tuple, Any
from dotenv import load_dotenv

from .client import EquasisClient
from .formatter import OutputFormatter
from .banner import display_banner, display_credentials_note, check_credentials, Colors

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class InteractiveShell(cmd.Cmd):
    """Interactive shell for Equasis CLI with slash command syntax"""

    intro = None  # We'll show banner in preloop
    prompt = f"{Colors.DIM_CYAN if Colors.supports_color() else ''}> {Colors.RESET if Colors.supports_color() else ''}"

    def __init__(self):
        super().__init__()
        self.client: Optional[EquasisClient] = None
        self.formatter = OutputFormatter()
        self.output_format = 'table'
        self.debug_mode = False
        self.logged_in = False

    def preloop(self):
        """Called once before the command loop starts"""
        # Show banner and check credentials
        display_banner(show_banner=True, show_info=True)
        print()

        if Colors.supports_color():
            print(f"{Colors.DIM}Type 'help' for available commands or 'exit' to quit.{Colors.RESET}")
            print(f"{Colors.DIM}Use /output with any command to save results to a file.{Colors.RESET}")
        else:
            print("Type 'help' for available commands or 'exit' to quit.")
            print("Use /output with any command to save results to a file.")
        print()

    def parseline(self, line):
        """Override parseline to handle empty lines gracefully"""
        if not line.strip():
            return '', '', line
        return super().parseline(line)

    def emptyline(self):
        """Override to do nothing on empty line (instead of repeating last command)"""
        pass

    def parse_slash_command(self, line: str, expected_params: Dict[str, bool]) -> Tuple[Dict[str, str], bool]:
        """
        Parse slash parameters like /imo 1234567 /format json

        Args:
            line: The command line to parse
            expected_params: Dict of {param_name: required} indicating expected parameters

        Returns:
            Tuple of (parsed_params, all_required_present)
        """
        params = {}

        # Match /param value or /param "quoted value"
        pattern = r'/(\w+)\s+(?:"([^"]+)"|(\S+))'
        matches = re.findall(pattern, line)

        for param, quoted_val, unquoted_val in matches:
            params[param] = quoted_val or unquoted_val

        # Check if all required parameters are present
        all_required_present = all(
            param in params
            for param, required in expected_params.items()
            if required
        )

        return params, all_required_present

    def ensure_authenticated(self) -> bool:
        """Ensure client is authenticated, prompt for credentials if needed"""
        if not self.client:
            # Check for credentials
            username = os.getenv('EQUASIS_USERNAME')
            password = os.getenv('EQUASIS_PASSWORD')

            if not username or not password:
                print()
                display_credentials_note()
                return False

            try:
                if Colors.supports_color():
                    print(f"{Colors.DIM}Connecting to Equasis...{Colors.RESET}")
                else:
                    print("Connecting to Equasis...")

                self.client = EquasisClient(username, password)
                self.logged_in = self.client.login()

                if self.logged_in:
                    if Colors.supports_color():
                        print(f"{Colors.DIM_GREEN}Connected successfully{Colors.RESET}")
                    else:
                        print("Connected successfully")
                    print()
                else:
                    if Colors.supports_color():
                        print(f"{Colors.DIM_RED}Authentication failed{Colors.RESET}")
                    else:
                        print("Authentication failed")
                    return False

            except Exception as e:
                if Colors.supports_color():
                    print(f"{Colors.DIM_RED}Connection error: {e}{Colors.RESET}")
                else:
                    print(f"Connection error: {e}")
                return False

        # Check if still logged in
        if not self.logged_in:
            if Colors.supports_color():
                print(f"{Colors.DIM}Reconnecting to Equasis...{Colors.RESET}")
            else:
                print("Reconnecting to Equasis...")
            self.logged_in = self.client.login()

        return self.logged_in

    def _handle_output_params(self, params):
        """Handle output format and file parameters"""
        # Set output format if specified (support both /format and /output)
        output_format = params.get('format') or self.output_format
        output_file = None

        # Handle /output parameter
        if 'output' in params:
            output_value = params['output']
            # Check if it's a filename (contains a dot) or just a format
            if '.' in output_value:
                output_file = output_value
                # Extract format from filename
                file_ext = output_value.split('.')[-1].lower()
                if file_ext in ['json', 'csv']:
                    output_format = file_ext
            else:
                # It's just a format specification
                if output_value in ['table', 'json', 'csv']:
                    output_format = output_value

        # Validate format
        if output_format not in ['table', 'json', 'csv']:
            if Colors.supports_color():
                print(f"{Colors.DIM_RED}Error: Invalid format. Use table, json, or csv{Colors.RESET}")
            else:
                print("Error: Invalid format. Use table, json, or csv")
            return None, None

        return output_format, output_file

    def _save_or_print_output(self, output, output_file, operation_name):
        """Save output to file or print to screen"""
        if output_file:
            # Save to file
            with open(output_file, 'w') as f:
                f.write(output)
            if Colors.supports_color():
                print(f"{Colors.DIM_GREEN}✓ {operation_name} data saved to {output_file}{Colors.RESET}")
            else:
                print(f"✓ {operation_name} data saved to {output_file}")
        else:
            # Print to screen
            print(output)

    def do_vessel(self, line: str):
        """
        Get comprehensive vessel information
        Usage: vessel /imo 1234567 [/format table|json|csv] [/output filename]

        Examples:
          vessel /imo 9074729
          vessel /imo 8515128 /format json
          vessel /imo 9074729 /output vessel_data.json
        """
        if not line.strip():
            self.help_vessel()
            return

        expected_params = {'imo': True, 'format': False, 'output': False}
        params, all_required = self.parse_slash_command(line, expected_params)

        if not all_required:
            if Colors.supports_color():
                print(f"{Colors.DIM_RED}Error: Missing required parameter /imo{Colors.RESET}")
            else:
                print("Error: Missing required parameter /imo")
            self.help_vessel()
            return

        if not self.ensure_authenticated():
            return

        # Handle output parameters
        output_format, output_file = self._handle_output_params(params)
        if output_format is None:
            return

        try:
            if Colors.supports_color():
                print(f"{Colors.DIM}Fetching vessel data for IMO {params['imo']}...{Colors.RESET}")
            else:
                print(f"Fetching vessel data for IMO {params['imo']}...")

            vessel = self.client.search_vessel_by_imo(params['imo'])

            if vessel:
                print()
                output = self.formatter.format_vessel_info(vessel, output_format)
                self._save_or_print_output(output, output_file, "Vessel")

                if Colors.supports_color():
                    print(f"{Colors.DIM_GREEN}✓ Vessel lookup completed{Colors.RESET}")
                else:
                    print("✓ Vessel lookup completed")
                print()
            else:
                if Colors.supports_color():
                    print(f"{Colors.DIM_RED}No vessel found with IMO: {params['imo']}{Colors.RESET}")
                else:
                    print(f"No vessel found with IMO: {params['imo']}")
                print()

        except Exception as e:
            if Colors.supports_color():
                print(f"{Colors.DIM_RED}Error: {e}{Colors.RESET}")
            else:
                print(f"Error: {e}")
            print()

    def do_search(self, line: str):
        """
        Search for vessels by name
        Usage: search /name "vessel name" [/format table|json|csv]

        Examples:
          search /name "MAERSK"
          search /name "EVER GIVEN" /format json
        """
        if not line.strip():
            self.help_search()
            return

        expected_params = {'name': True, 'format': False, 'output': False}
        params, all_required = self.parse_slash_command(line, expected_params)

        if not all_required:
            if Colors.supports_color():
                print(f"{Colors.DIM_RED}Error: Missing required parameter /name{Colors.RESET}")
            else:
                print("Error: Missing required parameter /name")
            self.help_search()
            return

        if not self.ensure_authenticated():
            return

        output_format = params.get('format', self.output_format)
        if output_format not in ['table', 'json', 'csv']:
            if Colors.supports_color():
                print(f"{Colors.DIM_RED}Error: Invalid format. Use table, json, or csv{Colors.RESET}")
            else:
                print("Error: Invalid format. Use table, json, or csv")
            return

        try:
            if Colors.supports_color():
                print(f"{Colors.DIM}Searching for vessels matching '{params['name']}'...{Colors.RESET}")
            else:
                print(f"Searching for vessels matching '{params['name']}'...")

            vessels = self.client.search_vessel_by_name(params['name'])

            if vessels:
                print()
                output = self.formatter.format_simple_vessel_list(vessels, output_format)
                print(output)

                if Colors.supports_color():
                    print(f"{Colors.DIM_GREEN}✓ Found {len(vessels)} vessel(s){Colors.RESET}")
                else:
                    print(f"✓ Found {len(vessels)} vessel(s)")
                print()
            else:
                if Colors.supports_color():
                    print(f"{Colors.DIM_RED}No vessels found matching: {params['name']}{Colors.RESET}")
                else:
                    print(f"No vessels found matching: {params['name']}")
                print()

        except Exception as e:
            if Colors.supports_color():
                print(f"{Colors.DIM_RED}Error: {e}{Colors.RESET}")
            else:
                print(f"Error: {e}")
            print()

    def do_fleet(self, line: str):
        """
        Get fleet information for a company
        Usage: fleet /company "company name" [/format table|json|csv]

        Examples:
          fleet /company "MAERSK LINE"
          fleet /company "MSC" /format json
        """
        if not line.strip():
            self.help_fleet()
            return

        expected_params = {'company': True, 'format': False, 'output': False}
        params, all_required = self.parse_slash_command(line, expected_params)

        if not all_required:
            if Colors.supports_color():
                print(f"{Colors.DIM_RED}Error: Missing required parameter /company{Colors.RESET}")
            else:
                print("Error: Missing required parameter /company")
            self.help_fleet()
            return

        if not self.ensure_authenticated():
            return

        output_format = params.get('format', self.output_format)
        if output_format not in ['table', 'json', 'csv']:
            if Colors.supports_color():
                print(f"{Colors.DIM_RED}Error: Invalid format. Use table, json, or csv{Colors.RESET}")
            else:
                print("Error: Invalid format. Use table, json, or csv")
            return

        try:
            if Colors.supports_color():
                print(f"{Colors.DIM}Fetching fleet data for '{params['company']}'...{Colors.RESET}")
            else:
                print(f"Fetching fleet data for '{params['company']}'...")

            fleet = self.client.get_fleet_info(params['company'])

            if fleet:
                print()
                output = self.formatter.format_fleet_info(fleet, output_format)
                print(output)

                if Colors.supports_color():
                    print(f"{Colors.DIM_GREEN}✓ Fleet lookup completed{Colors.RESET}")
                else:
                    print("✓ Fleet lookup completed")
                print()
            else:
                if Colors.supports_color():
                    print(f"{Colors.DIM_RED}No fleet found for company: {params['company']}{Colors.RESET}")
                else:
                    print(f"No fleet found for company: {params['company']}")
                print()

        except Exception as e:
            if Colors.supports_color():
                print(f"{Colors.DIM_RED}Error: {e}{Colors.RESET}")
            else:
                print(f"Error: {e}")
            print()

    def do_format(self, line: str):
        """
        Set default output format
        Usage: format table|json|csv

        Examples:
          format json
          format table
        """
        line = line.strip().lower()
        if line in ['table', 'json', 'csv']:
            self.output_format = line
            if Colors.supports_color():
                print(f"{Colors.DIM_GREEN}Default output format set to: {line}{Colors.RESET}")
            else:
                print(f"Default output format set to: {line}")
        else:
            if Colors.supports_color():
                print(f"{Colors.DIM_RED}Invalid format. Use: table, json, or csv{Colors.RESET}")
            else:
                print("Invalid format. Use: table, json, or csv")

    def do_output(self, line: str):
        """
        Information about saving output to files
        Usage: Use /output parameter with vessel, search, or fleet commands

        Examples:
          vessel /imo 9074729 /output vessel_data.json
          search /name "MAERSK" /output results.csv
          fleet /company "MSC" /output fleet.json

        You can also use /output to specify format:
          vessel /imo 9074729 /output json
        """
        if Colors.supports_color():
            print(f"""
{Colors.DIM_CYAN}output{Colors.RESET} - Save command results to files

{Colors.DIM}Usage:{Colors.RESET}
  Any command can use the /output parameter:
    command [parameters] /output filename.ext
    command [parameters] /output format

{Colors.DIM}Examples:{Colors.RESET}
  vessel /imo 9074729 /output vessel_data.json
  search /name "MAERSK" /output results.csv
  fleet /company "MSC" /output fleet.json
  vessel /imo 9074729 /output json

{Colors.DIM}Notes:{Colors.RESET}
  • File extension determines format (.json, .csv)
  • Use without extension to specify format only
  • Combine with /format for explicit format control
""")
        else:
            print("""
output - Save command results to files

Usage:
  Any command can use the /output parameter:
    command [parameters] /output filename.ext
    command [parameters] /output format

Examples:
  vessel /imo 9074729 /output vessel_data.json
  search /name "MAERSK" /output results.csv
  fleet /company "MSC" /output fleet.json
  vessel /imo 9074729 /output json

Notes:
  • File extension determines format (.json, .csv)
  • Use without extension to specify format only
  • Combine with /format for explicit format control
""")

    def do_clear(self, line: str):
        """Clear the screen"""
        os.system('clear' if os.name == 'posix' else 'cls')

    def do_status(self, line: str):
        """Show current session status"""
        print()
        if Colors.supports_color():
            print(f"{Colors.DIM_CYAN}Session Status:{Colors.RESET}")
            print(f"  Authentication: {Colors.DIM_GREEN + 'Connected' + Colors.RESET if self.logged_in else Colors.DIM_RED + 'Not connected' + Colors.RESET}")
            print(f"  Default Format: {Colors.DIM_WHITE + self.output_format + Colors.RESET}")
            print(f"  Debug Mode: {Colors.DIM_WHITE + str(self.debug_mode) + Colors.RESET}")
        else:
            print("Session Status:")
            print(f"  Authentication: {'Connected' if self.logged_in else 'Not connected'}")
            print(f"  Default Format: {self.output_format}")
            print(f"  Debug Mode: {self.debug_mode}")
        print()

    def do_exit(self, line: str):
        """Exit the interactive shell"""
        if Colors.supports_color():
            print(f"{Colors.DIM}Goodbye!{Colors.RESET}")
        else:
            print("Goodbye!")
        return True

    def do_quit(self, line: str):
        """Exit the interactive shell"""
        return self.do_exit(line)

    def do_EOF(self, line: str):
        """Handle Ctrl+D"""
        print()  # New line after ^D
        return self.do_exit(line)

    def help_vessel(self):
        """Help for vessel command"""
        if Colors.supports_color():
            print(f"""
{Colors.DIM_CYAN}vessel{Colors.RESET} - Get comprehensive vessel information

{Colors.DIM}Usage:{Colors.RESET}
  vessel /imo <IMO_NUMBER> [/format table|json|csv] [/output filename]

{Colors.DIM}Examples:{Colors.RESET}
  vessel /imo 9074729
  vessel /imo 8515128 /format json
  vessel /imo 9074729 /output vessel_data.json

{Colors.DIM}Parameters:{Colors.RESET}
  /imo      IMO number (required)
  /format   Output format: table, json, csv (optional)
  /output   Save to file or specify format (optional)
""")
        else:
            print("""
vessel - Get comprehensive vessel information

Usage:
  vessel /imo <IMO_NUMBER> [/format table|json|csv] [/output filename]

Examples:
  vessel /imo 9074729
  vessel /imo 8515128 /format json
  vessel /imo 9074729 /output vessel_data.json

Parameters:
  /imo      IMO number (required)
  /format   Output format: table, json, csv (optional)
  /output   Save to file or specify format (optional)
""")

    def help_search(self):
        """Help for search command"""
        if Colors.supports_color():
            print(f"""
{Colors.DIM_CYAN}search{Colors.RESET} - Search for vessels by name

{Colors.DIM}Usage:{Colors.RESET}
  search /name "<VESSEL_NAME>" [/format table|json|csv]

{Colors.DIM}Examples:{Colors.RESET}
  search /name "MAERSK"
  search /name "EVER GIVEN" /format json

{Colors.DIM}Parameters:{Colors.RESET}
  /name     Vessel name to search for (required)
  /format   Output format: table, json, csv (optional)
""")
        else:
            print("""
search - Search for vessels by name

Usage:
  search /name "<VESSEL_NAME>" [/format table|json|csv]

Examples:
  search /name "MAERSK"
  search /name "EVER GIVEN" /format json

Parameters:
  /name     Vessel name to search for (required)
  /format   Output format: table, json, csv (optional)
""")

    def help_fleet(self):
        """Help for fleet command"""
        if Colors.supports_color():
            print(f"""
{Colors.DIM_CYAN}fleet{Colors.RESET} - Get fleet information for a company

{Colors.DIM}Usage:{Colors.RESET}
  fleet /company "<COMPANY_NAME>" [/format table|json|csv]

{Colors.DIM}Examples:{Colors.RESET}
  fleet /company "MAERSK LINE"
  fleet /company "MSC" /format json

{Colors.DIM}Parameters:{Colors.RESET}
  /company  Company name (required)
  /format   Output format: table, json, csv (optional)
""")
        else:
            print("""
fleet - Get fleet information for a company

Usage:
  fleet /company "<COMPANY_NAME>" [/format table|json|csv]

Examples:
  fleet /company "MAERSK LINE"
  fleet /company "MSC" /format json

Parameters:
  /company  Company name (required)
  /format   Output format: table, json, csv (optional)
""")

    def default(self, line):
        """Handle unknown commands"""
        if Colors.supports_color():
            print(f"{Colors.DIM_RED}Unknown command: {line.split()[0]}{Colors.RESET}")
            print(f"{Colors.DIM}Type 'help' for available commands{Colors.RESET}")
        else:
            print(f"Unknown command: {line.split()[0]}")
            print("Type 'help' for available commands")
        print()