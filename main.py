from flask import Flask, jsonify, request, render_template
from bkcharts import Line, Scatter
from bokeh.resources import CDN
from bokeh.embed import components, autoload_static
from constants import SUBJECTS_SHORT_TO_LONG, SUBJECTS_LONG_TO_SHORT, YEARS, THRESHOLDS
from analyze import Analysis

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template(
        'hello.html',
        courses=list(SUBJECTS_LONG_TO_SHORT.keys()),
    )


@app.route('/api/change_graph')
def change_graph():
    stat = request.args.get('stat', '', type=str)
    th = request.args.get('threshold', '', type=int)
    after_scaling = bool(request.args.get('after_scaling', 1, type=int))
    module_long = request.args.get('module', '', type=str)
    module = SUBJECTS_LONG_TO_SHORT[module_long]
    modules = list(SUBJECTS_SHORT_TO_LONG.keys())
    module_index = modules.index(module)
    plot = create_figure(stat, module_index, th, after_scaling)
    script, div = components(plot)
    return jsonify({
        'graph_script': script,
        'graph_div': div,
    })

@app.route('/api/module_data')
def course_data_formatted():
    module_long = request.args.get('module', '', type=str)
    module = SUBJECTS_LONG_TO_SHORT[module_long]
    threshold = request.args.get('threshold', 70, type=int)
    an = Analysis()
    modules = list(SUBJECTS_SHORT_TO_LONG.keys())
    module_index = modules.index(module)
    after_scaling = True
    res = an.display_subject(module_index, threshold=threshold, after_scaling=after_scaling)

    # bokeh plot
    plot = create_figure('Above ' + str(threshold), module_index, threshold, after_scaling)
    script, div = components(plot)
    return jsonify({
        'text': res['description'].replace('\n', '<br>'),
        'df': res['df'].to_html(classes=['stats', 'table', 'table-responsive'], float_format=lambda x: '%10.3f' % x),
        'describe_df': res['df'].describe().to_html(classes=['stats', 'table', 'table-responsive'], float_format=lambda x: '%10.3f' % x),
        'graph_script': script,
        'graph_div': div,
    })


@app.route('/api/module/<module>', methods=['GET'])
def course_data(module):
    ret = {}
    an = Analysis()
    modules = list(SUBJECTS_SHORT_TO_LONG.keys())
    module_index = modules.index(module)
    module_data = an.histograms[module_index]
    print(module_index)
    print(module_data)
    for idx, year in enumerate(YEARS):
        ret[year] = {}
        if not isinstance(module_data[idx], list):
            ret[year] = "Not Found"
            continue
        for th_idx, th in enumerate(THRESHOLDS):
            range_str = "{}-{}".format(th, th + 9)
            ret[year][range_str] = {}
            ret[year][range_str]['scaled'] = module_data[idx][th_idx][0]
            ret[year][range_str]['unscaled'] = module_data[idx][th_idx][1]

    return jsonify(ret)


def create_figure(current_stat, subject, threshold, after_scaling):
    an = Analysis()
    df = an.display_subject(subject, threshold, after_scaling)['df']
    p = Scatter(df, x='index', y=current_stat, title=current_stat,
            legend='top_right', sizing_mode = 'scale_width', height=400)
    p.xaxis.axis_label = 'Years'
    p.yaxis.axis_label = current_stat
    return p


if __name__ == "__main__":
    app.run(debug=True)
