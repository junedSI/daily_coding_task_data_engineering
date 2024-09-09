import logging
from observex.executors.oxexecutors import ObserveXExecutor

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ObserveX():
    @staticmethod
    def observe(dataset, ruleset):
        logging.info("observe method called with dataset: %s and ruleset: %s", dataset, ruleset)
        return ObserveX._observe(dataset, ruleset)

    @staticmethod
    def scan(dataset, ruleset):
        logging.info("scan method called with dataset: %s and ruleset: %s", dataset, ruleset)
        return ObserveX._observe(dataset, ruleset)
    
    @staticmethod
    def _observe(dataset, ruleset):
        """Validate parameters"""
        if dataset is None:
            logging.error("Invalid value passed for parameter 'dataset': None")
            raise ValueError("Invalid value passed for parameter 'dataset': None")
        if ruleset is None:
            logging.error("Invalid value passed for parameter 'ruleset': None")
            raise ValueError("Invalid value passed for parameter 'ruleset': None")
        
        logging.info("Validating dataset and ruleset parameters...")
        # Additional validation logic here
        if not isinstance(ruleset, list):
            logging.error("Invalid value passed for parameter 'ruleset': Expected list, got %s", type(ruleset))
            raise ValueError("Invalid value passed for parameter 'ruleset': Expected list")

        # Call executor
        logging.info("Calling ObserveXExecutor with dataset and ruleset")
        result = ObserveXExecutor().execute(dataset, ruleset)
        logging.info("Execution complete")
        
        return result
