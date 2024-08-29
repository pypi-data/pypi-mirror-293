from pydantic import Extra, HttpUrl, EmailStr
from typing import Tuple, List, Optional, Dict
from redis_om import JsonModel, Field
from datetime import date


### Models for Kiwi
class Product(JsonModel):
    product_id: str = Field(..., description="Unique identifier for the product", index=True)
    name: str = Field(..., description="Name of the product", index=True)
    description: str = Field(..., description="Description of the product")
    #company: str = Field(..., description="company that offers the product")
    category: Optional[str] = Field(None, description="Category the product belongs to")
    price: Optional[float] = Field(None, description="Price of the product")
    currency: Optional[str] = Field(None, description="Currency for the price")
    stock_quantity: Optional[int] = Field(None, description="Number of items in stock")
    sku: Optional[str] = Field(None, description="Stock Keeping Unit identifier")
    manufacturer: Optional[str] = Field(None, description="Manufacturer of the product")
    warranty: Optional[str] = Field(None, description="Warranty period for the product")
    dimensions: Optional[List[str]] = Field([], description="Dimensions of the product (length, width, height)")
    weight: Optional[float] = Field(None, description="Weight of the product")
    color: Optional[str] = Field(None, description="Color of the product")
    release_date: Optional[date] = Field(None, description="Release date of the product")
    end_of_life_date: Optional[date] = Field(None, description="End of life date of the product")
    download_url: Optional[HttpUrl] = Field(None, description="URL to download the product, if applicable")
    documentation_url: Optional[HttpUrl] = Field(None, description="URL to the documentation, if applicable")
    features: Optional[Dict[str, str]] = {}

    def get_summary(self):
        return '\n'.join({f"{k.upper()} : {v}" for k,v in self.dict().items() if v and k!='pk' and type(v)!=list})

    def __str__(self):
        return '\n'.join({f"{k.upper()} : {v}" for k,v in self.dict().items() if v and k!='pk' and type(v)!=list})

    def get_long_description(self):
        summary = self.get_summary()
        features = "\nFEATURES: \n"+"\n".join(f"{k} : {v}" for k,v in self.features) if self.features else ""
        return summary+features

class Service(JsonModel):
    service_id: str = Field(..., description="Unique identifier for the service", index=True)
    name: str = Field(..., description="Name of the service", index=True)
    description: str = Field(..., description="Description of the service")
    #company: str = Field(..., description="company that offers the service")
    category: Optional[str] = Field(None, description="Category the service belongs to")
    price: Optional[float] = Field(None, description="Price of the service")
    currency: Optional[str] = Field(None, description="Currency for the price")
    availability: Optional[str] = Field(None, description="Availability status of the service")
    provider: Optional[str] = Field(None, description="Provider of the service")
    contact_email: Optional[EmailStr] = Field(None, description="Contact email for the service provider")
    contact_phone: Optional[str] = Field(None, description="Contact phone number for the service provider")
    website: Optional[HttpUrl] = Field(None, description="Website URL for the service")
    service_area: Optional[str] = Field(None, description="Geographical area where the service is offered")
    service_start_date: Optional[date] = Field(None, description="Start date of the service availability")
    service_end_date: Optional[date] = Field(None, description="End date of the service availability")
    features: Optional[Dict[str, str]] = {}

    def get_long_description(self):
        summary = self.get_summary()
        features = "\nFEATURES: \n"+"\n".join(f"{k} : {v}" for k,v in self.features) if self.features else ""
        return summary+features
    
    def get_summary(self):
        return '\n'.join({f"{k.upper()} : {v}" for k,v in self.dict().items() if v and k!='pk' and type(v)!=list})
        
    def __str__(self):
        return '\n'.join({f"{k.upper()} : {v}" for k,v in self.dict().items() if v and k!='pk' and type(v)!=list})

class Company(JsonModel, extra=Extra.allow):
    name: str = Field(index=True)
    vision: str | None = None
    mission: str | None = None
    description: str | None = None
    company_culture: str | None = None
    values: Dict[str, str] = {}
    industry: str | None = None
    founded: str | None = None
    num_employees: int|None = None
    headquarters: str | None = None
    website: HttpUrl | None = None
    email: EmailStr | None = None 
    phone: str | None = None
    other_addresses: List[str] = []
    social_media: Dict|None = None

    products: List[str] = []
    services: List[str] =[]


    def get_contact_info(self) -> str:
        contact_info = f"Email: {self.email}, Phone: {self.phone}, Website: {self.website}"
        return contact_info

    def get_summary(self) -> str:
        summary = [
            f"Company Name: {self.name}\n",
            f"Industry: {self.industry}\n",
            f"Founded: {self.founded}\n",
            f"Number of Employees: {self.num_employees}\n",
            f"Headquarters: {self.headquarters}\n",
            f"Website: {self.website}\n",
            f"Description: {self.description}\n",
        ]
        summary = [i for i in summary if 'None' not in i]
        return "".join(summary)

    
    def get_description(self) -> str:
        return '\n'.join({f"{k.upper()} : {v}" for k,v in self.dict().items() if v and k not in ('pk', 'products', 'services')})

    def get_long_description(self) -> str:
        products_descriptions, services_descriptions = "", ""
        products = [Product.find(Product.pk==p).first() for p in self.products]
        services = [Service.find(Service.pk==s).first() for s in self.services]
        if products:
            products_descriptions = "\nPRODUCTS:\n"+"\n".join(p.get_long_description() for p in products)
        if services:
            services_descriptions = "\nSERVICES\n"+"\n".join(s.get_long_description() for s in services)
            
        return self.get_description()+products_descriptions+services_descriptions
        
    def __str__(self):
        return '\n'.join({f"{k.upper()} : {v}" for k,v in self.dict().items() if v and k!='pk'})


