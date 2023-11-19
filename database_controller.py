 from PyQt5.QtCore import Qt
from bson import ObjectId
from pymongo import *

database_name = 'main_db'

client = MongoClient('mongodb://192.168.1.18:27017')
database = client[database_name]

def add_user(nickname, name, password):
    if get_user_info(nickname) is not None:
        return -1

    data_dict = {
        'nickname': nickname,
        'name': name,
        'password': password,
    }

    users_collection = database['users_data']

    try:
        user_id = users_collection.insert_one(data_dict).inserted_id
    except Exception as e:
        return -2

    return user_id


def add_note(user_id, note_title, note_desc, note_creation_date, note_colour) -> bool:
    data_dict = {
        'user_id': ObjectId(user_id),
        'title': note_title,
        'desc': note_desc,
        'creation_date': note_creation_date,
        'note_colour': note_colour,
    }

    notes_collection = database['notes_data']

    try:
        note_id = notes_collection.insert_one(data_dict).inserted_id
        return True if add_note_to_days(user_id, note_id, note_creation_date, note_colour) else False
    except Exception as e:
        return False


def add_note_to_days(user_id, note_id, creation_date, note_colour):
    days_collection = database['days_data']

    date_record = record_for_date(creation_date)
    if date_record is not None:
        return insert_note_for_date(user_id, note_id, note_colour, date_record)

    data_list = [
        {
            'note_1': {
                'user_id': ObjectId(user_id),
                'note_id': ObjectId(note_id),
                'note_colour': note_colour
            },
        }
    ]

    data_dict = {
        'date': creation_date,
        'notes_data': data_list
    }

    try:
        days_collection.insert_one(data_dict)
    except Exception as e:
        return -2

    return 1


def insert_note_for_date(user_id, note_id, note_colour, date_record):
    days_collection = database['days_data']

    notes_list = date_record['notes_data']
    num_for_new_record = len(notes_list) + 1

    new_note_dict = {
        f'note_{num_for_new_record}': {
            'user_id': ObjectId(user_id),
            'note_id': ObjectId(note_id),
            'note_colour': note_colour
        }
    }

    notes_list.append(new_note_dict)
    res_dict = {
        'notes_data': notes_list
    }

    try:
        days_collection.update_one({'date': date_record['date']}, {"$set": res_dict})
    except Exception as e:
        return False

    return True


def record_for_date(date_to_check):
    days_collection = database['days_data']
    return days_collection.find_one({'date': date_to_check})


def save_edited_note(user_id, note_id, note_title, note_desc, note_creation_date, note_colour):
    note_doc = get_note(note_id)

    if note_doc is None:
        return -1

    data_dict = {
        'user_id': ObjectId(user_id),
        'title': note_title,
        'desc': note_desc,
        'creation_date': note_creation_date,
        'note_colour': note_colour,
    }

    notes_collection = database['notes_data']
    try:
        notes_collection.update_one({'_id': ObjectId(note_id)}, {"$set": data_dict})
        edit_note_in_date(note_id, note_creation_date, note_colour)
    except Exception as e:
        return -2

    return 1


def edit_note_in_date(note_id, date, note_colour):
    days_collection = database['days_data']

    notes_list = list()
    for day in days_collection.find({}):
        if day['date'] != date:
            continue

        day_notes = day['notes_data']
        for note in day_notes:
            if list(note.items())[0][1]['note_id'] == note_id:
                list(note.items())[0][1]['note_colour'] = note_colour

            notes_list.append(note)

    res_dict = {
        'notes_data': notes_list
    }

    try:
        days_collection.update_one({'date': date}, {"$set": res_dict})
    except Exception as e:
        return -2

    return 1


def get_note(note_id):
    notes_collection = database['notes_data']
    return notes_collection.find_one({'_id': ObjectId(note_id)})


def delete_note(date, note_id):
    note_doc = get_note(note_id)

    if note_doc is None:
        return -1

    notes_collection = database['notes_data']
    try:
        notes_collection.delete_one({'_id': ObjectId(note_id)})
        delete_note_from_day(date, note_id)
    except Exception as e:
        return -2

    return 1


def delete_note_from_day(date, note_id):
    days_collection = database['days_data']

    notes_list = list()
    for day in days_collection.find({}):
        if day['date'] != date:
            continue

        day_notes = day['notes_data']
        for note in day_notes:
            if list(note.items())[0][1]['note_id'] == note_id:
                continue
            else:
                notes_list.append(note)

    res_dict = {
        'notes_data': notes_list
    }

    try:
        days_collection.update_one({'date': date}, {"$set": res_dict})
    except Exception as e:
        return -2

    return 1


def get_user_notes(user_id, note_creation_date):
    notes_collection = database['notes_data']

    col = notes_collection.find({'user_id': ObjectId(user_id)})

    if col is None:
        return None
    else:
        return get_date_notes(col, note_creation_date)


def get_date_notes(col, chosen_date):
    result_collection = list()
    for element in col:
        creation_date = element['creation_date']

        if creation_date == chosen_date:
            result_collection.append(element)

    return result_collection


def get_list_for_calendar(user_id):
    all_user_notes_for_date = get_all_notes_data(user_id)

    return all_user_notes_for_date


def get_notes_for_day(date, collection):
    res_list = list()
    for element in collection:
        if date.toString(Qt.ISODate) == element['date']:
            res_list.append(element)

    return res_list


def get_notes_for_id(user_id, collection):
    t_collection = list()
    for element_dict in collection:
        notes_data = element_dict['notes_data']

        notes_list = list()
        for note in notes_data:
            if list(note.items())[0][1]['user_id'] == ObjectId(user_id):
                notes_list.append(note)

        element_dict['notes_data'] = notes_list
        t_collection.append(element_dict)

    return t_collection


def get_all_notes_data(user_id):
    days_collection = database['days_data']

    res_list = list()

    for day in days_collection.find({}):
        day_notes = day['notes_data']

        for note in day_notes:
            if list(note.items())[0][1]['user_id'] == ObjectId(user_id):
                res_list.append(day)

    return res_list


def get_user_info(nickname):
    users_collection = database['users_data']
    return users_collection.find_one({'nickname': nickname})


def get_user_by_id(user_id):
    users_collection = database['users_data']
    return users_collection.find_one({'_id': ObjectId(user_id)})


def update_user(user_id, new_nickname, new_name, new_password):
    users_collection = database['users_data']

    user = get_user_by_id(user_id)
    if user is None:
        return -1

    data_dict = {
        'nickname': new_nickname,
        'name': new_name,
        'password': new_password,
    }

    try:
        users_collection.update_one({'_id': ObjectId(user_id)}, {"$set": data_dict})
    except Exception as e:
        return -2

    return 1


def try_log_user(nickname, password):
    user_info = get_user_info(nickname)

    if user_info is None:
        return -1

    if user_info['password'] != password:
        return -2

    return user_info['_id']


def search_note(search_text, user_id, note_date):
    note_date = note_date.toString(Qt.ISODate)
    res_list = list()

    print(f'Got search request:\n\tfor {search_text}\n\tfrom {user_id}\n\ton {note_date}')

    notes_collection = database['notes_data']

    try:
        notes_collection.create_index([('title', 'text'), ('desc', 'text')])
    except Exception as e:
        print('Index already exists')
        return res_list

    t_list = notes_collection.find({'user_id': ObjectId(user_id), 'creation_date': note_date,
                                    '$text': {
                                        '$search': search_text
                                    }
                                    })

    for note in t_list:
        res_list.append(note)

    return res_list
