from flask import Flask, request, render_template
import scanner  

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    result_data = None
    target_url = None
    
    if request.method == 'POST':
        
        target_url = request.form.get('url_input')
        
        if target_url:
            
            result_data = scanner.check_headers(target_url)
            
    
    return render_template('index.html', result=result_data)

if __name__ == '__main__':
    app.run(debug=True)