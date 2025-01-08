import json
from django.shortcuts import render, redirect
from enroll.models import User
from django.contrib import messages
import numpy as np
import pandas as pd
import pickle



# Create your views here.

def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')


def signupuser(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if pass1 !=pass2:
            messages.error(request,"password do not match")
            return redirect('signup')

        # Check if the username and email are unique
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('signup')

        else:
            # Create a new User object and save it
            user = User(username=username, fname=fname, lname=lname, email=email, pass1=pass1, pass2=pass2)
            user.save()

        # Redirect to the login page after successful registration
        messages.error(request, f"Hello {username}, You are registered successfully")
        return redirect('login')
    else:
        return render(request,'signup.html')

def loginuser(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = User.objects.filter(username=username, pass1=pass1).first()
        if user:
            # Set the User ID in the session to keep the User logged in
            request.session['User_id'] = user.id
            messages.error(request, "Logged in successfully")
            return redirect('home')

        user = User.objects.filter(email=username,pass1=pass1).first()
        if user:
            # Set the User ID in the session to keep the User logged in
            request.session['User_id'] = user.id
            messages.error(request, "Logged in Successfully")
            return redirect('home')

        return render(request, 'login.html', {'error': 'Invalid Email/Username or password'})

    # return render(request, 'login.html')
    return render(request,'login.html')

def logoutuser(request):
    request.session.flush()  # Ends the session and clears all session data
    messages.success(request, "Successfully logged out!")
    return redirect('index')  # Redirects to the URL named 'index'


def home(request):
    return render(request,'home.html')


def users(request):
    obj = User.objects.all()
    context = {
        'obj':obj
    }
    return render(request,'users.html',context)

def predict(request):
    if request.method == "POST":
        model = pickle.load(open('models/churn_prediction_model.pkl','rb'))
        
        with open("models/columns.json", "r") as f:
            data_columns = json.load(f)['data_columns']

        input_features = [

            request.POST['Tenure'],
            request.POST['Citytier'],
            request.POST['Warehousetohome'],
            request.POST['Gender'],
            request.POST['Hourspendonapp'],
            request.POST['Numberofdeviceregistered'],
            request.POST['Satisfactionscore'],
            request.POST['Maritalstatus'],
            request.POST['Numberofaddress'],
            request.POST['Complain'],
            request.POST['Orderamounthikefromlastyear'],
            request.POST['Couponused'],
            request.POST['Ordercount'],
            request.POST['Daysincelastorder'],
            request.POST['Cashbackamount']

        ]
        features_value = [np.array(input_features)]



        features_name = ["tenure",
                         "citytier",
                         "warehousetohome",
                        "gender",
                        "hourspendonapp",
                        "numberofdeviceregistered",
                        "satisfactionscore",
                        "maritalstatus",
                        "numberofaddress",
                        "complain",
                        "orderamounthikefromlastyear",
                        "couponused",
                        "ordercount",
                        "daysincelastorder",
                        "cashbackamount"
                        ]


        df = pd.DataFrame(features_value, columns=features_name)

        # One-hot encode categorical variables
        for col in data_columns:
            if col in df and isinstance(df[col], str):
                df[col] = df[col].lower().replace(' ', '_')

        # Create a list of zeros for all columns
        input_array = np.zeros(len(data_columns))

        # Fill the input array with the values from df
        for i, col in enumerate(data_columns):
            if col in df:
                input_array[i] = df[col]
            elif col in df.keys():
                # One-hot encode the categorical variables
                if f"{col}_{df[col]}" in data_columns:
                    input_array[data_columns.index(f"{col}_{df[col]}")] = 1

        output_probab = model.predict_proba([input_array])[0][1]

        pred = "Churn" if output_probab > 0.4 else "Not Churn"

        context = {
            'prediction': pred,
            'predict_probabality': output_probab
        }

        return render(request,'result.html',context)

    return render(request, 'predict.html')
