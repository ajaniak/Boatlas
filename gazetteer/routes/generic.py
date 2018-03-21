from flask import render_template, request, flash, redirect
from flask_login import current_user, login_user, logout_user, login_required

from ..app import app, login
from ..constantes import LIEUX_PAR_PAGE
from ..modeles.donnees import Place, Biblio
from ..modeles.utilisateurs import User


@app.route("/")
def accueil():
    """ Route permettant l'affichage d'une page accueil
    """
    # On a bien sûr aussi modifié le template pour refléter le changement
    lieux = Place.query.order_by(Place.place_id.desc()).limit(5).all()
    return render_template("pages/accueil.html", nom="Gazetteer", lieux=lieux)


@app.route("/place/<int:place_id>")
def lieu(place_id):
    """ Route permettant l'affichage des données d'un lieu

    :param place_id: Identifiant numérique du lieu
    """
    # On a bien sûr aussi modifié le template pour refléter le changement
    unique_lieu = Place.query.get(place_id)
    return render_template("pages/place.html", nom="Gazetteer", lieu=unique_lieu)


@app.route("/recherche")
def recherche():
    """ Route permettant la recherche plein-texte
    """
    # On préfèrera l'utilisation de .get() ici
    #   qui nous permet d'éviter un if long (if "clef" in dictionnaire and dictonnaire["clef"])
    motclef = request.args.get("keyword", None)
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    # On crée une liste vide de résultat (qui restera vide par défaut
    #   si on n'a pas de mot clé)
    resultats = []

    # On fait de même pour le titre de la page
    titre = "Recherche"
    if motclef:
        resultats = Place.query.filter(
            Place.place_nom.like("%{}%".format(motclef))
        ).paginate(page=page, per_page=LIEUX_PAR_PAGE)
        titre = "Résultat pour la recherche `" + motclef + "`"

    return render_template(
        "pages/recherche.html",
        resultats=resultats,
        titre=titre,
        keyword=motclef
    )

@app.route("/browse")
def browse():
    """ Route permettant la recherche plein-texte
    """
    # On préfèrera l'utilisation de .get() ici
    #   qui nous permet d'éviter un if long (if "clef" in dictionnaire and dictonnaire["clef"])
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    resultats = Place.query.paginate(page=page, per_page=LIEUX_PAR_PAGE)

    return render_template(
        "pages/browse.html",
        resultats=resultats
    )

@app.route("/register", methods=["GET", "POST"])
def inscription():
    """ Route gérant les inscriptions
    """
    # Si on est en POST, cela veut dire que le formulaire a été envoyé
    if request.method == "POST":
        statut, donnees = User.creer(
            login=request.form.get("login", None),
            email=request.form.get("email", None),
            nom=request.form.get("nom", None),
            motdepasse=request.form.get("motdepasse", None)
        )
        if statut is True:
            flash("Enregistrement effectué. Identifiez-vous maintenant", "success")
            return redirect("/")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            return render_template("pages/inscription.html")
    else:
        return render_template("pages/inscription.html")


@app.route("/connexion", methods=["POST", "GET"])
def connexion():
    """ Route gérant les connexions
    """
    if current_user.is_authenticated is True:
        flash("Vous êtes déjà connecté-e", "info")
        return redirect("/")
    # Si on est en POST, cela veut dire que le formulaire a été envoyé
    if request.method == "POST":
        utilisateur = User.identification(
            login=request.form.get("login", None),
            motdepasse=request.form.get("motdepasse", None)
        )
        if utilisateur:
            flash("Connexion effectuée", "success")
            login_user(utilisateur)
            return redirect("/")
        else:
            flash("Les identifiants n'ont pas été reconnus", "error")

    return render_template("pages/connexion.html")
login.login_view = 'connexion'


@app.route("/deconnexion", methods=["POST", "GET"])
def deconnexion():
    if current_user.is_authenticated is True:
        logout_user()
    flash("Vous êtes déconnecté-e", "info")
    return redirect("/")

@app.route("/depot", methods=["POST", "GET"])
def depot():
    if request.method == "POST":
        statut, donnees = Place.creer_lieu(
            lieu=request.form.get("lieu", None),
            lat=request.form.get("lat", None),
            longt=request.form.get("longt", None),
            desc=request.form.get("desc", None),
            typep=request.form.get("typep", None)
        )
        if statut is True:
            flash("Enregistrement effectué. Vous avez ajouté un nouveau lieu", "success")
            return redirect("/")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            return render_template("pages/depot.html")
    else:
        return render_template("pages/depot.html")

@app.route("/modif_lieu/<int:place_id>")
@login_required
def modif_lieu(place_id):
    status, donnees = Place.modif_lieu(
        id=place_id,
        nom=request.args.get("nom", None),
        latitude=request.args.get("latitude", None),
        longitude=request.args.get("longitude", None),
        description=request.args.get("description", None),
        type=request.args.get("type", None),
    )

    if status is True :
        flash("Merci pour votre contribution !", "success")
        unique_lieu = Place.query.get(place_id)
        return redirect("/") #vers le lieu qu'il vient de créer.

    else:
        flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
        unique_lieu = Place.query.get(place_id)
        return render_template("pages/modif_lieu.html", lieu=unique_lieu)

@app.route("/creer_biblio")
@login_required
def creer_biblio():
    status, donnees = Biblio.creer_biblio(
    titre=request.args.get("titre", None),
    auteur=request.args.get("auteur", None),
    date=request.args.get("date", None),
    lieu=request.args.get("lieu", None),
    type=request.args.get("type", None),
    )

    if status is True :
        flash("Merci pour votre contribution !", "success")


        return redirect("/") #vers la référence bibliographique qu'il vient de créer.

    else:
        flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")

        return render_template("pages/creer_biblio.html")

@app.route("/modif_biblio/<int:biblio_id>")
@login_required
def modif_biblio(biblio_id):
    status, donnees = Biblio.modif_biblio(
        id=biblio_id,
        titre=request.args.get("titre", None),
        auteur=request.args.get("auteur", None),
        date=request.args.get("date", None),
        lieu=request.args.get("lieu", None),
        type=request.args.get("type", None),
    )

    if status is True :
        flash("Merci pour votre contribution !", "success")
        unique_biblio = Biblio.query.get(biblio_id)
        return redirect("/") #vers le lieu qu'il vient de créer.

    else:
        flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
        unique_biblio = Biblio.query.get(biblio_id)
        return render_template("pages/modif_biblio.html", lieu=unique_biblio)


@app.route("/biblio/<int:biblio_id>")
def biblio(biblio_id):
    """ Route permettant l'affichage des données d'un lieu

    :param biblio_id: Identifiant numérique de la référence bibliographique
    """
    # On récupère le tuple correspondant aux champs de la classe Biblio
    unique_biblio = Biblio.query.get(biblio_id)
    print(unique_biblio)
    return render_template("pages/biblio.html", nom="Gazetteer", biblio=unique_biblio)
