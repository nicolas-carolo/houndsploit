from flask import Flask, render_template, request
from searcher.engine.search_engine import search_vulnerabilities_in_db

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def get_results_table():
    if request.method == 'POST':
        searched_text = request.form['searched-text']
        exploits_list = search_vulnerabilities_in_db(searched_text, 'searcher_exploit')
        for result in exploits_list:
            if result.port is None:
                result.port = ''
        shellcodes_list = search_vulnerabilities_in_db(searched_text, 'searcher_shellcode')
        return render_template('results_table.html', searched_item=searched_text,
                               exploits_list=exploits_list, shellcodes_list=shellcodes_list,
                               searched_text=searched_text)
    else:
        return render_template('home.html')


if __name__ == '__main__':
    app.run()
