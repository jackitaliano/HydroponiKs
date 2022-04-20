from os.path import join
import Methods.json_methods as json_methods

DEV_CONFIG_FILE_PATH = join('config', 'dev-config.json')
DEV_CONFIG = json_methods.load_json(DEV_CONFIG_FILE_PATH)