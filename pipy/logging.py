import logging
import logging.config


def disable_java_logging():
    import logging

    logging.getLogger("java_gateway").setLevel(logging.ERROR)
    logging.getLogger("java_gateway.run").setLevel(logging.ERROR)
    # Disable noisy Databricks JVM
    try:
        logger = spark._jvm.org.apache.log4j
        logger.LogManager.getRootLogger().setLevel(logger.Level.ERROR)

    except Exception as e:
        pass
    # Disable noisy Databricks JVM
    # https://forums.databricks.com/questions/17799/-infopy4jjava-gatewayreceived-command-c-on-object.html
    try:
        logging.getLogger("py4j").setLevel(logging.ERROR)
    except Exception as e:
        pass


disable_java_logging()


def get_logger(name=__name__):
    log_rd = {
            'version':                  1,
            'disable_existing_loggers': False,
            'formatters':               {
                    'standard': {

                            'format':  '%(asctime)s[%(module)s.%(funcName)s][%(levelname)s] %(message)s'.format(
                                    ),
                            'datefmt': '%Y-%m-%dT%I:%M:%S%z'
                            }
                    },
            'handlers':                 {
                    'default': {
                            'level':     'INFO',
                            'formatter': 'standard',
                            'class':     'logging.StreamHandler',
                            },

                    },
            'loggers':                  {
                    '': {
                            'handlers': ['default',
                                         # 'rotate_file'
                                         ],
                            'level':    'INFO',
                            },
                    }
            }

    logging.config.dictConfig(log_rd)
    return logging.getLogger(name)
