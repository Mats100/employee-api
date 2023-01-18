from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


app = FastAPI()


class Employee_Data(BaseModel):
    name: str
    profession: str
    experience: int


@app.get("/")
def read_api(db: Session = Depends(get_db)):
    return db.query(models.Employees).all()


@app.post("/create-record/")
def create_record(employee: Employee_Data, db: Session = Depends(get_db)):
    employee_model = models.Employees(name=employee.name, profession=employee.profession, experience=employee.experience)

    db.add(employee_model)
    db.commit()
    db.refresh(employee_model)

    return employee_model

@app.put("/update-user/{Id}")
def update_user(Id: int, employee: Employee_Data, db: Session = Depends(get_db)):
    employee_model = db.query(models.Employees).filter(models.Employees.id == Id).first()
    if employee_model is None:
        raise HTTPException(
            status_code=404, detail="User not Found"
        )
    employee_model.name = employee.name
    employee_model.profession = employee.profession
    db.commit()
    db.refresh(employee_model)
    return employee_model

@app.delete("/delete-user/{Id}")
def delete_user(Id: int, db: Session = Depends(get_db)):
    employee_model = db.query(models.Employees).filter(models.Employees.id == Id).first()
    if employee_model is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(employee_model)
    db.commit()
    return {"message": "User deleted Successfully"}