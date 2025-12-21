"""Services package"""
from .m3u_generator import generate_m3u_playlist
from .xtream_api import (
    fetch_api_data,
    fetch_categories_and_channels,
    fetch_series_episodes,
    validate_xtream_credentials,
)

__all__ = [
    'fetch_api_data',
    'validate_xtream_credentials',
    'fetch_categories_and_channels',
    'fetch_series_episodes',
    'generate_m3u_playlist'
]
