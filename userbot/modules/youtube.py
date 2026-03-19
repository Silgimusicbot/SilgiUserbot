import yt_dlp

class YouTubeDownloader:
    def __init__(self):
        self.ydl_opts_ytaudio = {
            'format': 'ba/b',
        }
        self.extractor_args = {
            'player_client': ['web'],
            'player_skip': True
        }
        self.ydl_opts_ytvideo = {
            'format': 'bv*+ba/b',
            'merge_output_format': 'mp4',
        }

    def download_audio(self, url):
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts_ytaudio) as ydl:
                ydl.download([url])
        except Exception as e:
            if 'Requested format is not available' in str(e):
                raise Exception('The requested audio format is not available. Please check the availability of the requested format.')
            raise

    def download_video(self, url):
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts_ytvideo) as ydl:
                ydl.download([url])
        except Exception as e:
            if 'Requested format is not available' in str(e):
                raise Exception('The requested video format is not available. Please check the availability of the requested format.')
            raise

# Example usage:
# downloader = YouTubeDownloader()
# downloader.download_audio('video_url')
# downloader.download_video('video_url')