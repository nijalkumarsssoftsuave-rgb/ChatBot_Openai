import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='basic_loggingg.log', filemode='a')

logging.info("Hello World")
logging.info("Hello World")
logging.info("Hello World")
logging.error("Error")
logging.critical("crashed")

