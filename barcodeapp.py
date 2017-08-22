from flask import Flask, render_template, request, send_file
import barcode
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('HTML_form.html')

@app.route('/barcodegenerator', methods = ['GET', 'POST'])
def barcodegenerator():
    location = request.args.get('location')
    CODE128 = barcode.get_barcode_class('code128')
    from barcode.writer import ImageWriter
    code128 = CODE128(location, writer=ImageWriter())
    fullname = code128.save('code128_barcode')
    return send_file(fullname)
    
def is_location_valid(location):
    location_format = re.compile('\d{3} [A-Z] \d{3} [A-Z]\d')
    result = location_format.match(location)
    if result:
        return True
    return False

@app.route('/barcodegenerator/upload', methods = ['POST'])
def upload():
    uploaded_file = request.files['datafile']
    pasted_locations = request.form['pasted_locations']
    if uploaded_file:
        locations = uploaded_file.readlines()
    elif pasted_locations:
        locations = pasted_locations.splitlines()
    else:
        locations = [request.form['location']]
    valid_locations = filter(is_location_valid, locations)
    invalid_locations = [x for x in locations if x not in valid_locations]
    return render_template('locatii.html', entries = valid_locations, invalid_locations = invalid_locations)
    
  
if __name__ == '__main__':
    app.run(debug = True)
