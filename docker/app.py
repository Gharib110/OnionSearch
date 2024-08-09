from flask import Flask, render_template, request
import subprocess
import datetime
import re
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the search query from the form
        search_query = request.form.get('search_query')
        
        # Limit the search query to 25 characters
        if len(search_query) > 25:
            error_msg = "Search query must be 25 characters or less."
            return render_template('index.html', error=error_msg)
        
        # Generate a sanitized version of the search query to use in the file name
        sanitized_query = re.sub(r'\W+', '_', search_query)[:25]
        
        # Generate the output file name with the current date and time
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file_name = f"{sanitized_query}_{timestamp}.txt"
        output_file_path = os.path.join('/opt', output_file_name)
        
        # Construct the command to run OnionSearch with the search query and proxy
        cmd = [
            'onionsearch',
            search_query,
            '--output', output_file_path,
            '--continuous_write', 'True',
            '--proxy', '127.0.0.1:9050'  # Add the proxy argument
        ]
        
        try:
            # Run the command and wait for it to complete
            subprocess.run(cmd, check=True, text=True)
            
            # Read the output file and capture its contents
            with open(output_file_path, 'r') as f:
                results = f.read()
            
            # Render the results in the HTML template
            return render_template('index.html', search_query=search_query, results=results)
        except subprocess.CalledProcessError as e:
            # Handle any errors that occur during the search
            error_msg = f"An error occurred: {str(e)}"
            return render_template('index.html', error=error_msg)
        except Exception as e:
            # Handle any file reading errors
            error_msg = f"An error occurred while reading the output file: {str(e)}"
            return render_template('index.html', error=error_msg)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
