import os.path
import logging
from configparser import SafeConfigParser
from lib.args import Args

__all__ = ['Config']


class VocConfigParser(SafeConfigParser):
    def getlist(self, section, option):
        return [x.strip() for x in self.get(section, option).split(',')]


files = [
    os.path.join(os.path.dirname(os.path.realpath(__file__)),
                 '../default-config.ini'),
    os.path.join(os.path.dirname(os.path.realpath(__file__)),
                 '../config.ini'),
    '/etc/voctomix/voctocore.ini',
    '/etc/voctomix.ini',  # deprecated
    '/etc/voctocore.ini',
    os.path.expanduser('~/.voctomix.ini'),  # deprecated
    os.path.expanduser('~/.voctocore.ini'),
]

if Args.ini_file is not None:
    files.append(Args.ini_file)

Config = VocConfigParser()
readfiles = Config.read(files)

log = logging.getLogger('ConfigParser')
log.debug('considered config-files: \n%s',
          "\n".join(["\t\t" + os.path.normpath(file) for file in files]))
log.debug('successfully parsed config-files: \n%s',
          "\n".join(["\t\t" + os.path.normpath(file) for file in readfiles]))

if Args.ini_file is not None and Args.ini_file not in readfiles:
    raise RuntimeError('explicitly requested config-file "%s" '
                       'could not be read', Args.ini_file)
