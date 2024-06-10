import logging
from logging.handlers import RotatingFileHandler

# Create and configure the first logger
funnel_logger = logging.getLogger('FunnelLogger')
funnel_logger.setLevel(logging.INFO)
funnel_handler = RotatingFileHandler('funnel_audits.log', maxBytes=2000, backupCount=5)
funnel_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
funnel_handler.setFormatter(funnel_formatter)
funnel_logger.addHandler(funnel_handler)

# Create and configure the second logger
creds_logger = logging.getLogger('CredsLogger')
creds_logger.setLevel(logging.INFO)
creds_handler = RotatingFileHandler('creds_audits.log', maxBytes=2000, backupCount=5)
creds_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
creds_handler.setFormatter(creds_formatter)
creds_logger.addHandler(creds_handler)

# Log messages using both loggers
funnel_logger.info('This is an info message from the funnel logger.')
creds_logger.info('This is an info message from the creds logger.')