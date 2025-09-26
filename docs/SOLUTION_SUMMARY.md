# Equasis Comprehensive Parsing Solution

## Overview
After analyzing the Equasis HTML structure for the vessel ALMAHER (IMO 8515128), I've created a comprehensive parser that can extract information from all three tabs and the common vessel information section.

## Key Discoveries

### 1. **Tab Structure**
The Equasis vessel page has three main tabs that are loaded dynamically:
- **Ship Info**: Contains overview, management details, classification, and geographical information
- **Inspections**: Contains Port State Control inspection records
- **Ship History**: Contains historical names, flags, and company management

### 2. **Common Information Section**
The `<!-- infoship -->` section appears on ALL tabs and contains the basic vessel information:
- Vessel Name: **ALMAHER**
- IMO Number: 8515128
- Flag: St. Kitts and Nevis
- Call Sign: V4FN6
- MMSI: 341787001
- Gross Tonnage: 1792
- DWT: 964
- Type: Passenger/Ro-Ro Ship (vehicles)
- Year Built: 1986
- Status: In Service/Commission

### 3. **HTML Structure Patterns**

#### Basic Vessel Info Pattern
```html
<h4 class="color-gris-bleu-copyright">
    <b>ALMAHER</b>
    &nbsp;-&nbsp; IMO n° &nbsp;<b>8515128</b>
</h4>
```

#### Field Pattern
```html
<div class="row">
    <div class="col-lg-4 col-md-4 col-sm-6 col-xs-6">
        <b>Flag</b>
    </div>
    <div class="col-lg-4 col-md-4 col-sm-6 col-xs-6">
        [Flag Image]
    </div>
    <div class="col-lg-4 col-md-4 col-sm-6 col-xs-6">
        (St.Kitts and Nevis)
    </div>
</div>
```

## Data Extracted from Each Tab

### Ship Info Tab
1. **Overview Section**
   - Flag Performance (Paris MOU: Black, Tokyo MOU: Black)
   - USCG Targeting: Not targeted

2. **Management Details**
   - AL JADARA MEMIZA (Ship manager/Commercial manager, Registered owner)
   - UNKNOWN (ISM Manager)

3. **Classification**
   - International Register of Shipping (IS) - Withdrawn during 04/2025

4. **Geographical Information**
   - Recent locations (September 2025: South Asia, etc.)
   - Historical tracking back to 2013

### Inspections Tab
- Port State Control inspections
- Example: 03/04/2009 inspection by Tokyo MoU (No detention)

### Ship History Tab
1. **Historical Names**
   - ALMAHER (since 01/07/2024)
   - St. Anthony de Padua (since 01/08/2012)
   - Cebu Ferry 2 (since 01/04/2009)

2. **Historical Flags**
   - St. Kitts and Nevis (since 01/07/2024)
   - Philippines (since 01/10/2009)

3. **Historical Companies**
   - AL JADARA MEMIZA (current)
   - 2GO GROUP INC (during 04/2009)

## Implementation

### Parser Features
The `equasis_comprehensive_parser.py` provides:

1. **Structured Data Classes**
   - `VesselBasicInfo`: Core vessel identification
   - `CompanyInfo`: Management companies
   - `InspectionInfo`: PSC inspection records
   - `HistoricalName/Flag/Company`: Historical data
   - `EquasisVesselData`: Complete vessel profile

2. **Tab-Aware Parsing**
   ```python
   parser = EquasisParser()
   vessel_data = parser.parse_html(html, tab="ship_info")
   ```

3. **Robust Extraction Methods**
   - Handles Bootstrap grid layouts
   - Extracts from tables and div structures
   - Parses collapsible sections
   - Handles mobile and desktop layouts

## Programmatic Access Strategy

To get complete vessel information from Equasis programmatically:

1. **Login to Equasis**
   ```python
   session = requests.Session()
   # Login with credentials
   ```

2. **Navigate to Vessel Page**
   ```python
   # Search for vessel by IMO
   vessel_url = f"https://www.equasis.org/EquasisWeb/restricted/ShipInfo?fs=ShipInfo&P_IMO={imo}"
   ```

3. **Fetch Each Tab**
   ```python
   # Ship Info (default)
   ship_info_html = session.get(vessel_url).text
   
   # Inspections
   inspections_url = f"...ShipInspection?fs=ShipInfo&P_IMO={imo}"
   inspections_html = session.get(inspections_url).text
   
   # Ship History
   history_url = f"...ShipHistory?fs=ShipInfo&P_IMO={imo}"
   history_html = session.get(history_url).text
   ```

4. **Parse Each Response**
   ```python
   parser = EquasisParser()
   
   # Parse each tab
   ship_info_data = parser.parse_html(ship_info_html, "ship_info")
   inspections_data = parser.parse_html(inspections_html, "inspections")
   history_data = parser.parse_html(history_html, "ship_history")
   
   # Combine data
   complete_vessel = merge_vessel_data(ship_info_data, inspections_data, history_data)
   ```

## Key Insights

1. **Tab Navigation via Form Submission**
   - Tabs are not AJAX-loaded; they're separate page requests
   - Each tab uses JavaScript form submission: `document.formOngletShip.submit()`
   - Actions: 'ShipInfo', 'ShipInspection', 'ShipHistory'

2. **Consistent Structure**
   - All tabs share the same basic vessel info section
   - Bootstrap responsive design with desktop/mobile variants
   - Collapsible sections using Bootstrap collapse

3. **Data Completeness**
   - To get ALL vessel data, you must fetch all three tabs
   - Each tab contains unique information not available in others
   - The infoship section provides core identification on every page

## Usage Example

```python
from equasis_comprehensive_parser import EquasisParser
import json

# Initialize parser
parser = EquasisParser()

# Parse HTML from Equasis
with open('vessel_page.html', 'r') as f:
    html = f.read()

# Parse vessel data
vessel_data = parser.parse_html(html, tab="ship_info")

# Access structured data
print(f"Vessel: {vessel_data.basic_info.name}")
print(f"IMO: {vessel_data.basic_info.imo}")
print(f"Flag: {vessel_data.basic_info.flag}")

# Export to JSON
vessel_dict = {
    'basic_info': asdict(vessel_data.basic_info),
    'management': [asdict(c) for c in vessel_data.management],
    'inspections': [asdict(i) for i in vessel_data.inspections],
    # ... etc
}

with open('vessel_data.json', 'w') as f:
    json.dump(vessel_dict, f, indent=2)
```

## Files Created

1. **equasis_comprehensive_parser.py**: Complete parser implementation
2. **parsed_vessel_data.json**: Extracted vessel data in JSON format
3. **test_equasis_parser.py**: Standalone test script
4. **equasis_cli_v2.py**: Updated CLI tool with fixed parsing

This comprehensive solution allows you to programmatically extract ALL information from Equasis vessel pages, handling the complex HTML structure and multi-tab layout effectively.
