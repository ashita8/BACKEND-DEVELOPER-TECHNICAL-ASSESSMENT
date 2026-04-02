from sqlalchemy import Column, String, Date, Numeric, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(String, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone = Column(String)
    address = Column(Text)
    date_of_birth = Column(Date)
    account_balance = Column(Numeric)
    created_at = Column(TIMESTAMP)