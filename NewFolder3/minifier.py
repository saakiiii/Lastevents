from jsmin import jsmin

with open('static/js/..js', 'r') as file:
    minified = jsmin(file.read())
    
with open('static/js/.1.js', 'w') as file:
    file.write(minified)