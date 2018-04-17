from flask import render_template, request, url_for, jsonify, json
from urllib.parse import urlencode

from ..app import app
from ..constantes import LIEUX_PAR_PAGE, API_ROUTE
from ..modeles.donnees import Place, Biblio, Relation, Authorship
from ..modeles.utilisateurs import User

#Classe pour encoder les sets en listes (pour la TypeError "JSON is not serializable")
class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

def Json_404():
    response = jsonify({"erreur": "Unable to perform the query"})
    response.status_code = 404
    return response


@app.route(API_ROUTE+"/places/<int:place_id>")
def api_places_single(place_id):
    lieu = Place.query.get(place_id)
    if not lieu:
        return Json_404
    else:
        return jsonify(lieu.to_jsonapi_dict())


@app.route(API_ROUTE+"/biblios/<biblio_id>")
def api_biblios_single(biblio_id):
    biblio = Biblio.query.get(biblio_id)
    if not biblio:
        return Json_404
    else:
        return jsonify(biblio.to_jsonapi_dict())


@app.route(API_ROUTE+"/relations/<relation_id>")
def api_relations_single(relation_id):
    try:
        query = Relation.query.get(relation_id)
        return jsonify(query.to_jsonapi_dict())
    except:
        return Json_404()



@app.route(API_ROUTE+"/places")
def api_places_browse():
    """ Route permettant la recherche plein-texte

    On s'inspirera de http://jsonapi.org/ faute de pouvoir trouver temps d'y coller à 100%
    """
    # q est très souvent utilisé pour indiquer une capacité de recherche
    motclef = request.args.get("q", None)
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    if motclef:
        query = Place.query.filter(
            Place.place_nom.like("%{}%".format(motclef))
        )
    else:
        query = Place.query

    try:
        resultats = query.paginate(page=page, per_page=LIEUX_PAR_PAGE)
    except Exception:
        return Json_404()

    dict_resultats = {
        "links": {
            "self": request.url
        },
        "data": [
            place.to_jsonapi_dict()
            for place in resultats.items
        ]
    }

    if resultats.has_next:
        arguments = {
            "page": resultats.next_num
        }
        if motclef:
            arguments["q"] = motclef
        dict_resultats["links"]["next"] = url_for("api_places_browse", _external=True)+"?"+urlencode(arguments)

    if resultats.has_prev:
        arguments = {
            "page": resultats.prev_num
        }
        if motclef:
            arguments["q"] = motclef
        dict_resultats["links"]["prev"] = url_for("api_places_browse", _external=True)+"?"+urlencode(arguments)

    response = jsonify(dict_resultats)
    return response
