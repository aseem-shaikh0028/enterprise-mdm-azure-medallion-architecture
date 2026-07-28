"""
exporter.py

Exports the generated synthetic datasets to CSV files.

Generated files:
- crm_customers.csv
- erp_customers.csv
- banking_customers.csv
- marketing_customers.csv
- master_customer.csv
- master_customer_dirty.csv
"""

import os


class DatasetExporter:

    def __init__(self, output_directory="output"):
        self.output_directory = output_directory
        os.makedirs(self.output_directory, exist_ok=True)

    def export_dataframe(self, dataframe, filename):
        """
        Export a pandas DataFrame to CSV.
        """
        output_path = os.path.join(self.output_directory, filename)

        dataframe.to_csv(
            output_path,
            index=False,
            encoding="utf-8"
        )

        print(f"✔ Exported: {output_path}")

    def export_all(
        self,
        crm_df,
        erp_df,
        banking_df,
        marketing_df,
        master_df,
        master_dirty_df
    ):

        self.export_dataframe(crm_df, "crm_customers.csv")

        self.export_dataframe(erp_df, "erp_customers.csv")

        self.export_dataframe(banking_df, "banking_customers.csv")

        self.export_dataframe(marketing_df, "marketing_customers.csv")

        self.export_dataframe(master_df, "master_customer.csv")

        self.export_dataframe(master_dirty_df, "master_customer_dirty.csv")

        print("\n====================================")
        print("All datasets exported successfully.")
        print(f"Location: {os.path.abspath(self.output_directory)}")
        print("====================================")


if __name__ == "__main__":

    print(
        "This module is intended to be imported into the data generation pipeline."
    )
