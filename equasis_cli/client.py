#!/usr/bin/env python3
"""
Equasis Client - Handles authentication and web scraping of Equasis website
"""

import requests
import time
import logging
from typing import Optional, List
from bs4 import BeautifulSoup
from dataclasses import dataclass

from .parser import EquasisParser, EquasisVesselData

logger = logging.getLogger(__name__)

@dataclass
class SimpleVesselInfo:
    """Simple vessel info for fleet/search operations"""
    imo: str
    name: str
    flag: str
    vessel_type: str
    dwt: Optional[str] = None
    grt: Optional[str] = None
    year_built: Optional[str] = None
    status: Optional[str] = None

@dataclass
class FleetInfo:
    """Data class for fleet information"""
    company_name: str
    vessels: List[SimpleVesselInfo]
    total_vessels: int


class EquasisClient:
    """Client for interacting with Equasis API"""

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.base_url = "https://www.equasis.org"
        self.logged_in = False
        self.comprehensive_parser = EquasisParser()

        # Set headers to mimic a real browser
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })

    def login(self) -> bool:
        """Login to Equasis"""
        try:
            # Get login page first
            login_url = f"{self.base_url}/EquasisWeb/authen/HomePage?fs=HomePage"
            response = self.session.get(login_url)

            if response.status_code != 200:
                logger.error(f"Failed to access login page: {response.status_code}")
                return False

            # Parse login form to get any hidden fields
            soup = BeautifulSoup(response.text, 'html.parser')

            # Prepare login data
            login_data = {
                'j_email': self.username,
                'j_password': self.password,
                'submit': 'Ok'
            }

            # Submit login
            response = self.session.post(login_url, data=login_data)

            # Check if login was successful (you may need to adjust this check)
            if "restricted" in response.url or "Welcome" in response.text:
                self.logged_in = True
                logger.info("Successfully logged in to Equasis")
                return True
            else:
                logger.error("Login failed - check credentials")
                return False

        except Exception as e:
            logger.error(f"Login error: {e}")
            return False

    def get_comprehensive_vessel_info(self, imo: str) -> Optional[EquasisVesselData]:
        """Get comprehensive vessel information from all tabs"""
        if not self.logged_in and not self.login():
            return None

        try:
            # URLs for the three tabs
            tab_urls = {
                'ship_info': f"{self.base_url}/EquasisWeb/restricted/ShipInfo?fs=ShipInfo&P_IMO={imo}",
                'inspections': f"{self.base_url}/EquasisWeb/restricted/ShipInspection?fs=ShipInfo&P_IMO={imo}",
                'ship_history': f"{self.base_url}/EquasisWeb/restricted/ShipHistory?fs=ShipInfo&P_IMO={imo}"
            }

            vessel_data = None

            # Fetch each tab
            for tab_name, url in tab_urls.items():
                logger.info(f"Fetching {tab_name} tab for IMO {imo}")
                response = self.session.get(url)
                time.sleep(1)  # Rate limiting

                if response.status_code == 200:
                    # Parse this tab's content
                    tab_data = self.comprehensive_parser.parse_html(response.text, tab_name)

                    if tab_data:
                        if vessel_data is None:
                            # First successful tab - use as base
                            vessel_data = tab_data
                        else:
                            # Merge data from additional tabs
                            self._merge_vessel_data(vessel_data, tab_data, tab_name)
                    else:
                        logger.warning(f"Failed to parse {tab_name} tab")
                else:
                    logger.error(f"Failed to fetch {tab_name} tab: HTTP {response.status_code}")

            return vessel_data

        except Exception as e:
            logger.error(f"Error getting comprehensive vessel info for {imo}: {e}")
            return None

    def _merge_vessel_data(self, base_data: EquasisVesselData, new_data: EquasisVesselData, tab_name: str):
        """Merge data from additional tabs into base vessel data"""
        if tab_name == 'inspections':
            base_data.inspections = new_data.inspections
        elif tab_name == 'ship_history':
            base_data.historical_names = new_data.historical_names
            base_data.historical_flags = new_data.historical_flags
            base_data.historical_companies = new_data.historical_companies
        elif tab_name == 'ship_info':
            # Update ship info specific data
            if new_data.overview:
                base_data.overview = new_data.overview
            if new_data.management:
                base_data.management = new_data.management
            if new_data.classification:
                base_data.classification = new_data.classification
            if new_data.geographical:
                base_data.geographical = new_data.geographical

    def search_vessel_by_imo(self, imo: str) -> Optional[EquasisVesselData]:
        """Search for vessel by IMO number - returns comprehensive vessel data"""
        return self.get_comprehensive_vessel_info(imo)

    def search_vessel_by_name(self, name: str) -> List[SimpleVesselInfo]:
        """Search for vessels by name"""
        if not self.logged_in and not self.login():
            return []

        try:
            search_url = f"{self.base_url}/EquasisWeb/restricted/ShipInfo?fs=ShipList"
            search_data = {
                'P_ENTSHIP': name,
                'submit': 'Search'
            }

            response = self.session.post(search_url, data=search_data)
            time.sleep(1)

            if response.status_code == 200:
                return self._parse_vessel_list(response.text)
            else:
                logger.error(f"Search failed with status code: {response.status_code}")
                return []

        except Exception as e:
            logger.error(f"Error searching vessel by name {name}: {e}")
            return []

    def get_fleet_info(self, company_identifier: str) -> Optional[FleetInfo]:
        """Get fleet information for a company"""
        if not self.logged_in and not self.login():
            return None

        try:
            # First search for company
            company_url = f"{self.base_url}/EquasisWeb/restricted/CompanyInfo?fs=ShipInfo"
            company_data = {
                'P_ENTCOMP': company_identifier,
                'submit': 'Search'
            }

            response = self.session.post(company_url, data=company_data)
            time.sleep(1)

            if response.status_code == 200:
                return self._parse_fleet_info(response.text, company_identifier)
            else:
                logger.error(f"Company search failed with status code: {response.status_code}")
                return None

        except Exception as e:
            logger.error(f"Error getting fleet info for {company_identifier}: {e}")
            return None

    def _parse_vessel_list(self, html: str) -> List[SimpleVesselInfo]:
        """Parse vessel list from search results"""
        # Similar parsing logic for multiple vessels
        # Implementation depends on HTML structure
        return []

    def _parse_fleet_info(self, html: str, company: str) -> Optional[FleetInfo]:
        """Parse fleet information from HTML"""
        # Implementation depends on HTML structure
        return None