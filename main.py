from datetime import date
from pydantic import BaseModel, EmailStr, Field, model_validator

class Person(BaseModel):
    id: int = Field(default=1, description="nniq id")
    name: str = Field(
        default="first_name + last_name",
        min_length=5,
        max_length=100
    )
    b_date: date = Field(default=date(2000, 1, 1))
    email: str = Field(pattern=r"[^@]+@utmn.ru")


    age: int 

    @model_validator(mode="after")
    def validate_age(self):
        pass






class Student(Person):
    score: int = Field(ge=80, le=300)





if __name__ == "__main__":
    
    # person_1 = Person(id=1, name="maxim", b_date="2002-02-11", email="sdfdf@utmn.ru")

    student_1 = Student(id=1, name="maxim", b_date="2002-02-11", email="sdfdf@utmn.ru", score=81)

    # print(person_1)
    print(student_1)