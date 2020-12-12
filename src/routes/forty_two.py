from flask import Blueprint

bp = Blueprint('forty_two', __name__, url_prefix='/42')

@bp.route('', methods=['GET'])
def forty_two():
    return {"Success": "42 endpoint successfully reached."}, 200
