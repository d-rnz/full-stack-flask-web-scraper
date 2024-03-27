from flask import request, jsonify
from config import app, db
from models import Manga


# Set up route for /mangas GET request
@app.route("/mangas", methods=["GET"])
def get_mangas():
    # Get all the Manga model objects from the database
    mangas = Manga.query.all()
    # Convert the Manga model objects to JSON
    json_mangas = list(map(lambda manga: manga.to_json(), mangas))
    return jsonify({"mangas": json_mangas})


@app.route("/create-manga", methods=["POST"])
def create_manga():
    # Get the JSON data from the request
    data = request.get_json()
    # Create a new Manga model object
    new_manga = Manga(
        image_url=data.get("imageURL", None),
        title=data["title"],
        rating=data["rating"],
        latest_chapter=data.get("latestChapter", None),
        current_chapter=data["currentChapter"],
        chapter_diff=data.get("chapterDiff", None),
        link=data.get("link", None),
        website=data["website"],
    )
    try:
        # Add the new Manga model object to the database
        db.session.add(new_manga)
        db.session.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({"message": "Manga created successfully"}), 201


@app.route("/update-manga/<int:id>", methods=["PATCH"])
def update_manga(id):
    # Get the JSON data from the request
    data = request.get_json()
    # Get the Manga model object from the database
    manga = Manga.query.get(id)
    if manga is None:
        return jsonify({"error": "Manga not found"}), 404

    # Update the Manga model object with the new data
    manga.rating = data.get("rating", manga.rating)
    manga.current_chapter = data.get("currentChapter", manga.current_chapter)
    manga.website = data.get("website", manga.website)
    # Commit the changes to the database
    db.session.commit()

    return jsonify({"message": "Manga updated successfully"}), 200


@app.route("/delete-manga/<int:id>", methods=["DELETE"])
def delete_manga(id):
    # Get the Manga model object from the database
    manga = Manga.query.get(id)
    if manga is None:
        return jsonify({"error": "Manga not found"}), 404

    # Delete the Manga model object from the database
    db.session.delete(manga)
    db.session.commit()

    return jsonify({"message": "Manga deleted successfully"}), 200


if __name__ == "__main__":
    # Create the database
    with app.app_context():
        db.create_all()

    # Run the Flask app
    app.run(debug=True)
