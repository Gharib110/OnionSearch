from flask import Flask, render_template, request
import subprocess
import datetime
import re
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_query = request.form.get('search_query')
        
        if len(search_query) > 25:
            error_msg = "Search query must be 25 characters or less."
            return render_template('index.html', error=error_msg)
        
        sanitized_query = re.sub(r'\W+', '_', search_query)[:25]
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file_name = f"{sanitized_query}_{timestamp}.txt"
        output_file_path = os.path.join('/opt', output_file_name)
        
        cmd = [
            'onionsearch',
            search_query,
            '--output', output_file_path,
            '--continuous_write', 'True',
            '--proxy', '127.0.0.1:9050'
        ]
        
        try:
            subprocess.run(cmd, check=True, text=True)
            with open(output_file_path, 'r') as f:
                results = f.read()
            return render_template('index.html', search_query=search_query, results=results)
        except subprocess.CalledProcessError as e:
            error_msg = f"An error occurred: {str(e)}"
            return render_template('index.html', error=error_msg)
        except Exception as e:
            error_msg = f"An error occurred while reading the output file: {str(e)}"
            return render_template('index.html', error=error_msg)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)
