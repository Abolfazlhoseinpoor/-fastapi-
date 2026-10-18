from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field,field_validator
app = FastAPI()
# dar inja iran yani inke in fard dar iran hast ya kheyr (true = dar iran , false = dar iran nis!)
contract = {
    1 : {"name":"Ali","phone_number":"05184945415","email":"Ali896@gmail.com","password":"0915abcd","iran":True},
    2 : {"name":"Hosein","phone_number":"09156487854","email":"Hosein325@gmail.com","password":"155425","iran":False},
    3 : {"name":"Arghavan","phone_number":"09135819612","email":"Arghavn164@gmail.com","password":"nubf477","iran":True},
    4 : {"name":"Hasan","phone_number":"09494845475","email":"Hasan016@gmail.com","password":"48vrev8","iran":True},
    5 : {"name":"Javad","phone_number":"04854781578","email":"Javad189@gmail.com","password":"158rv36b","iran":False},
    6 : {"name":"Sara","phone_number":"04615185387","email":"Sara749@gmail.com","password":"188125qf","iran":False}
}
class Show(BaseModel):
    name : str
    phone_number : str
    email : str

@app.get("/namayesh",response_model=dict[int,Show])
def namayesh_karbaran():
    return contract

@app.get("/namayesh/{karbar}",response_model=Show)
def namayesh_karbar(karbar : str):
    for user in contract.values():
        if karbar == user["name"]:
            return user
    else:
        raise HTTPException(status_code=404,detail="hamchin karbary peyda nashod!")

@app.get("/namayesh/{karbar}/iran")
def namayesh_karbar_dar_iran(karbar : str):
    for user in contract.values():
        if  karbar == user["name"]:
            if user["iran"] == False:
                raise HTTPException(status_code=400,detail="in karbar dar iran nis!!")
            return{
                "message":f"karbar {user["name"]} ba shomare {user["phone_number"]} va ba email: {user["email"]}  dar iran zendegi mikonnd!"
            }
    raise HTTPException(status_code=404, detail="in karbar peyda nashod!")

class new_karbar(BaseModel):
    name : str
    phone_number : str
    email : str
    password : str = Field(min_length=4,max_length=15)
    iran : bool = True


    @field_validator("email")
    def check_email(cls,v):
        if "@" not in v:
            raise ValueError ("@ bayad dar adres email bashad!")
        return v

@app.post("/add_karbar",status_code=201)
def karbar_ezafe(karbar : new_karbar):
    new_id = max(contract.keys())+1
    contract[new_id] = {
        "name": karbar.name,
        "phone_number": karbar.phone_number,
        "email": karbar.email,
        "password": karbar.password,
        "iran": karbar.iran
    }
    return {
        "message" : "karbar ezafe shod!", "id":new_id
    }

                


    


