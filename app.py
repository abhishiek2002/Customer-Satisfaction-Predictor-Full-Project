from flask import Flask,render_template,url_for,request
import joblib, sklearn
import mysql.connector as mc
import numpy as np

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/prediction',methods=['POST','GET'])
def prediction():


    # receiving data from form

    if request.method == "POST":
        age = int(request.form['age'])
        flight_distance = int(request.form['distance'])
        inflight_entertainment = int(request.form['entertainment'])
        baggage_handling = int(request.form['Handling'])
        clininess = int(request.form['clininess'])
        depart_delay = int(request.form['delay'])
        arrival_delay = int(request.form['arr_delay'])
        gender = int(request.form['sex'])
        customer_type = int(request.form['cust_type'])
        travel_type = int(request.form['trv_type'])
        Class_type = request.form['class']

        # changing class type data into int from string

        if Class_type == 'Eco':
            Class_Eco =1
            Class_Eco_Plus =0
        
        elif Class_type == 'Eco_Plus':
            Class_Eco=0
            Class_Eco_Plus=1

        else:
            Class_Eco=0
            Class_Eco_Plus=0

        # creating a tuple to store form data

        UNSEEN_DATA = (age,flight_distance,inflight_entertainment,baggage_handling,clininess,depart_delay,arrival_delay,gender,customer_type,travel_type,Class_Eco,Class_Eco_Plus)

        # loading or uploading trained model in the app.py file

        model = joblib.load('static/icons/LogisticRegression.lb')


        # converting unseen_data into 2d array because model will accept only 2d array 

        # UNSEEN_DATA_2d = [[age,flight_distance,inflight_entertainment,baggage_handling,clininess,depart_delay,arrival_delay,gender,customer_type,travel_type,Class_Eco,Class_Eco_Plus]]

        # or

        UNSEEN_DATA_2d = np.array([UNSEEN_DATA])
        

        # predicting customer satisfaction using model

        prediction = model.predict(UNSEEN_DATA_2d)[0]
        print(prediction)

        # because prediction is in 0 or 1 means unsatisfied or satisfied . That's why changing it into understandable form

        labels = {'1':'Satisfied','0':'unsatisfied'}

        # connecting to mysql database

        connect = mc.connect(host='localhost', user='root', password = 'Abhishek@2002', database='lr_userdata')



        insert_data = """
        insert into data(age,flight_distance,inflight_entertainment,baggage_handling,clininess,depart_delay,arrival_delay,gender,customer_type,travel_type,Class_Eco,Class_Eco_Plus,customer_satisfaction_prediction) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        # adding a new column customer satisfaction prediction in unseen_data

        UNSEEN_DATA = (age,flight_distance,inflight_entertainment,baggage_handling,clininess,depart_delay,arrival_delay,gender,customer_type,travel_type,Class_Eco,Class_Eco_Plus,labels[str(prediction)])

        # creating cursor to execute sql query

        cur = connect.cursor()

        # inserting data into table name "data" of database "lr_userdata"

        cur.execute(insert_data,UNSEEN_DATA)

        print("You successfully inserted")
        connect.commit()
        cur.close()
        connect.close()

        # return labels[str(prediction)]
        return render_template('output.html',output=labels[str(prediction)])



        # prediction = model.predict(UNSEEN_DATA)[0]
        # print(prediction)

        # labels = {'1':'Satisfied','0':'unsatisfied'}

        # # return labels[str(prediction)]
        # return render_template('output.html',output=labels[str(prediction)])



if __name__ == "__main__":
    app.run(debug=True)