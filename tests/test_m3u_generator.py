import unittest
from unittest.mock import patch, MagicMock
from app.services.m3u_generator import generate_m3u_playlist

class TestM3UGenerator(unittest.TestCase):
    def test_generate_m3u_playlist_with_list_episodes(self):
        """
        Test that generate_m3u_playlist correctly handles episodes returned as a list
        instead of a dictionary.
        """
        url = "http://example.com"
        username = "user"
        password = "pass"
        server_url = "http://example.com:8080"
        categories = [{"category_id": "1", "category_name": "Action"}]
        streams = [
            {
                "series_id": 123,
                "name": "Test Series",
                "category_id": "1",
                "content_type": "series",
                "stream_icon": "http://example.com/icon.jpg"
            }
        ]

        # Mock fetch_series_episodes to return a list of episodes
        # The list contains episodes which may or may not have 'season' field
        episodes_list = [
            {"id": "ep1", "episode_num": 1, "title": "Ep 1", "container_extension": "mp4", "season": 1},
            {"id": "ep2", "episode_num": 2, "title": "Ep 2", "container_extension": "mp4", "season": 1},
            {"id": "ep3", "episode_num": 1, "title": "Ep 3", "container_extension": "mp4", "season": 2}
        ]

        def mock_fetch(url, username, password, series_id):
            return series_id, episodes_list

        with patch('app.services.m3u_generator.fetch_series_episodes', side_effect=mock_fetch):
            playlist = generate_m3u_playlist(
                url=url,
                username=username,
                password=password,
                server_url=server_url,
                categories=categories,
                streams=streams,
                include_vod=True,
                no_stream_proxy=True
            )

            # Assertions
            self.assertIn("#EXTM3U", playlist)
            self.assertIn("Test Series - S01E01 - Ep 1", playlist)
            self.assertIn("Test Series - S01E02 - Ep 2", playlist)
            self.assertIn("Test Series - S02E01 - Ep 3", playlist)
            self.assertIn("http://example.com:8080/series/user/pass/ep1.mp4", playlist)

    def test_generate_m3u_playlist_with_list_episodes_no_season(self):
        """
        Test that generate_m3u_playlist handles list episodes without season field (defaults to 1).
        """
        url = "http://example.com"
        username = "user"
        password = "pass"
        server_url = "http://example.com:8080"
        categories = [{"category_id": "1", "category_name": "Action"}]
        streams = [
            {
                "series_id": 456,
                "name": "No Season Series",
                "category_id": "1",
                "content_type": "series",
            }
        ]

        # Mock fetch_series_episodes to return a list of episodes without season
        episodes_list = [
            {"id": "epX", "episode_num": 1, "title": "Ep X", "container_extension": "mp4"}
        ]

        def mock_fetch(url, username, password, series_id):
            return series_id, episodes_list

        with patch('app.services.m3u_generator.fetch_series_episodes', side_effect=mock_fetch):
            playlist = generate_m3u_playlist(
                url=url,
                username=username,
                password=password,
                server_url=server_url,
                categories=categories,
                streams=streams,
                include_vod=True,
                no_stream_proxy=True
            )

            # Assertions
            self.assertIn("No Season Series - S01E01 - Ep X", playlist)

    def test_generate_m3u_playlist_with_added_and_size(self):
        """
        Test that generate_m3u_playlist correctly adds 'added' attribute and '#EXTBYT' directive.
        """
        url = "http://example.com"
        username = "user"
        password = "pass"
        server_url = "http://example.com:8080"
        categories = [{"category_id": "1", "category_name": "Movies"}]
        streams = [
            {
                "stream_id": 101,
                "name": "Test Movie",
                "category_id": "1",
                "content_type": "vod",
                "added": "1672531200",
                "size": "104857600",  # 100 MB
                "container_extension": "mp4"
            },
            {
                "series_id": 202,
                "name": "Test Series",
                "category_id": "1",
                "content_type": "series",
            }
        ]

        episodes_list = [
            {
                "id": "ep1",
                "episode_num": 1,
                "title": "Ep 1",
                "container_extension": "mkv",
                "season": 1,
                "added": "1672617600",
                "size": 52428800 # 50 MB (int)
            }
        ]

        def mock_fetch(url, username, password, series_id):
            return series_id, episodes_list

        with patch('app.services.m3u_generator.fetch_series_episodes', side_effect=mock_fetch):
            playlist = generate_m3u_playlist(
                url=url,
                username=username,
                password=password,
                server_url=server_url,
                categories=categories,
                streams=streams,
                include_vod=True,
                no_stream_proxy=True
            )

            # Assertions for Movie
            self.assertIn('added="1672531200"', playlist)
            self.assertIn('#EXTBYT:104857600', playlist)

            # Assertions for Series Episode
            self.assertIn('added="1672617600"', playlist)
            self.assertIn('#EXTBYT:52428800', playlist)

if __name__ == '__main__':
    unittest.main()
