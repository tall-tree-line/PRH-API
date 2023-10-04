from typing import Optional, Union, Tuple, Type
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from uuid import uuid4
from decouple import config

from prh.helpers import as_timestamp, convert_address_type, convert_version, convert_source, REGISTERED_ENTRY_AUTHORITY, REGISTERED_ENTRY_REGISTER, REGISTERED_ENTRY_STATUS
from prh.logging_config import my_project_logger


Base = declarative_base()

class BaseCompanyModel(Base):
    __tablename__ = "company"

    pk = Column("pk", String, primary_key=True)
    company_number = Column("company_number", String)
    registration_date = Column("registration_date", DateTime)
    company_form = Column("company_form", String)
    details_uri = Column("details_uri", String)
    company_name = Column("company_name", String)
    data_fetched = Column("data_fetched", DateTime, nullable=False)

    # __table_args__ = (
    #     UniqueConstraint("pk"),
    # )

    @classmethod
    def from_dict(cls, company_uid:str, data_fetched:datetime, data:Optional[dict]):
        if not data:
            return cls()
        
        return cls(
            pk = company_uid,
            company_number = data.get("businessId"),
            registration_date = as_timestamp(data.get("registrationDate")),
            company_form = data.get("companyForm"),
            details_uri = data.get("detailsUri"),
            company_name = data.get("name"),
            data_fetched = data_fetched
        )

class CompanyNameModel(Base):
    __tablename__ = "company_name"

    pk = Column("pk", String, primary_key=True)
    company_uid = Column("company_uid", String, ForeignKey("company.pk"), nullable=False)
    source = Column("source", String)
    order = Column("order", String)
    version = Column("version", String)
    registration_date = Column("registration_date", String)
    end_date = Column("end_date", String)
    name = Column("name", String)
    language = Column("language", String)
    data_fetched = Column("data_fetched", DateTime, nullable=False)

    @classmethod
    def from_dict(cls, company_uid:str, data_fetched:datetime, data: Optional[dict]):
        if not data:
            return cls()
        
        return cls(
            pk = str(uuid4()),
            company_uid = company_uid,
            source = convert_source(data.get("version")),
            order = data.get("order"),
            version = convert_version(data.get("version")),
            registration_date = as_timestamp(data.get("registrationDate")),
            end_date = as_timestamp(data.get("endDate")),
            name = data.get("name"),
            language = data.get("language"),
            data_fetched = data_fetched
        )

class AddressModel(Base):
    __tablename__ = "address"

    pk = Column("pk", String, primary_key=True)
    company_uid = Column("company_uid", String, ForeignKey("company.pk"), nullable=False)
    source = Column("source", String)
    version = Column("version", String)
    registration_date = Column("registration_date", DateTime)
    end_date = Column("end_date", DateTime)
    care_of = Column("care_of", String)
    street = Column("street", String)
    post_code = Column("post_code", String)
    city = Column("city", String)
    language = Column("language", String)
    address_type = Column("address_type", String)
    country = Column("country", String)
    data_fetched = Column("data_fetched", DateTime, nullable=False)

    @classmethod
    def from_dict(cls, company_uid:str, data_fetched:datetime, data: Optional[dict]):
        if not data:
            return cls()
        
        return cls(
            pk = str(uuid4()),
            company_uid = company_uid,
            source = convert_source(data.get("version")),
            version = convert_version(data.get("version")),
            registration_date = as_timestamp(data.get("registrationDate")),
            end_date = as_timestamp(data.get("endDate")),
            care_of = data.get("careOf"),
            street = data.get("street"),
            post_code = data.get("postCode"),
            city = data.get("city"),
            language = data.get("language"),
            address_type = convert_address_type(data.get("type")),
            country = data.get("country"),
            data_fetched = data_fetched
        )
        
class CompanyFormModel(Base):
    __tablename__ = "company_form"

    pk = Column("pk", String, primary_key=True)
    company_uid = Column("company_uid", String, ForeignKey("company.pk"), nullable=False)
    source = Column("source", String)
    registration_date = Column("registration_date", DateTime)
    end_date = Column("end_date", DateTime)
    version = Column("version", String)
    name = Column("name", String)
    language = Column("language", String)
    form_type = Column("form_type", String)
    data_fetched = Column("data_fetched", DateTime, nullable=False)

    @classmethod
    def from_dict(cls, company_uid:str, data_fetched:datetime, data:Optional[dict]):
        if not data:
            return cls()
        
        return cls(
            pk = str(uuid4()),
            company_uid = company_uid,
            source = convert_source(data.get("version")),
            registration_date = as_timestamp(data.get("registrationDate")),
            end_date = as_timestamp(data.get("endDate")),
            version = convert_version(data.get("version")),
            name = data.get("name"),
            language = data.get("language"),
            form_type = data.get("type"),
            data_fetched = data_fetched
        )

