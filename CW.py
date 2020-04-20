from flask import Flask, render_template, request, jsonify
from cassandra.cluster import Cluster
import json
import requests
import requests_cache

requests_cache.install_cache('crime_api_cache', backend='sqlite', expire_after=36000)
cluster = Cluster(contact_points=['172.17.0.2'],port=9042)
session = cluster.connect()

app = Flask(__name__)

stop_search_template = 'https://data.police.uk/api/stops-street?lat={lat}&lng={lng}'
@app.route('/stop_and_search_area', methods=['GET'])
def stop_and_search():
    my_lat = request.args.get('lat','52.629729')
    my_lng = request.args.get('lng','-1.131592')
    stop_search_url = stop_search_template.format(lat = my_lat, lng = my_lng)
    resp = requests.get(stop_search_url)
    if resp.ok:
        return jsonify(resp.json()),200
    else:
        return jsonify({'Error':'No stop and searches were recorded on this date'}), 404

@app.route('/stop_and_search/<id>', methods=['GET'])
def stop_and_search_get(id):
    id = int(id)
    rows = session.execute( """Select * From stop_and_search_2.stats where id = {}""".format(id))
    for row in rows:
        return jsonify('<h1>{} has gender {}!</h1>'.format(id,row.gender))
    return jsonify('<h1>Error: That entry doesn\'t exist!</h1>'),404

@app.route('/stop_and_search/<id>', methods=['POST'])
def stop_and_search_post(id):
    id = int(id)
    rows = session.execute("""Select * From stop_and_search_2.stats where id = {}""".format(id))
    for row in rows:
            rows = session.execute("""Insert into stop_and_search_2.stats (id,gender) values ({},'Female')""".format(id))
        else:
            return jsonify('<h1>Error: The ID {} already exists</h1>'.format(id)),404
    return jsonify('<h1>Success: ID {} has been created!</h1>'.format(id)),201


@app.route('/stop_and_search/<id>/<gender>', methods=['PUT'])
def stop_and_search_put(id,gender):
    id = int(id)
    rows = session.execute("""Select * From stop_and_search_2.stats where id = {}""".format(id))
    for row in rows:
        if len(row)==0:
            return jsonify('<h1>Error: The ID {} doesn\'t exists</h1>'.format(id)),404
        else:
            rows = session.execute("""Update stop_and_search_2.stats Set gender='{}' where id = {}""".format(gender,id))
            return jsonify('<h1>Success: ID {} has been updated to gender {}!</h1>'.format(id,gender)),200

@app.route('/stop_and_search/<id>', methods=['DELETE'])
def stop_and_search_delete(id):
    id = int(id)
    rows = session.execute("""Select * From stop_and_search_2.stats where id = {}""".format(id))
    for row in rows:
        if len(row)==0:
            return jsonify({'Error: This ID doesn\'t exist'}),404
        else:
            rows = session.execute("""Delete From stop_and_search_2.stats where id = {}""".format(id))
            return jsonify('<h1>Success: ID {} has been deleted!</h1>'.format(id)),200

if __name__=="__main__":
    app.run(host='0.0.0.0', debug=True)
