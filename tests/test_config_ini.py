import configparser
from pathlib import Path

import mackerel


def test_default_config_settings():
    config = configparser.ConfigParser()
    with open(Path(mackerel.__file__).parent / Path('config.ini')) as f:
        config.read_file(f)
    assert config['mackerel']['TEMPLATE_PATH'] == 'templates/example'
    assert config['mackerel']['OUTPUT_PATH'] == '_build'
    assert config['mackerel']['CONTENT_PATH'] == 'content'
    assert config['mackerel']['DOC_EXT'] == '.md'
