from flask import Blueprint, request, jsonify

main_bp = Blueprint('main', __name__)

@main_bp.route('/api/convert', methods=['POST'])
def convert_markdown():
    # This will be implemented later
    return jsonify({"message": "Conversion endpoint"}) 