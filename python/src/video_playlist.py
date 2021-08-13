"""A video playlist class."""


class Playlist:
    """A class used to represent a Playlist."""
    def __init__(self, name: str):
        self._name = name
        "Stores videos as a list"
        self._videos = []

    "Returns the list of videos as a tuple"
    def videos(self):
        return tuple(self._videos)

    "Returns the name of the playlist"
    def get_name(self):
        return self._name
    "Adds a video to the playlist"
    def add_video(self, video):
            self._videos.append(video)

    "Removes a video from the playlist"
    def remove_video(self, video):
        self._videos.remove(video)

    "Clears the playlist"
    def clear(self):
        self._videos.clear()