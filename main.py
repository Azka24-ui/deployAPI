#import library
from fastapi import FastAPI, HTTPException, Header
import pandas as pd 

#create object / intansce for FastAPI
app = FastAPI()

#create endpoint home
@app.get("/")
def home(): 
    return {"message": "Selamat datang di toko pak icad!"}

# create endpoint data
@app.get("/data")
def read_data():
    # read data from file csv
    df = pd.read_csv("data.csv")
    # mengembalikan data
    return df.to_dict(orient="records") #to dict = untuk merubah df ke JSON/DICT / DICTIONARY
# create endpoint data with number of parameter id 
@app.get("/data/{number_id}")
def read_item(number_id: int):
    # read data from file csv
    df = pd.read_csv("data.csv")

    #filter data by id
    filter_data = df[df["id"] == number_id]
    if len(filter_data) == 0:
        raise HTTPException(status_code=404, detail="waduh, data yang lu cari gada bro ,maap")
    return filter_data.to_dict(orient="records")


#create API key
API_Key = "hck024data"

#create endpoint update file csv data
@app.put("/items/{number_id}")
def update_item(number_id: int, nama_barang: str, harga: float):
    # create dict for update data
    df = pd.read_csv("data.csv")

    #create data from update input 
    updated_df = pd.DataFrame([{
        "id": number_id,
        "nama_barang": nama_barang,
        "harga": harga
    }])

    # merge upload dataframe with original dataframe
    df = pd.concat([df, updated_df], ignore_index=True)
    df.to_csv("data.csv", index=False)
    return {"message": f"Item with name {number_id} has been updated successfully."}

@app.get("/secret")
def read_secret (api_key: str = Header(None)):
    # from data csv
    secret_df = pd.read_csv("secret_data.csv")

    if api_key != API_Key:
        # jika api key is not valid return error
        raise HTTPException(status_code=401, detail="API_Key tidak valid.")
    return secret_df.to_dict(orient="records")

