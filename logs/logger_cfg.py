from utils.paths import path_to_log

cfg = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console_msg': {
            'format': '%(asctime)s | %(levelname)3s | %(filename)s:%(funcName)s:%(lineno)s | %(message)s',
            'datefmt': '%d-%m-%Y %H:%M:%S'
        },
        'file_msg': {
            'format': '%(asctime)s | %(levelname)3s | %(filename)s:%(funcName)s:%(lineno)s | %(message)s',
            'datefmt': '%d-%m-%Y %H:%M:%S'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'console_msg'
        },
        'file_main': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'DEBUG',
            'filename': path_to_log("main.log"),
            'formatter': 'file_msg',
            'when': 'midnight',        # ротация каждый день в полночь
            'interval': 1,
            'backupCount': 3,          # хранить 3 последних логов
            'encoding': 'utf-8'
        },
        'file_gui': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'DEBUG',
            'filename': path_to_log("gui.log"),
            'formatter': 'file_msg',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 3,
            'encoding': 'utf-8'
        },
        'file_bridge': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'DEBUG',
            'filename': path_to_log("bridges.log"),
            'formatter': 'file_msg',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 3,
            'encoding': 'utf-8'
        },
        'file_worker': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'DEBUG',
            'filename': path_to_log("worker.log"),
            'formatter': 'file_msg',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 3,
            'encoding': 'utf-8'
        },
        'file_db': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'DEBUG',
            'filename': path_to_log("db.log"),
            'formatter': 'file_msg',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 3,
            'encoding': 'utf-8'
        },
        'file_scan': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'DEBUG',
            'filename': path_to_log("scan.log"),
            'formatter': 'file_msg',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 3,
            'encoding': 'utf-8'
        },
        'file_utils': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'DEBUG',
            'filename': path_to_log("utils.log"),
            'formatter': 'file_msg',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 3,
            'encoding': 'utf-8'
        },
    },
    'loggers': {
        'log_main': {
            'level': 'DEBUG',
            'handlers': ['console', 'file_main'],
            'propagate': False
        },
        'log_gui': {
            'level': 'DEBUG',
            'handlers': ['console', 'file_gui'],
            'propagate': False
        },
        'log_bridge': {
            'level': 'DEBUG',
            'handlers': ['console', 'file_bridge'],
            'propagate': False
        },
        'log_worker': {
            'level': 'DEBUG',
            'handlers': ['console', 'file_worker'],
            'propagate': False
        },
        'log_db': {
            'level': 'DEBUG',
            'handlers': ['console', 'file_db'],
            'propagate': False
        },
        'log_scan': {
            'level': 'DEBUG',
            'handlers': ['console', 'file_scan'],
            'propagate': False
        },
        'log_utils': {
            'level': 'DEBUG',
            'handlers': ['console', 'file_utils'],
            'propagate': False
        },
    }
}
