import sys
import pandas as pd
from src.logger import logger
from src.exception import CustomException
from src.entity.config_entity import CustomerAggregationConfig
from src.entity.artifact_entity import DataCleaningArtifact, CustomerAggregationArtifact

class CustomerAggregation:
    """
    CustomerAggregation changes the grain of the dataset from transaction-level
    to customer-level, computing raw un-opinionated facts.
    """
    def __init__(self, config: CustomerAggregationConfig):
        self.config = config

    def initiate_customer_aggregation(self, cleaning_artifact: DataCleaningArtifact) -> CustomerAggregationArtifact:
        """
        Groups the data by Customer ID and calculates raw facts (e.g. sums, counts).
        """
        logger.info("Starting customer aggregation process.")
        try:
            df = cleaning_artifact.cleaned_dataframe.copy()
            
            # Calculate a Revenue column to summarize
            df['Total_Price'] = df['Quantity'] * df['Price']
            
            # Identify returns for aggregation
            df['Returned_Quantity'] = df['Quantity'].apply(lambda x: abs(x) if x < 0 else 0)
            df['Purchased_Quantity'] = df['Quantity'].apply(lambda x: x if x > 0 else 0)
            
            # Group by Customer ID
            customer_facts = df.groupby('Customer ID').agg(
                Total_Invoices=('Invoice', 'nunique'),
                Total_Items_Bought=('Purchased_Quantity', 'sum'),
                Total_Returned_Items=('Returned_Quantity', 'sum'),
                Total_Spend=('Total_Price', 'sum'),
                First_Purchase_Date=('InvoiceDate', 'min'),
                Last_Purchase_Date=('InvoiceDate', 'max')
            ).reset_index()
            
            total_customers = customer_facts.shape[0]
            logger.info(f"Aggregation complete. Total customers found: {total_customers}")
            
            return CustomerAggregationArtifact(
                aggregated_dataframe=customer_facts,
                total_customers=total_customers
            )
            
        except Exception as e:
            logger.error("Error occurred in customer aggregation process.")
            raise CustomException(e, sys)
