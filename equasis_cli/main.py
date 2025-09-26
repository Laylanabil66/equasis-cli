#!/usr/bin/env python3
"""
Equasis CLI Tool - Main CLI application
Command-line interface for accessing Equasis maritime data
"""

import argparse
import os
import logging
from dotenv import load_dotenv

from .client import EquasisClient
from .formatter import OutputFormatter

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description='Equasis CLI Tool for Maritime Data')
    parser.add_argument('--username', help='Equasis username (or set EQUASIS_USERNAME env var)')
    parser.add_argument('--password', help='Equasis password (or set EQUASIS_PASSWORD env var)')
    parser.add_argument('--output', choices=['table', 'json', 'csv'], default='table', help='Output format')
    parser.add_argument('--output-file', help='Output file path (optional)')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging and save HTML responses')

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Vessel command
    vessel_parser = subparsers.add_parser('vessel', help='Get vessel information')
    vessel_parser.add_argument('--imo', required=True, help='IMO number')

    # Search command
    search_parser = subparsers.add_parser('search', help='Search vessels by name')
    search_parser.add_argument('--name', required=True, help='Vessel name')

    # Fleet command
    fleet_parser = subparsers.add_parser('fleet', help='Get fleet information')
    fleet_parser.add_argument('--company', required=True, help='Company name or identifier')

    args = parser.parse_args()

    # Set logging level based on debug flag
    if args.debug:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logger.info("Debug mode enabled")
    else:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    if not args.command:
        parser.print_help()
        return

    # Use environment variables as fallback
    username = args.username or os.getenv('EQUASIS_USERNAME')
    password = args.password or os.getenv('EQUASIS_PASSWORD')

    if not username or not password:
        print("Error: Username and password required either as arguments or environment variables")
        print("Set EQUASIS_USERNAME and EQUASIS_PASSWORD in .env file, or use --username and --password")
        return

    # Initialize client
    client = EquasisClient(username, password)
    formatter = OutputFormatter()

    try:
        if args.command == 'vessel':
            vessel = client.search_vessel_by_imo(args.imo)
            if vessel:
                output = formatter.format_vessel_info(vessel, args.output)
                if args.output_file:
                    with open(args.output_file, 'w') as f:
                        f.write(output)
                    print(f"Output saved to {args.output_file}")
                else:
                    print(output)
            else:
                print(f"No vessel found with IMO: {args.imo}")

        elif args.command == 'search':
            vessels = client.search_vessel_by_name(args.name)
            if vessels:
                output = formatter.format_simple_vessel_list(vessels, args.output)
                if args.output_file:
                    with open(args.output_file, 'w') as f:
                        f.write(output)
                    print(f"Search results saved to {args.output_file}")
                else:
                    print(output)
            else:
                print(f"No vessels found with name: {args.name}")

        elif args.command == 'fleet':
            fleet = client.get_fleet_info(args.company)
            if fleet:
                output = formatter.format_fleet_info(fleet, args.output)
                if args.output_file:
                    with open(args.output_file, 'w') as f:
                        f.write(output)
                    print(f"Fleet data saved to {args.output_file}")
                else:
                    print(output)
            else:
                print(f"No fleet found for company: {args.company}")

    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")


if __name__ == '__main__':
    main()