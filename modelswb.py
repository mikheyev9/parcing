from pydantic import BaseModel, root_validator

#need this keys from json
#['id', 'name', 'price', 'brand', 'sales_count', 'raiting', 'have_now']

class WB_items(BaseModel):
    id: int
    name: str
    salePriceU: float
    brand: str
    sale: int
    rating: int
    volume: int 

    @root_validator(pre=True)
    def convert_price(cls, values:dict):
        price = values.get('salePriceU')
        if price is not None:
            values['salePriceU'] = price / 100
        return values

class Main_box(BaseModel):
    products: list[WB_items]


