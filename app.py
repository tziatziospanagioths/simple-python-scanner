from flask import Flask, request, render_template
import scanner  

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    target = None
    
    if request.method == 'POST':
        
        target = request.form.get('url_input')
        
        
        result = "Scan initiated for: " + target
        
    return render_template('index.html', scan_result=result, url=target)

if __name__ == '__main__':
    app.run(debug=True)