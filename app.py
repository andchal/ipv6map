from rangetree import RangeTree, BBox, Point, readPointFile, GeometryException
from flask import Flask, jsonify, make_response, request, render_template

import os

app = Flask(__name__)

points = readPointFile(os.path.join(os.path.dirname(__file__), 'data/ipv6data.csv'))
tree = RangeTree()
tree.create(points)

@app.route('/ipv6/api/v1.0/locations', methods=['GET'])
def get_points():
    try:
        args= request.args.to_dict()
        bbox = BBox(float(args['lowerx']), float(args['lowery']), float(args['upperx']), float(args['uppery']))
    except GeometryException:
        return make_response('Geometry Exception: invalid bounding box', 400)
    except TypeError:
        return make_response('Invalid inputs.  Please use float args for lowerx, lowery, upperx, uppery', 400)
    return jsonify([p.heatPoint() for p in tree.bboxQuery(bbox)])

@app.route('/ipv6/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)