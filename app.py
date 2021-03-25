from flask import Flask ,render_template,request
import requests
import numpy as np
import pickle
app = Flask(__name__)
model = pickle.load(open('C:/miniconda/Conda/envs/myenv/car_price/car_price1.pkl', 'rb'))
@app.route('/',methods=['GET'])
def home():
    return render_template('d:templates/car_price.html')

@app.route('/prediction',methods=['POST'])
def predict():
    Fuel_Type_Diesel = 0
    if (request.method)=='POST':
        Years_Driven = int(request.form['Years_Driven'])
        Kms_Driven = int(request.form['Kms_Driven'])
        Kms_Driven2=np.log(Kms_Driven)
        Present_Price = int(request.form['Present_Price'])
        Owner = int(request.form['Owner'])
        
        Fuel_Type_Petrol = request.form['Fuel_Type_Petrol']
        if Fuel_Type_Petrol=='Petrol':
            Fuel_Type_Petrol=1
            Fuel_Type_Diesel=0
        elif Fuel_Type_Petrol=='Diesel':
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=1
        else:
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=0
        Years_Driven = 2021 - Years_Driven
        Seller_Type_Individual = request.form['Seller_Type_Individual']
        if Seller_Type_Individual == 'Individual':
            Seller_Type_Individual=1
        else:
            Seller_Type_Individual=0
        Transmission_Manual = request.form['Transmission_Manual']
        if Transmission_Manual=='Manual':
            Transmission_Manual = 1
        else:
            Transmission_Manual = 0
        predictions = model.predict([[Present_Price,Kms_Driven2,Owner,Years_Driven,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Manual]])
        output = round(predictions[0],2)
        if output<0:
            return render_template('d:templates/car_price.html',predictions_text="Sorry,You can't sell this car")
        else:
            return render_template("d:templates/car_price.html",predictions_text='Your car price is {}'.format(output))
    else:
        return render_template('d:templates/car_price.html')
if __name__ == '__main__':
    app.run()