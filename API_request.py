from flask import Flask, render_template, request, jsonify
import json
import requests
import requests_cache

requests_cache.install_cache('crime_api_cache', backend='sqlite', expire_after=36000)

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

if __name__=="__main__":
  app.run(host='0.0.0.0', debug=True)