class CompanyLiquidationModel(Base):
    __tablename__ = "liquidation"

    pk = Column("pk", String, primary_key=True)
    company_uid = Column("company_uid", String, ForeignKey("company.pk"), nullable=False)
    source = Column("source", String)
    registration_date = Column("registration_date", DateTime)
    end_date = Column("end_date", DateTime)
    version = Column("version", String)
    name = Column("name", String)
    language = Column("language", String)
    liquidation_type = Column("liquidation_type", String)
    data_fetched = Column("data_fetched", DateTime, nullable=False)

    @classmethod
    def from_dict(cls, company_uid:str, data_fetched:datetime, data:Optional[dict]):
        if not data:
            return cls()
        
        return cls(
            pk = str(uuid4()),
            company_uid = company_uid,
            source = convert_source(data.get("version")),
            registration_date = as_timestamp(data.get("registrationDate")),
            end_date = as_timestamp(data.get("endDate")),
            version = convert_version(data.get("version")),
            name = data.get("name"),
            language = data.get("language"),
            liquidation_type = data.get("type"),
            data_fetched = data_fetched
        )
    
class BusinessLineModel(Base):
    __tablename__ = "business_line"

    pk = Column("pk", String, primary_key=True)
    company_uid = Column("company_uid", String, ForeignKey("company.pk"), nullable=False)
    source = Column("source", String)
    code = Column("code", String)
    order = Column("order", String)
    version = Column("version", String)
    registration_date = Column("registration_date", DateTime)
    end_date = Column("end_date", DateTime)
    name = Column("name", String)
    language = Column("language", String)
    data_fetched = Column("data_fetched", DateTime, nullable=False)

    @classmethod
    def from_dict(cls, company_uid:str, data_fetched:datetime, data:Optional[dict]):
        if not data:
            return cls()
        
        return cls(
            pk = str(uuid4()),
            company_uid = company_uid,
            source = convert_source(data.get("version")),
            code = data.get("code"),
            order = data.get("order"),
            registration_date = as_timestamp(data.get("registrationDate")),
            end_date = as_timestamp(data.get("endDate")),
            version = convert_version(data.get("version")),
            name = data.get("name"),
            language = data.get("language"),
            data_fetched = data_fetched
        )
    
class RegisteredOfficeModel(Base):
    __tablename__ = "registered_office"

    pk = Column("pk", String, primary_key=True)
    company_uid = Column("company_uid", String, ForeignKey("company.pk"), nullable=False)
    source = Column("source", String)
    order = Column("order", Integer)
    registration_date = Column("registration_date", DateTime)
    end_date = Column("end_date", DateTime)
    version = Column("version", String)
    name = Column("name", String)
    language = Column("language", String)
    data_fetched = Column("data_fetched", DateTime, nullable=False)

    @classmethod
    def from_dict(cls, company_uid:str, data_fetched:datetime, data:Optional[dict]):
        if not data:
            return cls()
        
        return cls(
            pk = str(uuid4()),
            company_uid = company_uid,
            source = convert_source(data.get("version")),
            order = data.get("order"),
            registration_date = as_timestamp(data.get("registrationDate")),
            end_date = as_timestamp(data.get("endDate")),
            version = convert_version(data.get("version")),
            name = data.get("name"),
            language = data.get("language"),
            data_fetched = data_fetched
        )
    
class ContactDetailModel(Base):
    __tablename__ = "contact_detail"

    pk = Column("pk", String, primary_key=True)
    company_uid = Column("company_uid", String, ForeignKey("company.pk"), nullable=False)
    source = Column("source", String)
    version = Column("version", String)
    registration_date = Column("registration_date", DateTime)
    end_date = Column("end_date", DateTime)
    language = Column("language", String)
    contact_type = Column("contact_type", String)
    value = Column("value", String)
    data_fetched = Column("data_fetched", DateTime, nullable=False)

    @classmethod
    def from_dict(cls, company_uid:str, data_fetched:datetime, data:Optional[str]):
        if not data:
            return cls()
        
        return cls(
            pk = str(uuid4()),
            company_uid = company_uid,
            source = convert_source(data.get("version")),
            version = convert_version(data.get("version")),
            registration_date = as_timestamp(data.get("registrationDate")),
            end_date = as_timestamp(data.get("endDate")),
            language = data.get("language"),
            contact_type = data.get("type"),
            value = data.get("value"),
            data_fetched = data_fetched
        )
    
