import json

from flask_security import login_required, roles_required

from api import api
from main import service


@api.route('<string:photo_id>/like', methods=['POST'])
def like(photo_id):
    n_likes = service.like_photo(photo_id)
    return json.dumps({'success': n_likes > 0, 'total_likes': n_likes}), 200 if n_likes > 0 else 404, {
        'ContentType': 'application/json'}


@api.route('<string:photo_id>/approve', methods=['POST'])
@login_required
@roles_required('owner')
def approve(photo_id):
    activated = service.activate_photo(photo_id)
    return json.dumps({'success': activated}), 200 if activated else 404, {'ContentType': 'application/json'}
