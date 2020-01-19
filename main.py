from flask import Flask, render_template, url_for, redirect
from reader import get_current_data, get_historic_data, ABBR_TO_FULL, ABBRS

app = Flask(__name__, static_folder='web/static', template_folder='web/templates')


def get_nav_active(item):
    return {'summary': '', 'map': '', item: 'active'}


@app.route("/")
def home():
    return redirect(url_for("summary"))


@app.route("/summary")
def summary():
    data = get_current_data()
    table_data = []
    for abbr in data:
        table_data += [{'abbr': abbr, 'province': ABBR_TO_FULL[abbr], 'demand': f"{data[abbr]['Demand']:.2f}", 'time': data[abbr]['Time']}]
    bar_graph_data = {'labels': ", ".join([f"'{abbr}'" for abbr in ABBRS]),
                      'demands': ", ".join([f"{record['Demand']}" for _, record in data.items()])}

    return render_template("summary.html",
                           table_data=table_data,
                           bar_graph_data=bar_graph_data,
                           nav_active=get_nav_active('summary'))


@app.route("/canada_map")
def canada_map():
    data = get_current_data()

    # Add a comma
    for abbr in data:
        data[abbr]['Demand'] = f"{data[abbr]['Demand']:,.0f}"

    return render_template("canada_map.html", nav_active=get_nav_active('canada_map'), data=data)


@app.route("/history/<abbr>")
def history(abbr):
    data = get_historic_data(abbr)[-20:]  # Fetch last 20 entries
    return render_template("history.html", nav_active=get_nav_active(abbr), abbr=abbr, province=ABBR_TO_FULL[abbr], data=data)


# jsonify

if __name__ == '__main__':
    app.run(debug=True)
