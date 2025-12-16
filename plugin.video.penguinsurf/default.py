# -*- coding: utf-8 -*-
# Module: default
# Author: Manus
# Created: 2025-12-16
# License: GPL-3.0-or-later

import sys
import xbmcaddon
import xbmcplugin
import xbmcgui
import urllib.parse
import xbmc
from . import scraper

# Get the plugin url in proper encoding
__url__ = sys.argv[0]
# Get the plugin handle as an integer number
__handle__ = int(sys.argv[1])

# Get addon info
ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
ADDON_NAME = ADDON.getAddonInfo('name')
ADDON_VERSION = ADDON.getAddonInfo('version')
ADDON_PATH = ADDON.getAddonInfo('path')

def get_url(**kwargs):
    """
    Create a URL for calling the plugin recursively from the Kodi interface.
    :param kwargs: keyword arguments to be passed as URL parameters
    :return: plugin URL
    :rtype: str
    """
    return '{0}?{1}'.format(__url__, urllib.parse.urlencode(kwargs))

def list_root_menu():
    """
    Create the main menu for the addon.
    """
    # The Crew features include: Movies, TV Shows, Sports, IPTV, Kids, Collections, Tools
    # We will start with the core features: Movies and TV Shows
    
    # Movies
    list_item = xbmcgui.ListItem('Movies')
    list_item.setArt({'icon': 'DefaultVideo.png'})
    url = get_url(action='list_movies')
    xbmcplugin.addDirectoryItem(__handle__, url, list_item, isFolder=True)

    # TV Shows
    list_item = xbmcgui.ListItem('TV Shows')
    list_item.setArt({'icon': 'DefaultVideo.png'})
    url = get_url(action='list_tvshows')
    xbmcplugin.addDirectoryItem(__handle__, url, list_item, isFolder=True)

    # Add-on Settings
    list_item = xbmcgui.ListItem('Settings')
    list_item.setArt({'icon': 'DefaultAddon.png'})
    list_item.setProperty('IsPlayable', 'false')
    xbmcplugin.addDirectoryItem(__handle__, 'plugin://{0}/settings'.format(ADDON_ID), list_item, isFolder=False)

    # End of the list
    xbmcplugin.endOfDirectory(__handle__)

def list_movies():
    """
    Placeholder for listing movie categories/genres.
    """
    # Example categories
    categories = [
        ('Popular Movies', 'popular'),
        ('Trending Movies', 'trending'),
        ('In Theaters', 'intheatres'),
        ('Genres', 'genres')
    ]

    for title, slug in categories:
        list_item = xbmcgui.ListItem(title)
        list_item.setArt({'icon': 'DefaultVideo.png'})
        url = get_url(action='list_items', category='movies', subcategory=slug)
        xbmcplugin.addDirectoryItem(__handle__, url, list_item, isFolder=True)

    xbmcplugin.endOfDirectory(__handle__)

def list_tvshows():
    """
    Placeholder for listing TV show categories/genres.
    """
    # Example categories
    categories = [
        ('Popular TV Shows', 'popular'),
        ('Trending TV Shows', 'trending'),
        ('Airing Today', 'airingtoday'),
        ('Genres', 'genres')
    ]

    for title, slug in categories:
        list_item = xbmcgui.ListItem(title)
        list_item.setArt({'icon': 'DefaultVideo.png'})
        url = get_url(action='list_items', category='tvshows', subcategory=slug)
        xbmcplugin.addDirectoryItem(__handle__, url, list_item, isFolder=True)

    xbmcplugin.endOfDirectory(__handle__)

