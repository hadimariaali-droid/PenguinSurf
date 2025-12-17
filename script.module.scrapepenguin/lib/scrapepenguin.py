# -*- coding: utf-8 -*-
# Module: scrapepenguin
# Author: Manus
# Created: 2025-12-16
# License: GPL-3.0-or-later

from .region_free_logic import get_region_free_url, fetch_region_free_content

# Central module to be imported by all video addons
class Scraper:
    """
    Central class for all scraping and region-free operations.
    """
    
    @staticmethod
    def get_unblocked_url(url):
        """
        Returns a region-free version of the URL.
        """
        return get_region_free_url(url)

    @staticmethod
    def get_unblocked_content(url):
        """
        Fetches content from a URL, bypassing geo-restrictions.
        """
        return fetch_region_free_content(url)

    # Placeholder for other scraping methods (e.g., TMDB, Archive.org)
    # These would be implemented here and imported by the video addons.
    pass
