# Equasis CLI Tool

A comprehensive command-line interface for accessing Equasis maritime intelligence. This professional-grade tool provides complete vessel profiles with management details, inspection history, and ownership tracking through a clean, scriptable CLI.

> **🚢 Major Update**: Now provides comprehensive vessel intelligence with 50+ data points including management companies, PSC inspections, historical names/flags, and classification details - all collected automatically from multiple Equasis tabs.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Output Formats](#output-formats)
- [Examples](#examples)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [Legal and Compliance](#legal-and-compliance)
- [Contributing](#contributing)
- [License](#license)

## Overview

Equasis CLI Tool is a Python-based command-line application that interfaces with the Equasis maritime database to retrieve vessel and fleet information. Unlike web-based tools, this CLI provides:

- Fast, scriptable access to maritime data
- Multiple output formats (table, JSON, CSV)
- Batch processing capabilities
- Integration with automation workflows
- Clean separation from GUI dependencies

## Features

### Current Features

#### Core Vessel Intelligence
- **Comprehensive Vessel Lookup**: Get complete vessel profiles with 50+ data points from multiple Equasis tabs
- **3-Tab Data Collection**: Automatically fetches Ship Info, Inspections, and Ship History data
- **Management Company Details**: Current and historical management with roles and dates
- **PSC Inspection History**: Port State Control inspections with detention records
- **Historical Vessel Data**: Name changes, flag changes, and ownership history over time
- **Classification Society Info**: Current and historical classification with status
- **Geographical Tracking**: Vessel location history and movement patterns
- **Flag Performance**: Paris MOU and Tokyo MOU ratings, USCG targeting status

#### Search & Fleet Operations
- **Vessel Search by IMO**: Look up comprehensive vessel information using IMO numbers
- **Vessel Search by Name**: Search for vessels using partial or complete names
- **Fleet Information**: Retrieve fleet data for shipping companies

#### Technical Features
- **Professional Package Structure**: Modular architecture ready for distribution (Homebrew, PyPI)
- **Multiple Output Formats**: Export data as formatted tables, structured JSON, or CSV
- **File Output**: Save results directly to files
- **Session Management**: Automatic login and session handling with error recovery
- **Rate Limiting**: Built-in delays to respect server resources (1-second intervals)
- **Environment Variables**: Secure credential management via .env files
- **Comprehensive Logging**: Debug and monitor operations with detailed logging

### Planned Features

#### Near-Term Enhancements
- **Batch Processing**: Process multiple IMO numbers efficiently
- **Data Caching**: Reduce redundant API calls with intelligent caching
- **Enhanced Search/Fleet Parsing**: Apply comprehensive parsing to search results
- **Progress Indicators**: Visual feedback for long operations
- **Configuration Files**: User preferences and custom settings

#### Medium-Term Goals
- **Homebrew Distribution**: Native macOS installation via `brew install equasis-cli`
- **Additional Maritime Data**: Integration with other vessel databases
- **Export Formats**: Excel, PDF reports, specialized maritime formats
- **Vessel Analytics**: Risk assessment and compliance scoring
- **Fleet Intelligence**: Company-wide vessel analysis and reporting

#### Advanced Features
- **Maritime Intelligence Platform**: Beyond basic vessel lookup
- **API Service**: RESTful API for integration with other maritime tools
- **Visualization**: Charts and graphs for historical vessel data
- **Automated Monitoring**: Alerts for vessel status changes

## Prerequisites

- **Python 3.7+**: Required for modern features and type hints
- **Equasis Account**: Valid username and password from equasis.org
- **Internet Connection**: Required for accessing Equasis servers

### System Requirements

- macOS, Linux, or Windows
- 50MB disk space for virtual environment
- Stable internet connection

## Installation

### Prerequisites

- **pipx**: Recommended for isolated installation of Python CLI tools
- **Python 3.7+**: Required for the application
- **Git** (optional): For cloning the repository

### Install pipx (if not already installed)

```bash
# On macOS with Homebrew
brew install pipx

# On other systems, use pip
python3 -m pip install --user pipx

# Add pipx to PATH
pipx ensurepath

# Restart your terminal or run:
source ~/.zshrc  # or ~/.bashrc
```

### Install Equasis CLI

#### Option 1: Install from Source (Recommended for Development)

```bash
# Clone or download the project
cd ~/Projects/  # or your preferred location
git clone <repository-url> equasis-cli  # or download and extract
cd equasis-cli

# Install with pipx in editable mode
pipx install -e .

# Verify installation
equasis --help
```

#### Option 2: Install from Git (if available)

```bash
# Install directly from repository
pipx install git+<repository-url>
```

#### Option 3: Traditional Virtual Environment (Alternative)

If you prefer not to use pipx:

```bash
cd ~/Projects/equasis-cli

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .

# Note: You'll need to activate the venv each time you use the tool
```

## Configuration

### Environment Variables (Recommended)

Create a `.env` file in your project directory (if installed from source):

```bash
# Navigate to project directory (only needed for source installation)
cd ~/Projects/equasis-cli

# Create .env file from template
cp .env.example .env

# Edit with your credentials
nano .env  # or code .env, vim .env, etc.
```

Add your Equasis credentials:

```bash
EQUASIS_USERNAME=your_username_here
EQUASIS_PASSWORD=your_password_here
```

### Alternative: Command Line Arguments

You can also pass credentials directly:

```bash
equasis --username your_user --password your_pass vessel --imo 9074729
```

### Security Best Practices

1. **Never commit credentials**: Ensure `.env` is in your `.gitignore`
2. **Use environment variables**: Avoid passing credentials on command line in shared environments
3. **Limit file permissions**: `chmod 600 .env` (read/write for owner only)

## Usage

The tool is available globally after installation via pipx. No need to activate virtual environments or navigate to specific directories.

### Basic Syntax

```bash
equasis [global_options] command [command_options]
```

### Global Options

- `--username USERNAME`: Equasis username (optional if set in .env)
- `--password PASSWORD`: Equasis password (optional if set in .env)
- `--output FORMAT`: Output format (table, json, csv) - default: table
- `--output-file FILE`: Save output to file instead of printing

### Tab Completion

The tool includes comprehensive tab completion for zsh with intelligent suggestions and examples.

**Completion Features:**

- **Commands**: `equasis <TAB>` shows available commands with descriptions
- **Command-specific options**: `equasis vessel <TAB>` shows only vessel-related options
- **Output formats**: `equasis --output <TAB>` shows format options with descriptions
- **Real examples**: Completion provides actual IMO numbers, vessel names, and company names
- **Context-aware**: Different completions for different commands

**What you can complete:**

- Commands: `vessel`, `search`, `fleet`
- Global options: `--username`, `--password`, `--output`, `--output-file`, `--help`
- Output formats: `table`, `json`, `csv` (with descriptions)
- Example IMO numbers: Real vessels like EVER GIVEN (9074729)
- Example vessel names: "EVER GIVEN", "MAERSK", "COSCO", etc.
- Major shipping companies: "MAERSK LINE", "MSC", "COSCO SHIPPING", etc.

**Setting up tab completion:**

1. **Ensure completion directory exists:**

   ```bash
   mkdir -p ~/.zsh/completions
   ```

2. **Copy completion script** (if installed from source):

   ```bash
   cp ~/Projects/equasis-cli/completions/equasis_completion.zsh ~/.zsh/completions/_equasis
   ```

3. **Add to .zshrc** (if not already present):

   ```bash
   echo 'fpath=(~/.zsh/completions $fpath)' >> ~/.zshrc
   echo 'autoload -Uz compinit && compinit' >> ~/.zshrc
   ```

4. **Reload shell:**
   ```bash
   source ~/.zshrc
   ```

**Usage tips:**

- Always add a space before pressing TAB: `equasis vessel --imo <TAB>` (not `equasis vessel --imo<TAB>`)
- Use TAB at any point to see available options
- Select from examples or type your own values
- Descriptions help you understand what each option does

### Commands

#### vessel

Get detailed information for a specific vessel by IMO number.

```bash
equasis vessel --imo IMO_NUMBER
```

**Options:**

- `--imo IMO_NUMBER`: Required. The IMO number of the vessel

#### search

Search for vessels by name (partial matches supported).

```bash
equasis search --name VESSEL_NAME
```

**Options:**

- `--name VESSEL_NAME`: Required. Full or partial vessel name

#### fleet

Get fleet information for a shipping company.

```bash
equasis fleet --company COMPANY_NAME
```

**Options:**

- `--company COMPANY_NAME`: Required. Company name or identifier

## Output Formats

### Table Format (Default) - Comprehensive Intelligence

Human-readable formatted output with comprehensive vessel intelligence.

```
Vessel Information (Comprehensive):
===================================
IMO Number:    8515128
Name:          ALMAHER
Flag:          St.Kitts and Nevis (KNA)
Call Sign:     V4FN6
MMSI:          341787001
Type:          Passenger/Ro-Ro Ship (vehicles)
Gross Tonnage: 1792
DWT:           964
Year Built:    1986
Status:        In Service/Commission
Last Update:   02/07/2025

Management Companies (3):
------------------------------
• AL JADARA MEMIZA (Ship manager/Commercial manager)
• AL JADARA MEMIZA (Registered owner)
• UNKNOWN (ISM Manager)

Classification (1):
----------------
• International Register of Shipping (IS) - Withdrawn

Recent PSC Inspections (1 of 1):
-----------------------------------
• 03/04/2009: Tokyo MoU
  ⚠️  Detention: N

Historical Names (3 total):
----------------------
• ALMAHER (since 01/07/2024)
• St. Anthony de Padua (since 01/08/2012)
• Cebu Ferry 2 (since 01/04/2009)
```

### JSON Format - Rich Nested Structure

Structured data with comprehensive vessel intelligence for programmatic processing.

```json
{
  "basic_info": {
    "imo": "8515128",
    "name": "ALMAHER",
    "flag": "St.Kitts and Nevis",
    "flag_code": "KNA",
    "call_sign": "V4FN6",
    "mmsi": "341787001",
    "vessel_type": "Passenger/Ro-Ro Ship (vehicles)",
    "gross_tonnage": "1792",
    "dwt": "964",
    "year_built": "1986",
    "status": "In Service/Commission",
    "last_update": "02/07/2025"
  },
  "management": [
    {
      "name": "AL JADARA MEMIZA",
      "role": "Ship manager/Commercial manager",
      "imo": "0050002",
      "date_effect": "since 01/07/2024"
    }
  ],
  "inspections": [
    {
      "date": "03/04/2009",
      "psc_organization": "Tokyo MoU",
      "detention": "N",
      "authority": "Japan",
      "port": "Osaka"
    }
  ],
  "historical_names": [
    {
      "name": "ALMAHER",
      "date_effect": "since 01/07/2024",
      "source": "Equasis"
    }
  ]
}
```

### CSV Format

Basic CSV format for spreadsheet compatibility (basic fields only).

```csv
8515128,ALMAHER,St.Kitts and Nevis,Passenger/Ro-Ro Ship,964,1792,1986
```

## Examples

### Comprehensive Vessel Lookup

Get complete vessel intelligence with management, inspections, and history:

```bash
# Using environment variables for credentials (recommended)
equasis vessel --imo 8515128

# Using command-line credentials
equasis --username myuser --password mypass vessel --imo 8515128

# Use tab completion for IMO examples
equasis vessel --imo <TAB>  # Shows real vessel examples like EVER GIVEN

# Get comprehensive data in JSON format
equasis --output json vessel --imo 8515128

# Save comprehensive report to file
equasis --output json --output-file vessel_intelligence.json vessel --imo 8515128
```

**What you get**: Complete vessel profile including management companies, PSC inspection history, historical names/flags, classification details, and geographical tracking - all from a single command!

### Search by Name

```bash
# Search for vessels with "MAERSK" in the name
equasis search --name "MAERSK"

# Use tab completion for vessel name examples
equasis search --name <TAB>  # Shows examples like "EVER GIVEN", "MAERSK"

# Partial name search
equasis search --name "EVER"
```

### Fleet Information

```bash
# Get fleet information for a company
equasis fleet --company "MAERSK LINE"

# Use tab completion for company examples
equasis fleet --company <TAB>  # Shows major shipping companies
```

### Tab Completion Examples

```bash
# Complete commands
equasis <TAB>                    # Shows: vessel, search, fleet

# Complete command-specific options
equasis vessel <TAB>             # Shows: --imo, --help, --username, etc.
equasis search <TAB>             # Shows: --name, --help, --username, etc.

# Complete with real examples
equasis vessel --imo <TAB>       # Shows real IMO numbers with vessel names
equasis fleet --company <TAB>    # Shows major shipping companies

# Complete output formats with descriptions
equasis --output <TAB>           # Shows: table, json, csv with descriptions
```

### Different Output Formats

```bash
# JSON output
equasis --output json vessel --imo 9074729

# CSV output
equasis --output csv vessel --imo 9074729

# Save to file
equasis --output json --output-file vessel_data.json vessel --imo 9074729
```

### Batch Processing

```bash
# Process multiple IMO numbers from a file
while read imo; do
    echo "Processing IMO: $imo"
    equasis vessel --imo "$imo" --output csv >> vessels.csv
    sleep 2  # Be respectful to the server
done < imo_list.txt
```

### Integration with Other Tools

```bash
# Use with jq for JSON processing
equasis --output json vessel --imo 9074729 | jq '.name'

# Pipe to grep for filtering
equasis search --name "CONTAINER" | grep "Singapore"

# Count results
equasis search --name "MAERSK" --output csv | wc -l

# Use tab completion with pipes
equasis vessel --imo <TAB>  # Select example, then continue with pipe
equasis vessel --imo 9074729 | head -5
```

## Architecture & Data Collection

### Comprehensive Intelligence Strategy

The Equasis CLI uses a **3-request multi-tab strategy** to collect comprehensive vessel data:

1. **Ship Info Tab**: Management, classification, geographical data
2. **Inspections Tab**: PSC inspection history and detention records
3. **Ship History Tab**: Historical names, flags, and ownership changes

Each vessel lookup automatically:
- Authenticates with Equasis using your credentials
- Makes 3 targeted requests to different Equasis tabs
- Parses rich HTML data structures from each tab
- Merges all data into a comprehensive vessel profile
- Formats output with smart summarization

### Data Architecture

```
Single IMO Request → 3 Parallel Tab Requests → Comprehensive Profile

┌─────────────────┐    ┌──────────────┐    ┌─────────────────────┐
│  Ship Info Tab  │    │Inspections   │    │  Ship History Tab   │
│                 │    │Tab           │    │                     │
│ • Management    │    │              │    │ • Historical Names  │
│ • Classification│ → │ • PSC Records│ → │ • Historical Flags  │
│ • Geographical  │    │ • Detentions │    │ • Historical Owners │
│ • Flag Performance│    │ • Authorities│    │ • Name Changes     │
└─────────────────┘    └──────────────┘    └─────────────────────┘
         ↓                       ↓                        ↓
         └─────────────── Merge Data ──────────────┘
                              ↓
                    ┌─────────────────────┐
                    │ Complete Vessel     │
                    │ Intelligence Profile│
                    │                     │
                    │ 50+ Data Points     │
                    │ Across 9 Categories │
                    └─────────────────────┘
```

### Professional Package Structure

```
equasis-cli/
├── equasis_cli/              # Main package
│   ├── __init__.py          # Package initialization
│   ├── main.py              # CLI interface & argument parsing
│   ├── client.py            # EquasisClient & authentication
│   ├── parser.py            # HTML parser & data structures
│   └── formatter.py         # Output formatting
├── setup.py                 # Package distribution config
├── requirements.txt         # Dependencies
├── completions/             # Tab completion
│   └── equasis_completion.zsh
├── old_files/              # Backup of original code
└── .env                    # Credentials (not in git)
```

## Development

### Updated Project Structure

The tool now uses a professional package structure:

```
equasis-cli/
├── equasis_cli/                    # Main package directory
│   ├── __init__.py                # Package initialization & public API
│   ├── main.py                    # CLI interface & argument parsing
│   ├── client.py                  # EquasisClient & web scraping
│   ├── parser.py                  # Comprehensive HTML parser
│   └── formatter.py               # Output formatting (table/JSON/CSV)
├── setup.py                       # Package distribution configuration
├── requirements.txt               # Python dependencies
├── completions/                   # Tab completion scripts
│   └── equasis_completion.zsh     # Zsh completion (unchanged)
├── local/                         # Development and archive files
│   ├── archive/                   # Original monolithic code backup
│   ├── development/               # Intermediate development versions
│   └── debug/                     # HTML debug files and analysis tools
├── .env                          # Environment variables (not in git)
├── .env.example                  # Environment template
├── SESSION_SUMMARY.md            # Development session documentation
├── SOLUTION_SUMMARY.md           # Technical implementation notes
├── README.md                     # This file
└── MANIFEST.in                   # Package manifest
```

### Setting Up Development Environment

```bash
# Clone or download the project
cd ~/Projects/
git clone <repository-url> equasis-cli  # or create directory manually
cd equasis-cli

# Install in editable mode with pipx (recommended)
pipx install -e .

# Or use traditional virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

### Making Changes

With the new package structure, changes to individual modules are automatically available with pipx editable installation:

```bash
# Code changes in equasis_cli/*.py files (automatic)
# No action needed - changes are immediately available

# After modifying setup.py, requirements.txt, or package structure
cd ~/Projects/equasis-cli
pipx install -e . --force

# Alternative: upgrade command
pipx upgrade equasis-cli
```

### Module-Specific Development

```bash
# Test individual components
cd ~/Projects/equasis-cli

# Test parser independently
python3 -c "from equasis_cli.parser import EquasisParser; print('Parser loaded successfully')"

# Test client authentication
python3 -c "from equasis_cli.client import EquasisClient; print('Client loaded successfully')"

# Test output formatting
python3 -c "from equasis_cli.formatter import OutputFormatter; print('Formatter loaded successfully')"
```

### Package Management

```bash
# List installed pipx packages
pipx list

# Show package details
pipx list --include-deps

# Uninstall if needed
pipx uninstall equasis-cli

# Reinstall from scratch
pipx install -e . --force
```

### Debugging

Enable debug logging by modifying the logging level:

```python
logging.basicConfig(level=logging.DEBUG)
```

Or set environment variable:

```bash
export PYTHONPATH=$(pwd)
python3 -c "import logging; logging.basicConfig(level=logging.DEBUG)" equasis_cli.py vessel --imo 9074729
```

### Testing HTML Parsing

Since Equasis HTML structure may change, you can test parsing with saved HTML:

```python
def test_parsing():
    with open('sample_vessel_page.html', 'r') as f:
        html = f.read()

    # Import the client class
    from equasis_cli import EquasisClient

    client = EquasisClient('', '')
    result = client._parse_vessel_info(html, '1234567')
    print(result)

if __name__ == '__main__':
    test_parsing()
```

### Extending Functionality

The modular design makes it easy to add features:

1. **Add new search types**: Extend the argument parser and add methods to `EquasisClient`
2. **Create new formatters**: Add methods to `OutputFormatter` class
3. **Add data validation**: Create validation functions for input data
4. **Implement caching**: Add caching layer to reduce redundant requests

## Troubleshooting

### Common Issues

#### Command Not Found

```
zsh: command not found: equasis
```

**Solutions:**

1. Ensure pipx installation was successful: `pipx list`
2. Check that pipx is in your PATH: `pipx ensurepath` then restart terminal
3. Verify the package is installed: `pipx list | grep equasis`
4. If using virtual environment instead of pipx, ensure it's activated

#### Tab Completion Not Working

**Solutions:**

1. Ensure completion script exists: `ls ~/.zsh/completions/_equasis`
2. Check completion script is properly formatted (no syntax errors)
3. Verify your `.zshrc` has completion initialization:
   ```bash
   grep -E "(fpath|compinit)" ~/.zshrc
   ```
   Should show:
   ```bash
   fpath=(~/.zsh/completions $fpath)
   autoload -Uz compinit && compinit
   ```
4. Clear completion cache and reload:
   ```bash
   rm -f ~/.zcompdump*
   source ~/.zshrc
   ```
5. Test with a simple completion first: `equasis <TAB>`

#### Completion Shows Wrong Options

**Solutions:**

1. Ensure you're using spaces correctly: `equasis vessel --imo <TAB>` (space before TAB)
2. Clear old cached completions: `unfunction _equasis 2>/dev/null && autoload -Uz compinit && compinit`
3. Reinstall completion script: `cp ~/Projects/equasis-cli/completions/equasis_completion.zsh ~/.zsh/completions/_equasis`

#### Connection Issues

```
Error: Failed to access login page: 500
```

**Solutions:**

1. Check your internet connection
2. Verify Equasis website is accessible (equasis.org)
3. Try again later (server may be temporarily unavailable)
4. Check if you're behind a firewall or proxy

#### Parsing Errors

```
Error: No vessel found with IMO: 1234567
```

**Solutions:**

1. Verify the IMO number is correct and exists in Equasis
2. The HTML parsing may need adjustment for current Equasis structure
3. Enable debug logging to see raw HTML response
4. Check if Equasis has changed their page structure

#### Python Environment Issues

```
ModuleNotFoundError: No module named 'requests'
```

**Solutions:**

1. Ensure virtual environment is activated
2. Reinstall requirements: `pip install -r requirements.txt`
3. Check Python version compatibility

### Rate Limiting

If you encounter rate limiting:

1. Increase delay between requests in the code
2. Reduce concurrent operations
3. Implement exponential backoff
4. Consider contacting Equasis for API access

### Debug Mode

Enable comprehensive logging:

```bash
PYTHONPATH=$(pwd) python3 -c "
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
exec(open('equasis_cli.py').read())
" vessel --imo 9074729
```

## Legal and Compliance

### Terms of Service

- This tool accesses publicly available data from Equasis
- Users must comply with Equasis Terms of Service
- Respect rate limits and server resources
- Use for legitimate maritime research and safety purposes only

### Best Practices

- **Rate Limiting**: Don't overload Equasis servers
- **Data Usage**: Use retrieved data responsibly
- **Authentication**: Keep credentials secure
- **Compliance**: Follow maritime industry regulations

### Disclaimer

- This tool is for educational and research purposes
- Users are responsible for compliance with applicable laws
- No warranty is provided for data accuracy or availability
- The tool may break if Equasis changes their website structure

## Contributing

Contributions are welcome! Please follow these guidelines:

### Reporting Issues

1. Check existing issues before creating new ones
2. Provide detailed error messages and steps to reproduce
3. Include your Python version and operating system
4. Don't include credentials in issue reports

### Submitting Changes

1. Fork the repository
2. Create a feature branch
3. Make your changes with appropriate tests
4. Update documentation as needed
5. Submit a pull request with clear description

### Development Guidelines

- Follow PEP 8 style guidelines
- Add type hints for new functions
- Include docstrings for public methods
- Test changes with different Equasis data
- Update README for new features

## License

This project is licensed under the MIT License. See LICENSE file for details.

### MIT License Summary

- Free to use, modify, and distribute
- No warranty provided
- Must include original license notice
- Author not liable for damages

---

**Note**: This tool interfaces with Equasis through web scraping. The HTML parsing may need updates if Equasis changes their website structure. Users should monitor for any changes and update the parsing logic accordingly.
