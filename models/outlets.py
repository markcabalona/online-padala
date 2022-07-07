from pydantic import BaseModel


class OutletModel(BaseModel):
    address:str
    service_fee:float

class CreateOutlet(OutletModel):
    pass

class Outlet(OutletModel):
    outlet_num:str
    
        