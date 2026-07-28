import pandas as pd
from datetime import datetime
from faker import Faker
import random
import string

fake = Faker("en_IN")
random.seed(42)
Faker.seed(42)


class CustomerTransformer:

    def __init__(self):
        self.current_year = datetime.now().year

    # --------------------------------------------------------
    # CRM Transformation
    # --------------------------------------------------------
    def transform_crm(self, df):

        canonical = pd.DataFrame()

        canonical["customer_id"] = df["customer_id"].astype(str)
        canonical["first_name"] = df["first_name"]
        canonical["last_name"] = df["last_name"]

        canonical["full_name"] = (
            df["first_name"] + " " + df["last_name"]
        )

        canonical["date_of_birth"] = pd.to_datetime(df["date_of_birth"])

        canonical["age"] = (
            self.current_year -
            canonical["date_of_birth"].dt.year
        )

        canonical["gender"] = df["gender"]

        canonical["email"] = df["email"]
        canonical["phone"] = df["phone"]

        canonical["address"] = df["address_line1"]
        canonical["city"] = df["city"]
        canonical["state"] = df["state"]
        canonical["postal_code"] = df["postal_code"]
        canonical["country"] = df["country"]

        canonical["pan_number"] = df["pan_number"]
        canonical["aadhaar_number"] = df["aadhaar_number"]

        canonical["education"] = None
        canonical["income"] = None
        canonical["marital_status"] = None

        canonical["source_system"] = "CRM"

        return canonical

    # --------------------------------------------------------
    # Banking Transformation
    # --------------------------------------------------------
    def transform_banking(self, df, crm_df, erp_df):

        canonical = pd.DataFrame()

        canonical["customer_id"] = df["CLIENTNUM"].astype(str)

        # Build identity pool from CRM + ERP
        identity_pool = pd.concat(
            [
                crm_df[
                    [
                        "first_name",
                        "last_name",
                        "full_name",
                        "date_of_birth",
                        "email",
                        "phone",
                        "address",
                        "city",
                        "state",
                        "postal_code",
                        "country",
                        "pan_number",
                        "aadhaar_number",
                    ]
                ],
                erp_df[
                    [
                        "first_name",
                        "last_name",
                        "full_name",
                        "date_of_birth",
                        "email",
                        "phone",
                        "address",
                        "city",
                        "state",
                        "postal_code",
                        "country",
                        "pan_number",
                        "aadhaar_number",
                    ]
                ],
            ],
            ignore_index=True,
        ).drop_duplicates()

        overlap_fraction = 0.40
        overlap_size = int(len(df) * overlap_fraction)
        overlap_indices = set(random.sample(range(len(df)), overlap_size))

        identities = []

        for i in range(len(df)):

            if i in overlap_indices and len(identity_pool) > 0:

                identities.append(
                    identity_pool.sample(1).iloc[0].to_dict()
                )

            else:

                first = fake.first_name()
                last = fake.last_name()

                identities.append(
                    {
                        "first_name": first,
                        "last_name": last,
                        "full_name": f"{first} {last}",
                        "date_of_birth": fake.date_of_birth(
                            minimum_age=20,
                            maximum_age=70,
                        ),
                        "email": fake.email(),
                        "phone": fake.msisdn()[-10:],
                        "address": fake.street_address(),
                        "city": fake.city(),
                        "state": fake.state(),
                        "postal_code": fake.postcode(),
                        "country": "India",
                        "pan_number": (
                            "".join(random.choices(string.ascii_uppercase, k=5))
                            + "".join(random.choices(string.digits, k=4))
                            + random.choice(string.ascii_uppercase)
                        ),
                        "aadhaar_number": "".join(
                            random.choices(string.digits, k=12)
                        ),
                    }
                )

        identity_df = pd.DataFrame(identities)

        canonical = pd.concat(
            [
                canonical.reset_index(drop=True),
                identity_df.reset_index(drop=True),
            ],
            axis=1,
        )

        canonical["age"] = df["Customer_Age"]
        canonical["gender"] = (
    df["Gender"]
        .replace({
            "M": "Male",
            "F": "Female"
        }) 
)
        canonical["education"] = df["Education_Level"]
        canonical["income"] = df["Income_Category"]
        canonical["marital_status"] = df["Marital_Status"]
        canonical["source_system"] = "BANKING"

        return canonical

    # --------------------------------------------------------
    # Marketing Transformation
    # --------------------------------------------------------
    def transform_marketing(self, df):

        canonical = pd.DataFrame()

        canonical["customer_id"] = df["ID"].astype(str)

        canonical["first_name"] = None
        canonical["last_name"] = None
        canonical["full_name"] = None
        canonical["date_of_birth"] = None

        canonical["age"] = self.current_year - df["Year_Birth"]

        canonical["gender"] = None

        canonical["email"] = None
        canonical["phone"] = None

        canonical["address"] = None
        canonical["city"] = None
        canonical["state"] = None
        canonical["postal_code"] = None
        canonical["country"] = None

        canonical["pan_number"] = None
        canonical["aadhaar_number"] = None

        canonical["education"] = df["Education"]
        canonical["income"] = df["Income"]
        canonical["marital_status"] = df["Marital_Status"]

        canonical["source_system"] = "MARKETING"

        return canonical

    # --------------------------------------------------------
    # ERP Transformation
    # --------------------------------------------------------
    def transform_erp(self, df):

        canonical = pd.DataFrame()

        canonical["customer_id"] = df["customer_id"].astype(str)

        canonical["first_name"] = df["first_name"]
        canonical["last_name"] = df["last_name"]

        canonical["full_name"] = (
            df["first_name"] + " " + df["last_name"]
        )

        canonical["date_of_birth"] = pd.to_datetime(
            df["date_of_birth"]
        )

        canonical["age"] = (
            self.current_year -
            canonical["date_of_birth"].dt.year
        )

        canonical["gender"] = df["gender"]

        canonical["email"] = df["email"]
        canonical["phone"] = df["phone"]

        canonical["address"] = df["address_line1"]
        canonical["city"] = df["city"]
        canonical["state"] = df["state"]
        canonical["postal_code"] = df["postal_code"]
        canonical["country"] = df["country"]

        canonical["pan_number"] = df["pan_number"]
        canonical["aadhaar_number"] = df["aadhaar_number"]

        canonical["education"] = None
        canonical["income"] = None
        canonical["marital_status"] = None

        canonical["source_system"] = "ERP"

        return canonical