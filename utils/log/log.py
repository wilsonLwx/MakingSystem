# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
#             'style': '{',
#         },
#         'simple': {
#             'format': '{levelname} {message}',
#             'style': '{',
#         },
#     },
#     'filters': {
#         'special': {
#             '()': 'project.logging.SpecialFilter',
#             'foo': 'bar',
#         },
#         'require_debug_true': {
#             '()': 'django.utils.log.RequireDebugTrue',
#         },
#     },
#     'handlers': {
#         'console': {
#             'level': 'INFO',
#             'filters': ['require_debug_true'],
#             'class': 'logging.StreamHandler',
#             'formatter': 'simple'
#         },
#         'mail_admins': {
#             'level': 'ERROR',
#             'class': 'django.utils.log.AdminEmailHandler',
#             'filters': ['special']
#         }
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'propagate': True,
#         },
#         'django.request': {
#             'handlers': ['mail_admins'],
#             'level': 'ERROR',
#             'propagate': False,
#         },
#         'myproject.custom': {
#             'handlers': ['console', 'mail_admins'],
#             'level': 'INFO',
#             'filters': ['special']
#         }
#     }
# }

# import os
#
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
#         },
#     },
# }
import os
import datetime
import logging
import logging.config


def genLogDict(logDir, logFile):
    '''
    配置日志格式的字典
    '''
    logDict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                'format': '%(asctime)s [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
            },
            'standard': {
                'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
            },
        },

        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "stream": "ext://sys.stdout"
            },

            "default": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "simple",
                "filename": os.path.join(logDir, logFile),
                'mode': 'w+',
                "maxBytes": 1024 * 1024 * 5,  # 5 MB
                "backupCount": 20,
                "encoding": "utf8"
            },
        },

        # "loggers": {
        #     "app_name": {
        #         "level": "INFO",
        #         "handlers": ["console"],
        #         "propagate": "no"
        #     }
        # },

        "root": {
            'handlers': ['default'],
            'level': "INFO",
            'propagate': False
        }
    }
    return logDict


def initLogConf():
    """
    配置日志
    """
    baseDir = os.path.dirname(os.path.abspath(__file__))
    logDir = os.path.join(baseDir, "logs")
    if not os.path.exists(logDir):
        os.makedirs(logDir)  # 创建路径

    logFile = datetime.datetime.now().strftime("%Y-%m-%d") + ".log"
    logDict = genLogDict(logDir, logFile)
    logging.config.dictConfig(logDict)
