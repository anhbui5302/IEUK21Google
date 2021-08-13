"""A video player class."""
import random

from .video_library import VideoLibrary
from .video_playlist_library import PlaylistLibrary


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._playlist_library = PlaylistLibrary()
        self.currently_playing = None
        self.video_paused = False

    def get_print_string(self, video):
        """Generates the video title, id and tags string for a video"""
        tags = ""
        "Construct the tags string from the tuple"
        for tag in video.tags:
            tags += tag + " "
        return video.title + " (" + video.video_id + ") [" + tags.strip() + "]"
    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""

        print("Here's a list of all available videos:")
        for video in self._video_library.get_all_videos():
            if video.flagged:
                print(self.get_print_string(video) + " - FLAGGED (reason: ", video.flag_reason, ")", sep='')
            else:
                print(self.get_print_string(video))

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        video = self._video_library.get_video(video_id)
        "If video does not exist"
        if not video:
            print("Cannot play video: Video does not exist")
            return
        "If video is flagged"
        if video.flagged:
            print("Cannot play video: Video is currently flagged (reason: ", video.flag_reason, ")",sep='')
            return
        if self.currently_playing != None:
            print("Stopping video:", self.currently_playing.title)
        print("Playing video:", self._video_library.get_video(video_id).title)
        self.currently_playing = self._video_library.get_video(video_id)
        self.video_paused = False

    def stop_video(self):
        """Stops the current video."""
        if self.currently_playing == None:
            print("Cannot stop video: No video is currently playing")
        else:
            print("Stopping video:", self.currently_playing.title)
            self.currently_playing = None
            self.video_paused = False

    def play_random_video(self):
        """Plays a random video from the video library."""
        if self.currently_playing != None:
            print("Stopping video:", self.currently_playing.title)
        unflagged_videos = self._video_library.get_unflagged_videos()
        #print(unflagged_videos)
        if not unflagged_videos:
            print("No videos available")
            return
        to_play = random.choice(unflagged_videos)
        print("Playing video:", to_play.title)
        self.currently_playing = to_play
        self.video_paused = False

    def pause_video(self):
        """Pauses the current video."""
        if self.currently_playing == None:
            print("Cannot pause video: No video is currently playing")
        else:
            if not(self.video_paused):
                print("Pausing video:", self.currently_playing.title)
                self.video_paused = True
            else:
                print("Video already paused:", self.currently_playing.title)

    def continue_video(self):
        """Resumes playing the current video."""
        if self.currently_playing == None:
            print("Cannot continue video: No video is currently playing")
        else:
            if not(self.video_paused):
                print("Cannot continue video: Video is not paused")
            else:
                print("Continuing video:", self.currently_playing.title)
                self.video_paused = False

    def show_playing(self):
        """Displays video currently playing."""
        if self.currently_playing == None:
            print("No video is currently playing")
        else:
            tags = ""
            "Construct the tags string from the tuple"
            for tag in self.currently_playing.tags:
                tags += tag + " "
            if self.video_paused:
                print("Currently playing: ", self.currently_playing.title," (", self.currently_playing.video_id, ") [",
                      tags.strip(),"] - PAUSED", sep='')
            else:
                print("Currently playing: ", self.currently_playing.title, " (", self.currently_playing.video_id, ") [",
                      tags.strip(), "]", sep='')

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        self._playlist_library.add_playlist(playlist_name)


    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        "Checks if the playlist exists"
        if self._playlist_library.get_playlist(playlist_name) == None:
            print("Cannot add video to ", playlist_name,": Playlist does not exist", sep='')
            return
        playlist = self._playlist_library[playlist_name.upper()]
        video = self._video_library.get_video(video_id)
        "Checks if the video exists"
        if video == None:
            print("Cannot add video to ", playlist_name,": Video does not exist", sep='')
            return
        "If video is flagged"
        if video.flagged:
            print("Cannot add video to ", playlist_name, ": Video is currently flagged (reason: ", video.flag_reason,
                  ")", sep='')
            return
        "Checks if the video is already in the playlist"
        if video in playlist._videos:
            print("Cannot add video to ", playlist_name,": Video already added", sep='')
            return
        "Adds the video to the playlist"
        playlist.add_video(video)
        print("Added video to ",playlist_name,": ", video.title, sep='')

    def show_all_playlists(self):
        """Display all playlists."""
        playlists = self._playlist_library.get_all_playlists()

        if not playlists:
            print("No playlists exist yet")
        else:
            print("Showing all playlists:")
            for playlist in playlists:
                print(" ",playlist.get_name())

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        "Checks if the playlist exists"
        if self._playlist_library.get_playlist(playlist_name) == None:
            print("Cannot show playlist ",playlist_name,": Playlist does not exist", sep='')
            return
        playlist = self._playlist_library[playlist_name.upper()]
        print("Showing playlist:", playlist_name)
        "If the playlist is empty"
        if playlist._videos == []:
            print("  No videos here yet")
        else:
            "Prints the videos"
            for video in playlist._videos:
                if video.flagged:
                    print(self.get_print_string(video) + " - FLAGGED (reason: ", video.flag_reason, ")", sep='')
                else:
                    print(self.get_print_string(video))

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        "Checks if the playlist exists"
        if self._playlist_library.get_playlist(playlist_name) == None:
            print("Cannot remove video from ",playlist_name,": Playlist does not exist", sep='')
            return
        playlist = self._playlist_library[playlist_name.upper()]
        video = self._video_library.get_video(video_id)
        "Checks if the video exists"
        if video == None:
            print("Cannot remove video from ",playlist_name,": Video does not exist", sep='')
            return
        "Checks if the video is in the playlist"
        if video not in playlist._videos:
            print("Cannot remove video from ",playlist_name,": Video is not in playlist", sep='')
            return
        "Removes the video from the playlist"
        playlist.remove_video(video)
        print("Removed video from ", playlist_name,": ",video.title, sep='')

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        "Checks if the playlist exists"
        if self._playlist_library.get_playlist(playlist_name) == None:
            print("Cannot clear playlist ",playlist_name,": Playlist does not exist", sep='')
            return
        playlist = self._playlist_library[playlist_name.upper()]
        "Clears the playlist"
        playlist.clear()
        print("Successfully removed all videos from", playlist_name)

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        "Checks if the playlist exists"
        if self._playlist_library.get_playlist(playlist_name) == None:
            print("Cannot delete playlist ",playlist_name,": Playlist does not exist", sep='')
            return
        playlist = self._playlist_library[playlist_name.upper()]
        self._playlist_library.delete_playlist(playlist_name.upper())
        print("Deleted playlist:", playlist_name)

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        "Obtain search results"
        search_results = []
        search_term_upper = search_term.upper()
        for video in self._video_library.get_all_videos():
            if (search_term_upper in video.title.upper()) and not video.flagged:
                search_results.append(video)
        "If there is no result matching the search term"
        if not search_results:
            print("No search results for", search_term)
            return
        "Print the search results"
        print("Here are the results for ", search_term, ":", sep='')

        for i in range(0,len(search_results)):
            print("  ", i+1, ") ",self.get_print_string(search_results[i]),sep='')
        print("Would you like to play any of the above? If yes, specify the number of the video.")
        print("If your answer is not a valid number, we will assume it's a no.")

        user_input = input("")
        try:
            val = int(user_input)
        except ValueError:
            val = 0

        if 1 <= val <= len(search_results):
            self.play_video(search_results[val-1].video_id)


    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        search_results = []
        for video in self._video_library.get_all_videos():
            if (video_tag in video.tags) and not video.flagged:
                search_results.append(video)

        "If there is no result matching the tags"
        if not search_results:
            print("No search results for", video_tag)
            return
        "Print the search results"
        print("Here are the results for ", video_tag, ":", sep='')

        for i in range(0, len(search_results)):
            print("  ", i + 1, ") ", self.get_print_string(search_results[i]), sep='')
        print("Would you like to play any of the above? If yes, specify the number of the video.")
        print("If your answer is not a valid number, we will assume it's a no.")

        user_input = input("")
        try:
            val = int(user_input)
        except ValueError:
            val = 0

        if 1 <= val <= len(search_results):
            self.play_video(search_results[val - 1].video_id)

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        "Default flag_reason is 'Not supplied'"
        if not flag_reason:
            flag_reason = "Not supplied"

        video = self._video_library.get_video(video_id)
        "If video does not exist"
        if not video:
            print("Cannot flag video: Video does not exist")
            return
        "If video is already flagged"
        if video.flagged:
            print("Cannot flag video: Video is already flagged")
            return
        if video == self.currently_playing:
            self.stop_video()
        video.flag(flag_reason)
        print("Successfully flagged video: ", video.title, " (reason: ", flag_reason,")", sep='')
    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        video = self._video_library.get_video(video_id)
        "If video does not exist"
        if not video:
            print("Cannot remove flag from video: Video does not exist")
            return
        "If video is not flagged"
        if not video.flagged:
            print("Cannot remove flag from video: Video is not flagged")
            return

        video.unflag()
        print("Successfully removed flag from video:", video.title)
