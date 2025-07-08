from flask import Flask, request, jsonify
import geopandas as gpd
from shapely.geometry import Point
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

cuadrantes = gpd.read_file("geojson/cuadrantes.geojson").to_crs(epsg=4326)
barrios = gpd.read_file("geojson/barrios.geojson").to_crs(epsg=4326)
villas = gpd.read_file("geojson/villas.geojson").to_crs(epsg=4326)

@app.route("/zonas", methods=["GET"])
def zonas():
    try:
        lat = float(request.args.get("lat"))
        lon = float(request.args.get("lon"))
        punto = Point(lon, lat)

        cuadrante = cuadrantes[cuadrantes.geometry.contains(punto)]
        barrio = barrios[barrios.geometry.contains(punto)]
        villa = villas[villas.geometry.contains(punto)]

        data = {
            "cuadrante": cuadrante.iloc[0]["NUM_CUAD"] if not cuadrante.empty else "Sin cuadrante",
            "barrio": barrio.iloc[0]["BARRIO"] if not barrio.empty else "Sin barrio",
            "villa": villa.iloc[0]["NOMBRE_LOT"] if not villa.empty else "Sin villa"
        }

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run()
