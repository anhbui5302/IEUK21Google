"""A Playlist Library class"""

from .video_playlist import Playlist


class PlaylistLibrary:
    """A class used to represent a Playlist Library."""

    def __init__(self):
        """Stores Playlists as a dictionary to allow for searching"""
        self._playlists = {}

    def __getitem__(self, name):
        "Allows the '[]' operator to be used on PlaylistLibrary instances"
        return self._playlists[name.upper()]

    def add_playlist(self, name):
        """Adds the playlist to the library"""
        name_upper = name.upper()
        "Checks if a playlist with the same name exists"
        if name_upper in self._playlists:
            print("Cannot create playlist: A playlist with the same name already exists")
        else:
            self._playlists[name_upper] = Playlist(name)
            print("Successfully created new playlist:", name)

    def get_playlist(self, name):
        """Returns the playlist from the library if it exists"""
        return self._playlists.get(name.upper(), None)

    def delete_playlist(self, name):
        """Deletes the playlist from the library"""
        del self._playlists[name.upper()]

    def get_all_playlists(self):
        """Returns all available playlist names from the library"""
        "Sorts the list of playlists by name in alphabetical order"
        return sorted(self._playlists.values(), key=lambda x: x._name)
