import logging
import os

cwd = os.getcwd()
filepath = os.path.join(cwd, "app.log")
# Configure logging (this will be the central configuration)
logging.basicConfig(
    level=logging.WARNING,  # Set the logging level to ERROR or any desired level
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(filepath)
    ]
)

my_project_logger = logging.getLogger('my_project_logger')
