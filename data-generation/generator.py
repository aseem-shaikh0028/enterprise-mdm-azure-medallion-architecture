import pandas as pd
from pathlib import Path
from transformer import CustomerTransformer


class DataLoader:

    def __init__(self):
        self.project_root = Path(__file__).resolve().parent.parent
        self.raw_path = self.project_root / "data" / "raw"

    # --------------------------------------------------------
    # Load Banking Dataset
    # --------------------------------------------------------
    def load_banking(self):
        return pd.read_csv(
            self.raw_path / "banking" / "BankChurners.csv"
        )

    # --------------------------------------------------------
    # Load CRM Dataset
    # --------------------------------------------------------
    def load_crm(self):
        return pd.read_excel(
            self.raw_path / "crm" / "generic_customer_dataset.xlsx"
        )

    # --------------------------------------------------------
    # Load Marketing Dataset
    # --------------------------------------------------------
    def load_marketing(self):
        return pd.read_csv(
            self.raw_path / "marketing" / "marketing_campaign.xls",
            sep="\t",
            engine="python",
            on_bad_lines="skip"
        )

    # --------------------------------------------------------
    # Load ERP Dataset
    # --------------------------------------------------------
    def load_erp(self):
        print("\n========== ERP ==========")

        erp_df = pd.read_csv(
            self.raw_path / "erp" / "customers_erp.csv"
        )

        print(erp_df.head())
        print(f"\nShape (raw) : {erp_df.shape}")

        # ------------------------------------------------------------
        # Quarantine rows with a missing/blank customer_id.
        #
        # The clean master dataset must have a complete primary
        # identifier for every record. Rows without one are dirty
        # data, not clean data, so they are split off here rather
        # than being carried forward into the canonical pipeline.
        # ------------------------------------------------------------
        if "customer_id" not in erp_df.columns:
            raise KeyError(
                "Expected a 'customer_id' column in customers_erp.csv "
                f"but found columns: {erp_df.columns.tolist()}"
            )

        # Treat both true NaN and blank/whitespace-only strings as missing.
        id_series = erp_df["customer_id"]
        is_missing = id_series.isna() | (
            id_series.astype(str).str.strip().eq("")
        )

        clean_erp_df = erp_df.loc[~is_missing].copy()
        dirty_erp_df = erp_df.loc[is_missing].copy()

        print(f"Null/blank customer_id rows : {len(dirty_erp_df)}")
        print(f"Shape (clean)                : {clean_erp_df.shape}")

        if not dirty_erp_df.empty:
            quarantine_dir = self.project_root / "data" / "quarantine"
            quarantine_dir.mkdir(parents=True, exist_ok=True)
            quarantine_path = quarantine_dir / "erp_missing_customer_id.csv"

            dirty_erp_df.to_csv(quarantine_path, index=False)
            print(
                f"Quarantined {len(dirty_erp_df)} row(s) with missing "
                f"customer_id to: {quarantine_path}"
            )

        return clean_erp_df


# ======================================================================
# MAIN PROGRAM
# ======================================================================

if __name__ == "__main__":

    print("=" * 70)
    print("ENTERPRISE MDM DATA INGESTION")
    print("=" * 70)

    # --------------------------------------------------------
    # Load Source Systems
    # --------------------------------------------------------

    loader = DataLoader()

    banking = loader.load_banking()
    crm = loader.load_crm()
    marketing = loader.load_marketing()
    erp = loader.load_erp()

    print("\n========== BANKING COLUMNS ==========")
    print(banking.columns.tolist())

    print("\n========== MARKETING COLUMNS ==========")
    print(marketing.columns.tolist())

    print("\nCRM Columns:")
    print(crm.columns.tolist())

    # --------------------------------------------------------
    # Canonical Transformations
    # --------------------------------------------------------

    transformer = CustomerTransformer()

    # CRM
    crm_canonical = transformer.transform_crm(crm)

    # ERP
    erp_canonical = transformer.transform_erp(erp)

    # Banking (needs CRM & ERP identities)
    banking_canonical = transformer.transform_banking(
        banking,
        crm_canonical,
        erp_canonical
    )

    # Marketing
    marketing_canonical = transformer.transform_marketing(marketing)

    # --------------------------------------------------------
    # Unified Master Customer Dataset
    # --------------------------------------------------------

    master_customer = pd.concat(
        [
            crm_canonical,
            banking_canonical,
            marketing_canonical,
            erp_canonical
        ],
        ignore_index=True
    )

    # Save clean master dataset
    master_customer.to_csv(
        "output/master_customer_clean.csv",
        index=False
    )

    print("\nClean master dataset saved to output/master_customer_clean.csv")

    print("\n========== MASTER CUSTOMER DATASET ==========")
    print(master_customer.head())
    print(f"Shape: {master_customer.shape}")

    # --------------------------------------------------------
    # Print Raw Source Data
    # --------------------------------------------------------

    print("\n========== BANKING ==========")
    print(banking.head())
    print("Shape:", banking.shape)

    print("\n========== CRM ==========")
    print(crm.head())
    print("Shape:", crm.shape)

    print("\n========== MARKETING ==========")
    print(marketing.head())
    print("Shape:", marketing.shape)

    # --------------------------------------------------------
    # Print Canonical Data
    # --------------------------------------------------------

    print("\n========== CRM CANONICAL ==========")
    print(crm_canonical.head())
    print("Shape:", crm_canonical.shape)

    print("\n========== BANKING CANONICAL ==========")
    print(banking_canonical.head())
    print("Shape:", banking_canonical.shape)

    print("\n========== MARKETING CANONICAL ==========")
    print(marketing_canonical.head())
    print("Shape:", marketing_canonical.shape)

    print("\n========== ERP CANONICAL ==========")
    print(erp_canonical.head())
    print("Shape:", erp_canonical.shape)

    # --------------------------------------------------------
    # Print Unified Master Dataset
    # --------------------------------------------------------

    print("\n========== MASTER CUSTOMER DATASET ==========")
    print(master_customer.head())
    print("Shape:", master_customer.shape)

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("DATASET SUMMARY")
    print("=" * 70)

    print(f"CRM Records        : {len(crm_canonical)}")
    print(f"Banking Records    : {len(banking_canonical)}")
    print(f"Marketing Records  : {len(marketing_canonical)}")
    print(f"ERP Records        : {len(erp_canonical)}")
    print("-" * 70)
    print(f"Master Records     : {len(master_customer)}")

    print("\n" + "=" * 70)
    print("INGESTION & CANONICAL TRANSFORMATION COMPLETED")
    print("=" * 70)