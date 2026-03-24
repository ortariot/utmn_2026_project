from typing import Annotated

from datetime import date
from pydantic import BaseModel, EmailStr, Field, model_validator, field_validator, computed_field, PlainSerializer

class Person(BaseModel):
    id: int = Field(default=1, description="nniq id")
    name: str = Field(
        default="first_name + last_name",
        min_length=5,
        max_length=100
    )
    b_date: date = Field(default=date(2000, 1, 1))
    email: str = Field(pattern=r"[^@]+@utmn.ru")

    desc: Annotated[
        str,
        Field(max_length=50, default="super user", examples=""),
        PlainSerializer(lambda x: x.upper(), return_type=str),
        PlainSerializer(lambda x: x.lower(), return_type=str)
    ] 


    # age: int 

    @model_validator(mode="after")
    def validate_age(self):
        today = date.today()

        age = today.year - self.b_date.year - ((today.month, today.day) < (self.b_date.month, self.b_date.day))

        if age < 18:
            raise ValueError("user must be over 18 years")
        elif age > 120:
            raise ValueError("user must be under 120 years")
        else:
            return self
        
    
    @field_validator("name", mode="before")
    def validate_name(cls, v):

        if isinstance(v, str):
            return v
        elif isinstance(v, int):
            return str(v)
        else:
            ValueError("mame must be str or int")

    @computed_field(return_type=int)
    def age(self):

        today = date.today()

        age = today.year - self.b_date.year - ((today.month, today.day) < (self.b_date.month, self.b_date.day))

        return age



class Student(Person):
    score: int = Field(ge=80, le=300)





if __name__ == "__main__":
    
    # person_1 = Person(id=1, name="maxim", b_date="2002-02-11", email="sdfdf@utmn.ru")

    student_1 = Student(id=1, name=1224565, b_date="2002-02-11", email="sdfdf@utmn.ru", score=81)

    # print(person_1)
    print(student_1.model_dump())