from flask import Flask,render_template,url_for,request
import joblib, sklearn

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/prediction',methods=['POST','GET'])
def prediction():
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

    if Class_type == 'Eco':
        Class_Eco =1
        Class_Eco_Plus =0
    
    elif Class_type == 'Eco_Plus':
        Class_Eco=0
        Class_Eco_Plus=1

    else:
        Class_Eco=0
        Class_Eco_Plus=0



    UNSEEN_DATA = [[age,flight_distance,inflight_entertainment,baggage_handling,clininess,depart_delay,arrival_delay,gender,customer_type,travel_type,Class_Eco,Class_Eco_Plus]]

    model = joblib.load('static/icons/LogisticRegression.lb')

    prediction = model.predict(UNSEEN_DATA)[0]
    print(prediction)

    labels = {'1':'Satisfied','0':'unsatisfied'}

    # return labels[str(prediction)]
    return render_template('output.html',output=labels[str(prediction)])



if __name__ == "__main__":
    app.run(debug=True)