class RegisteredEntryModel(Base):
    __tablename__ = "registered_entry"

    pk = Column("pk", String, primary_key=True)
    company_uid = Column("company_uid", String, ForeignKey("company.pk"), nullable=False)
    description = Column("description", String)
    status = Column("status", String)
    registration_date = Column("registration_date", DateTime)
    end_date = Column("end_date", DateTime)
    register = Column("register", String)
    language = Column("language", String)
    authority = Column("authority", String)
    data_fetched = Column("data_fetched", DateTime, nullable=False)

    @classmethod
    def from_dict(cls, company_uid:str, data_fetched:datetime, data:Optional[dict]):
        if not data:
            return cls()
        
        return cls(
            pk = str(uuid4()),
            company_uid = company_uid,
            description = data.get("description"),
            status = REGISTERED_ENTRY_STATUS.get(data.get("status")),
            registration_date = as_timestamp(data.get("registrationDate")),
            end_date = as_timestamp(data.get("endDate")),
            register = REGISTERED_ENTRY_REGISTER.get(data.get("register")),
            language = data.get("language"),
            authority = REGISTERED_ENTRY_AUTHORITY.get(data.get("authority")),
            data_fetched = data_fetched
        )
    
class BusinessIdChangeModel(Base):
    __tablename__ = "business_id_change"

    pk = Column("pk", String, primary_key=True)
    company_uid = Column("company_uid", String, ForeignKey("company.pk"), nullable=False)
    source = Column("source", String)
    description = Column("description", String)
    reason = Column("reason", String)
    change_date = Column("change_date", DateTime)
    change = Column("change", Integer)
    old_company_number = Column("old_company_number", String)
    new_company_number = Column("new_company_number", String)
    language = Column("language", String)
    data_fetched = Column("data_fetched", DateTime)

    @classmethod
    def from_dict(cls, company_uid:str, data_fetched:datetime, data:Optional[dict]):
        if not data:
            return cls()
        
        return cls(
            pk = str(uuid4()),
            company_uid = company_uid,
            source = convert_source(data.get("source")),
            description = data.get("description"),
            reason = data.get("reason"),
            change_date = as_timestamp(data.get("changeDate")),
            old_company_number = data.get("oldBusinessId"),
            new_company_number = data.get("newBusinessId"),
            language = data.get("language"),
            data_fetched = data_fetched
        )
    
class CompanyLanguageModel(Base):
    __tablename__ = "company_language"

    pk = Column("pk", String, primary_key=True)
    company_uid = Column("company_uid", String, ForeignKey("company.pk"), nullable=False)
    source = Column("source", String)
    version = Column("version", String)
    registration_date = Column("registration_date", DateTime)
    end_date = Column("end_date", DateTime)
    name = Column("name", String)
    language = Column("language", String)
    data_fetched = Column("data_fetched", DateTime)

    @classmethod
    def from_dict(cls, company_uid:str, data_fetched:datetime, data:Optional[dict]):
        if not data:
            return cls()
        
        return cls(
            pk = str(uuid4()),
            company_uid = company_uid,
            source = convert_source(data.get("source")),
            version = convert_version(data.get("version")),
            registration_date = as_timestamp(data.get("registrationDate")),
            end_date = as_timestamp(data.get("endDate")),
            name = data.get("name"),
            language = data.get("language"),
            data_fetched = data_fetched
        )