def list_items(category, subcategory):
    """
    Lists actual movies or TV shows based on category and subcategory.
    """
    xbmc.log(f"Listing items for category: {category}, subcategory: {subcategory}", xbmc.LOGINFO)

    if category == 'movies':
        # For now, we only implement the 'popular' subcategory
        if subcategory == 'popular':
            data = scraper.get_popular_movies()
            items = data.get('results', [])
            
            for item in items:
                title = item.get('title')
                item_id = item.get('id')
                plot = item.get('overview')
                poster = scraper.TMDB_IMAGE_BASE_URL + item.get('poster_path', '')
                
                list_item = xbmcgui.ListItem(title)
                list_item.setArt({'icon': poster, 'thumb': poster})
                list_item.setInfo('video', {'title': title, 'plot': plot, 'mediatype': 'movie'})
                
                # The URL for a playable item will point to the resolve_item action
                url = get_url(action='resolve_item', item_id=item_id, item_type='movie', title=title)
                xbmcplugin.addDirectoryItem(__handle__, url, list_item, isFolder=False)
        else:
            # Placeholder for other movie subcategories
            list_item = xbmcgui.ListItem(f'Placeholder for {subcategory} Movies')
            xbmcplugin.addDirectoryItem(__handle__, get_url(), list_item, isFolder=False)

    elif category == 'tvshows':
        # For now, we only implement the 'popular' subcategory
        if subcategory == 'popular':
            data = scraper.get_popular_tvshows()
            items = data.get('results', [])
            
            for item in items:
                title = item.get('name')
                item_id = item.get('id')
                plot = item.get('overview')
                poster = scraper.TMDB_IMAGE_BASE_URL + item.get('poster_path', '')
                
                list_item = xbmcgui.ListItem(title)
                list_item.setArt({'icon': poster, 'thumb': poster})
                list_item.setInfo('video', {'title': title, 'plot': plot, 'mediatype': 'tvshow'})
                
                # The URL for a playable item will point to the resolve_item action
                url = get_url(action='resolve_item', item_id=item_id, item_type='tvshow', title=title)
                xbmcplugin.addDirectoryItem(__handle__, url, list_item, isFolder=False)
        else:
            # Placeholder for other TV show subcategories
            list_item = xbmcgui.ListItem(f'Placeholder for {subcategory} TV Shows')
            xbmcplugin.addDirectoryItem(__handle__, get_url(), list_item, isFolder=False)

    xbmcplugin.endOfDirectory(__handle__)

def resolve_item(item_id, item_type, title):
    """
    Resolves the stream URL for a selected item.
    """
    xbmc.log(f"Resolving stream for {item_type} ID: {item_id}, Title: {title}", xbmc.LOGINFO)
    
    # Use the scraper to find a stream URL
    stream_url = scraper.resolve_stream_url(title)
    
    if stream_url:
        xbmc.log(f"Stream found: {stream_url}", xbmc.LOGINFO)
        # Create a list item with the stream URL
        list_item = xbmcgui.ListItem(path=stream_url)
        # Set the item as playable
        xbmcplugin.setResolvedUrl(__handle__, True, list_item)
    else:
        xbmc.log("No stream found.", xbmc.LOGWARNING)
        # Show a notification if no stream is found
        xbmcgui.Dialog().notification(ADDON_NAME, f'No stream found for {title}.', xbmcgui.NOTIFICATION_INFO, 5000)
        # Must call setResolvedUrl with success=False to prevent Kodi from hanging
        xbmcplugin.setResolvedUrl(__handle__, False, xbmcgui.ListItem())

# The 



def router(paramstring):
    """
    Router function that calls the appropriate action function.
    :param paramstring: URL parameter string
    :type paramstring: str
    """
    # Parse a URL-encoded paramstring to a dictionary.
    params = dict(urllib.parse.parse_qsl(paramstring))
    
    # Check the action parameter to determine which function to call
    action = params.get('action')

    if action is None:
        # Default action is to list the root menu
        list_root_menu()
    elif action == 'list_movies':
        list_movies()
    elif action == 'list_tvshows':
        list_tvshows()
    elif action == 'list_items':
        category = params.get('category')
        subcategory = params.get('subcategory')
        if category and subcategory:
            list_items(category, subcategory)
    elif action == 'resolve_item':
        item_id = params.get('item_id')
        item_type = params.get('item_type')
        title = params.get('title')
        if item_id and item_type and title:
            resolve_item(item_id, item_type, title)
    else:
        # Unknown action
        xbmcgui.Dialog().notification(ADDON_NAME, 'Unknown action: {0}'.format(action), xbmcgui.NOTIFICATION_ERROR, 5000)

if __name__ == '__main__':
    router(sys.argv[2][1:])
