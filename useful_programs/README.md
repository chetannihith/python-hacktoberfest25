# Useful Programs

Small collection of handy CLI utilities.

Files:
- `cli_calculator.py` — safe arithmetic evaluator
- `file_organizer.py` — move files into folders by extension
- `json_pretty.py` — pretty-print JSON from file or stdin
- `simple_http_server.py` — serve current directory over HTTP
- `smoke_test.py` — quick checks to verify the scripts run

Usage examples:

python cli_calculator.py "(2+3)*4"
python file_organizer.py /path/to/folder
cat file.json | python json_pretty.py
python simple_http_server.py 8080