class Company:
    def __init__(self,
                 names: Optional[list]=None,
                 auxiliaryNames: Optional[list]=None,
                 addresses: Optional[list]=None,
                 companyForms: Optional[list]=None,
                 liquidations: Optional[list]=None,
                 businessLines: Optional[list]=None,
                 languages: Optional[list]=None,
                 registeredOffices: Optional[list]=None,
                 contactDetails: Optional[list]=None,
                 registeredEntries: Optional[list]=None, 
                 businessIdChanges: Optional[list]=None,
                 businessId:Optional[str]=None,
                 registrationDate: Optional[str]=None,
                 companyForm: Optional[str]=None,
                 detailsUri: Optional[str]=None,
                 name: Optional[str]=None,
                 company_uid:str|None=None,
                 **kwargs
                 ) -> None:

        self.company_uid: str = str(uuid4()) if not company_uid else company_uid
        self.data_fetched: datetime = datetime.now()
        self.company_number: Optional[str] = businessId

        self.names = names
        self.auxiliary_names = auxiliaryNames
        self.addresses = addresses
        self.company_forms = companyForms
        self.liquidations = liquidations
        self.business_lines = businessLines
        self.languages = languages
        self.registered_offices = registeredOffices
        self.contact_details = contactDetails
        self.registered_entries = registeredEntries
        self.business_id_changes = businessIdChanges
        self.base_company = {
            "businessId":businessId,
            "registrationDate":registrationDate,
            "companyForm":companyForm,
            "detailsUri":detailsUri,
            "name":name
        }

        self.attribute_model_pairs: list[Tuple[Optional[list], Type]] = [
            (self.names, CompanyNameModel),
            (self.auxiliary_names, CompanyNameModel),
            (self.addresses, AddressModel),
            (self.company_forms, CompanyFormModel),
            (self.liquidations, CompanyLiquidationModel),
            (self.business_lines, BusinessLineModel),
            (self.languages, CompanyLanguageModel),
            (self.registered_offices, RegisteredOfficeModel),
            (self.contact_details, ContactDetailModel),
            (self.registered_entries, RegisteredEntryModel),
            (self.business_id_changes, BusinessIdChangeModel)
        ]

        # Logging the extra key-value pairs that was passed to this class.
        if kwargs:
            my_project_logger.info(f"Extra arguments passed to class: {self.__class__.__name__}, extra arguments: {kwargs}, happened with company: {self.company_uid}")
        
    @staticmethod
    def _create_session():
        output_db_uri = config("POSTGRES_OUTPUT_DB")
        engine = create_engine(output_db_uri)
        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            session.execute(text("SELECT 1"))
            return session
        except Exception as e:
            my_project_logger.error(f"Error creating a session to postgre:{output_db_uri}, message: {str(e)}")
            session.close()
            return False
     
    def _create_model_instance_list(self,
                                    model: Union[
                                        CompanyNameModel,
                                        CompanyFormModel,
                                        CompanyLiquidationModel,
                                        BaseCompanyModel,
                                        BusinessIdChangeModel,
                                        BusinessLineModel,
                                        RegisteredEntryModel,
                                        RegisteredOfficeModel,
                                        AddressModel,
                                        CompanyLanguageModel],
                                    data:Optional[list[dict]|dict]

                                    ) -> list[Union[
                                            CompanyNameModel,
                                            CompanyFormModel,
                                            CompanyLiquidationModel,
                                            BaseCompanyModel,
                                            BusinessIdChangeModel,
                                            BusinessLineModel,
                                            RegisteredEntryModel,
                                            RegisteredOfficeModel,
                                            AddressModel,
                                            CompanyLanguageModel]] | BaseCompanyModel:
        if not data:
            return
        
        if isinstance(data, dict):
            return model.from_dict(self.company_uid, self.data_fetched, data)

        model_list = []
        for data_dict in data:
            model_list.append(model.from_dict(self.company_uid, self.data_fetched, data_dict))

        return model_list

    def to_postgres(self) -> bool:
        session = self._create_session()
        if session is False:
            return False
        
        attribute_model_pairs: list[Tuple[Optional[list], Type]] = [
            (self.names, CompanyNameModel),
            (self.auxiliary_names, CompanyNameModel),
            (self.addresses, AddressModel),
            (self.company_forms, CompanyFormModel),
            (self.liquidations, CompanyLiquidationModel),
            (self.business_lines, BusinessLineModel),
            (self.languages, CompanyLanguageModel),
            (self.registered_offices, RegisteredOfficeModel),
            (self.contact_details, ContactDetailModel),
            (self.registered_entries, RegisteredEntryModel),
            (self.business_id_changes, BusinessIdChangeModel)
        ]

        try:
            # Need to commit the BaseCompanyModel data first due to FK constraints.
            base_instance = self._create_model_instance_list(model=BaseCompanyModel, data=self.base_company)
            session.add(base_instance)
            session.commit()

            for attribute, model in attribute_model_pairs:
                instance_list = self._create_model_instance_list(model=model, data=attribute)
                if not instance_list:
                    continue
                session.add_all(instance_list)

            session.commit()
            return True
        
        except SQLAlchemyError as e:
            my_project_logger.error(f"Error committing models to PostgreSQL, company_uid: {self.company_uid}, company number: {self.company_number}, error message: {str(e)}")
            session.rollback()
            return False
        
        finally:
            session.close()

    def _update_rows(self, session):

        for attribute, model in self.attribute_model_pairs:
            instance_list = self._create_model_instance_list(model=model, data=attribute)
            if not instance_list:
                continue

            existing_rows = session.query(model).filter_by(company_uid=self.company_uid).all()
            for row in existing_rows:
                session.delete(row)

            session.add_all(instance_list)

    def update_postgres(self) -> bool:
        session = self._create_session()
        if session is False:
            return False
        
        try:
            base_instance = self._create_model_instance_list(BaseCompanyModel, self.base_company)
            existing_row = session.query(BaseCompanyModel).filter_by(pk=self.company_uid).first()
            if not base_instance:
                return False
            
            if existing_row:
                session.merge(base_instance)
                session.commit()
            else:
                session.add(base_instance)
                session.commit()
            

            self._update_rows(session)

            session.commit()
            return True

        except Exception as e:
            my_project_logger.error(f"Error committing models to PostgreSQL, company_uid: {self.company_uid}, company number: {self.company_number}, error message: {str(e)}")
            session.rollback()
            return False
        
        finally:
            session.close()

def create_tables():
    address_p = config("POSTGRES_OUTPUT_DB")
    engine = create_engine(address_p)
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)
    session.commit()
    session.close()

