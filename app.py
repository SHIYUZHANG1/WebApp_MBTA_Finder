from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Length
from mbta_finder import find_stop_near

app = Flask(__name__)

# Secrete key is require for csrf
app.config['SECRET_KEY']  = "ooiiiiuju76777666655cfdd$$jj99986^^@44"



@app.route('/', methods=['GET', 'POST'])
def find():
    # modify this function so it renders different templates for POST and GET method.
    # aka. it displays the form when the method is 'GET'; it displays the results when
    # the method is 'POST' and the data is correctly processed.
    if request.method == 'POST':
        return 'Hello. Please access this page using a web browser'
    else:
        errormsg = request.args.get('errmsg', '')
        form = FormFinder()
        return render_template('index.html', form=form, errormsg=errormsg)


@app.route('/nearest', methods=['POST', 'GET'])
def find_nearest():
    if request.method == 'GET':
        return redirect(url_for('find', errmsg=''))
    else:
        form = FormFinder()
        if form.validate_on_submit():
            # This is the only aspect we expect error from our app.
            # So it is good we catch the error and send user a better response
            try:
                return nearest_mbta_page()
            except:
                return render_template('error_page.html')

        error_msg = ''
        for field, errors in form.errors.items():
            for errmsg in errors:
                error_msg += f' {field} : {errmsg}  '

        return redirect(url_for('find', errmsg=error_msg))


def nearest_mbta_page():

    place = request.form['place']
    vehicle_type = request.form['vehicle_type']
    radius = request.form['radius']

    station_name, wheelchair_boarding, vehicle_type = find_stop_near(place, vehicle_type, radius)

    wheel_acess = ['No Information', 'Yes', 'No']
    transportation = ['Light Rail', 'Heavy Rail', 'Commuter Rail', 'Bus', 'Ferry']
    wheelcha_acc = wheel_acess[int(wheelchair_boarding)]
    traspn  =  transportation[int(vehicle_type)]

    sdata = (place, station_name, wheelcha_acc, traspn)

    return render_template('mbta_station.html', data=sdata)



class FormFinder(FlaskForm):
    place = StringField('Enter Place Name', [DataRequired(),
                                             Length(min=3, message=('Please enter a valid place name'))])
    vehicle_type = SelectField('Type of Transportation', [],
                               choices=[('', 'No Preference'),
                    ('4', 'Ferry'),
                    ('3', 'Bus'),
                    ('2', 'Commuter Rail'),
                    ('1', 'Heavy Rai'),
                    ('0', 'Light Rail')])

    radius = SelectField('Find within:', [DataRequired()],
                               choices=[('0.01', 'Half mile'),
                                        ('0.02', '1 mile'),
                                        ('0.04', '2 mile'),
                                        ('0.1', '5 mile'),
                                        ('0.2', '10 mile'),
                                        ('0.4', '20 mile')])
