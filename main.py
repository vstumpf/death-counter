import keyboard
import requests
import configparser
import sqlite3
import datetime
import time
import logging
import sys

class DeathCounter:

    config = None
    db_path = None
    game_id = None

    log = None

    def __init__(self):
        self.init_logger()
        self.load_config()
        self.register_hotkeys()
        self.init_database()

    def record_death(self):
        dt = datetime.datetime.now().isoformat(sep=' ', timespec='seconds')
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('INSERT INTO deaths(game_id, datetime) VALUES (?, ?)', (self.game_id, dt))
            conn.commit()
        self.log.info('Recorded death')
        self.update_deaths()

    def undo_death(self):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('DELETE FROM deaths WHERE id = (SELECT MAX(id) FROM deaths)')
            conn.commit()
        self.log.info('Undid death')
        self.update_deaths()

    def update_deaths(self):
        count = None
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT count(*) FROM deaths')
            row = c.fetchone()
            count = row[0]
        
        with open(self.config['Paths']['OBSSource'], "w") as f:
            f.write(str(count))
        self.log.info('Updated death count: %d', count)

    def init_database(self):
        self.db_path = self.config['Paths']['Database']
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute(
                """CREATE TABLE IF NOT EXISTS deaths (
                    id INTEGER PRIMARY KEY,
                    game_id INTEGER,
                    datetime TEXT
                    )
                """
            )
            conn.commit()
        self.log.info('Initialized database')

    def init_logger(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] %(message)s')
        self.log = logging.getLogger()
        self.log.info('Initialized logger')


    def get_game(self):
        params = {'user_login': self.config['Twitch']['Username']}
        headers = {'Client-ID': self.config['Twitch']['Client-ID']}
        r = requests.get('https://api.twitch.tv/helix/streams', params=params, headers=headers)
        game_id = 0
        self.log.debug(r.json())
        try:
            r.raise_for_status()
            game_id = r.json()['data'][0]['game_id']
        except requests.exceptions.HTTPError:
            pass
        except ValueError:
            pass
        except IndexError:
            pass
        self.log.info('Game updated: ' + str(game_id))
        return game_id


    def load_config(self):
        self.config = configparser.ConfigParser()
        self.config.read('deathcounter.ini')
        config_dict = dict(self.config)
        for k in config_dict:
            config_dict[k] = dict(config_dict[k])
        self.log.info('Config loaded: %s', str(config_dict))
    
    def register_hotkeys(self):
        recorddeath_hk = self.config['Hotkeys']['RecordDeath']
        undodeath_hk = self.config['Hotkeys']['UndoDeath']
        keyboard.add_hotkey(recorddeath_hk, self.record_death, timeout=3)
        keyboard.add_hotkey(undodeath_hk, self.undo_death, timeout=3)
        self.log.info('Registered Hotkeys')
    
    def wait(self):
        self.log.info('Starting loop')
        while True:
            self.get_game()
            self.game_id = time.sleep(10)


def main():
    dc = DeathCounter()
    dc.wait()
    keyboard.remove_all_hotkeys()

if __name__ == "__main__":
    main()