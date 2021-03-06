import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

user_prefs = Blueprint('user_prefs', 'user_prefs')

# TEST
@user_prefs.route('/')
def user_prefs_index():
  return "user_prefs resource working"

# INDEX
@user_prefs.route('/show', methods=['GET'])
@login_required
def user_prefs_show():
  # have to query the user_prefs table and only return the currently logged in user's prefs
  current_user_user_pref_dicts = [model_to_dict(user_pref) for user_pref in current_user.user_prefs]
  print(current_user_user_pref_dicts)
  for user_pref_dict in current_user_user_pref_dicts:
    user_pref_dict['owner'].pop('password')
  print(current_user_user_pref_dicts)

  return jsonify({
    'data': current_user_user_pref_dicts,
    'message': f"Successfully FOUND {len(current_user_user_pref_dicts)} (YOUR) USER PREFERENCES",
    'status': 200
  }), 200

# @user_prefs.route('/all', methods=['GET'])
# def get_all_user_prefs():
#   user_prefs = models.User_pref.select()
#   user_pref_dicts = [model_to_dict(user_pref) for user_pref in user_prefs] 
#   for user_pref in user_pref_dicts:
#     user_pref['owner'].pop('password')
#     if not current_user.is_authenticated: 
#       user_pref.pop('owner')
#   return jsonify({
#     'data': user_pref_dicts,
#     'message': f"Successfully FOUND {len(user_pref_dicts)} (ALL) user_prefs",
#     'status': 200
#   })

# CREATE
@user_prefs.route('/', methods=['POST'])
@login_required
def create_user_profile():
  payload = request.get_json()
  print("USER PROFILE PREFS -- PAYLOAD -->", payload)

  new_user_profile = models.User_pref.create(
    name=payload['name'], 
    owner=current_user.id, 
    clean_pref=payload['clean_pref'],
    big_pref=payload['big_pref'],
    fenced_pref=payload['fenced_pref'],
    busy_pref=payload['busy_pref'],
    note=payload['note'],
  )
  print(dir(new_user_profile))
  user_prefs_dict = model_to_dict(new_user_profile)
  print(user_prefs_dict)
  user_prefs_dict['owner'].pop('password')

  return jsonify(
    data=[user_prefs_dict], 
    message='Successfully CREATED USER PREFERENCES',
    status=201
  ), 201

# UPDATE
@user_prefs.route('/', methods=['PUT'])
@login_required
def update_user_pref():
  payload = request.get_json()
  user_pref_to_update = models.User_pref.get_by_id(id)
  if user_pref_to_update.owner.id == current_user.id:
    if 'name' in payload:
      user_pref_to_update.name = payload['name']
    if 'clean_pref' in payload:
      user_pref_to_update.clean_pref = payload['clean_pref']
    if 'big_pref' in payload:
      user_pref_to_update.big_pref = payload['big_pref']
    if 'fenced_pref' in payload:
      user_pref_to_update.fenced_pref = payload['fenced_pref']
    if 'busy_pref' in payload:
      user_pref_to_update.busy_pref = payload['busy_pref']
    if 'note' in payload:
      user_pref_to_update.note = payload['note']
    user_pref_to_update.save()
    updated_user_pref_dict = model_to_dict(user_pref_to_update)
    updated_user_pref_dict['owner'].pop('password')

    return jsonify(
        data=updated_user_pref_dict,
        message=f"Successfully UPDATED USER PREFERENCES",
        status=200
      ), 200
  else:
    return jsonify(
      data={ 'error': '403 Forbidden'},
      message="USER's ID DOES NOT MATCH current users id. User can only UPDATE their own PREFERENCES",
      status=403
    ), 403

# DELETE
# make it so that only 1 can be created.  once a user makes their
# preferences, they can only edit it moving forward

@user_prefs.route('/<id>', methods=['DELETE'])
@login_required
def delete_user_pref(id):
  try:
    user_pref_to_delete = models.User_pref.get_by_id(id)
    if user_pref_to_delete.owner.id == current_user.id:
      user_pref_to_delete.delete_instance()
      return jsonify(
        data={},
        message=f"Successfully DELETED USER PREFS (should only have 1) with id {id}",
        status=200
      ), 200
    else:
      return jsonify(
        data={
          'error': '403 Forbidden'
        },
        message="User Pref's owner's id DOES NOT MATCH user's id.",
        status=403
      ), 403

  except models.DoesNotExist:
    return jsonify(
      data={
        'error': '404 Not found'
      },
      message="There is NO User prefs with that ID.",
      status=404
    ), 404











# @user_prefs.route('/show', methods=['GET'])
# @login_required
# def user_prefs_show():
#   # try:
#   #   user_pref_to_show = current_user.user_pref
#   #   if user_pref_to_show.owner.id == current_user.id:

#   # have to query the user_prefs table and only 
#   # return the currently logged in user's prefs

#     # if new_user_profile.owner.id == current_user.id:
#   if current_user.user_prefs:
#     current_user_user_pref_dicts = [model_to_dict(user_pref) for user_pref in current_user.user_prefs]
#     print(current_user_user_pref_dicts)
#     for user_pref_dict in current_user_user_pref_dicts:
#       user_pref_dict['owner'].pop('password')
#     print(current_user_user_pref_dicts)

#   return jsonify({
#     'data': current_user_user_pref_dicts,
#     'message': f"Successfully FOUND {len(current_user_user_pref_dicts)} (YOUR) USER PREFERENCES",
#     'status': 200
#   }), 200


















