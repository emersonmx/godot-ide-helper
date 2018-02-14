import os
import requests

class Downloader:

    def download(self):
        pass

class ZipDownloader(Downloader):

    def __init__(self, version):
        super(ZipDownloader, self).__init__()

        self.dl_url_base = 'https://github.com/godotengine/godot/archive/'
        self.version = version

    def get_download_url(self):
        return os.path.join(self.dl_url_base, self.zip_filename())

    def zip_filename(self):
        return '{}.zip'.format(self.version)

    def get_output_path(self):
        home_path = os.environ.get('HOME')
        base_path = os.path.abspath('.')
        if home_path:
            base_path = os.path.join(home_path, '.cache/godot_ide_helper')
            os.makedirs(base_path, exist_ok=True)
        return os.path.join(base_path, self.zip_filename())

    def download(self):
        dl_url = self.get_download_url()
        response = requests.get(dl_url, stream=True)
        with open(self.get_output_path(), 'wb') as f:
            for chunk in response:
                f.write(chunk)
