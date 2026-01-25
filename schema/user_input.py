
from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Literal, Annotated


# pydantic model to validate incoming data
class UserInput(BaseModel):

    title: Annotated[str, Field(...,  description='Job Title')]
    requirements: Annotated[str, Field(..., description='Requirements for the job')]
    company_profile: Annotated[str, Field(..., description='1-2 line about the company')]
    description: Annotated[str, Field(..., description='Company Description')]
    industry: Annotated[literal['Marketing_and_Advertising', 'Computer_Software' , 'Hospital_&_Health Care'], Field(..., description='Which industry the job belongs to')]
    benefits: Annotated[str, Field(..., description='Benefits provided by the company')]
    salary_range: Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'], Field(..., description='Occupation of the user')]
    location: Annotated[str, Field(..., description='The city that the user belongs to')]
    employment_type: Annotated[str, Field(..., description='The city that the user belongs to')]
    
    
    @field_validator('city')
    @classmethod
    def normalize_city(cls, v: str) -> str:
        v = v.strip().title()
        return v
    
    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight/(self.height**2)
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"
        
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"
    
    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3
