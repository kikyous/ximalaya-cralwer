from selenium import webdriver
import time
import aria2p
import json
import os

print('1. start aria2c: `aria2c --enable-rpc --rpc-listen-all`')
print('2. login your account and play first track')

driver = webdriver.Chrome()
driver.get('https://www.ximalaya.com/')

input('3. press any key to start download: ')

aria2 = aria2p.API(
    aria2p.Client(
        host="http://localhost",
        port=6800,
    )
)

base_dir = os.getcwd()


class Track:
    tracks = []

    def __init__(self, data):
        self.data = data
        self.id = data['trackId']
        self.name = data['trackName']
        self.album_name = data['albumName']
        self.album_id = data['albumId']
        self.src = data['src']

    @classmethod
    def current(cls):
        storage = driver.execute_script("return localStorage.getItem('player_track');")
        data = json.loads(storage)
        return Track(data)

    @classmethod
    def get_new_track(cls):
        while True:
            track = cls.current()
            if len(cls.tracks) > 1 and track.id == cls.tracks[0]:
                return False
            elif track.id in cls.tracks:
                time.sleep(0.2)
            else:
                cls.tracks.append(track.id)
                return track

    @classmethod
    def next(cls):
        next_btn = driver.find_element_by_css_selector("a.next")
        next_btn.click()
        time.sleep(0.5)

    def download(self):
        options = {
            'dir': f'{base_dir}/{self.album_id}/',
            'out': f'{self.name}.m4a'
        }
        aria2.add_uris([self.src], options)


while True:
    track = Track.get_new_track()
    if track:
        track.download()
    else:
        exit()

    track.next()
