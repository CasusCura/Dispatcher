from tornado.options import define

# Define command line parameters and config
define('port', default=8088, help='run on the given port', type=int)
define('mode', default='dev', help='run app for specific config', type=str)
define('db',
       default='sqlite:///dispatcher-0.2.db',
       help='run with the given database file',
       type=str)
