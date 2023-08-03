from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/crud"
mongo = PyMongo(app)

# def get_collection_name():
#     return mongo.list_collection_names()[0]  # Assuming you have only one collection

# # Example route to demonstrate getting the collection name
# @app.route('/api/collection_name', methods=['GET'])
# def collection_name():
#     collection_name = get_collection_name()
#     return jsonify({"collection_name": collection_name}), 200

# Define the data model
class ClothesItem:
    def __init__(self, id, clothes_original_image, clothes_image, clothes_mask_image, sleeves, length, ckpt, category):
        self.id = id
        self.clothes_original_image = clothes_original_image
        self.clothes_image = clothes_image
        self.clothes_mask_image = clothes_mask_image
        self.sleeves = sleeves
        self.length = length
        self.ckpt = ckpt
        self.category = category

# CRUD operations
@app.route('/api/clothes', methods=['GET'])
def get_all_clothes():
    clothes_list = list(mongo.test.find({}, {"_id": 0}))
    return jsonify(clothes_list)

@app.route('/api/clothes/<string:clothes_id>', methods=['GET'])
def get_clothes(clothes_id):
    clothes = mongo.test.find_one({"_id": ObjectId(clothes_id)}, {"_id": 0})
    if clothes:
        return jsonify(clothes)
    else:
        return jsonify({"message": "Clothes not found"}), 404

@app.route('/api/clothes', methods=['POST'])
def create_clothes():
    data = request.get_json()
    new_clothes = ClothesItem(None, **data)
    result = mongo.test.insert_one(new_clothes.__dict__)
    return jsonify({"message": "Clothes created successfully", "inserted_id": str(result.inserted_id)}), 201

@app.route('/api/clothes/<string:clothes_id>', methods=['PUT'])
def update_clothes(clothes_id):
    data = request.get_json()
    updated_clothes = ClothesItem(clothes_id, **data)
    mongo.test.update_one({"_id": ObjectId(clothes_id)}, {"$set": updated_clothes.__dict__})
    return jsonify({"message": "Clothes updated successfully"}), 200

@app.route('/api/clothes/<string:clothes_id>', methods=['DELETE'])
def delete_clothes(clothes_id):
    result = mongo.test.delete_one({"_id": ObjectId(clothes_id)})
    if result.deleted_count > 0:
        return jsonify({"message": "Clothes deleted successfully"}), 200
    else:
        return jsonify({"message": "Clothes not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
