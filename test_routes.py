import re
with open('main.py') as f:
    for line_num, line in enumerate(f, 1):
        if '@app.get' in line:
            match = re.search(r'@app\.get\("([^"]+)"\)', line)
            if match:
                route = match.group(1)
                print(f"{route}")
