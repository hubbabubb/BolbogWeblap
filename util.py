import re
import bcrypt


def hash_password(plain_text_password):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


# def highlight_text(search_results, search):
#     new_results = []
#
#     for highlight in search_results:
#         new_title = re.sub(re.escape(search), f'<mark>{search.upper()}</mark>', highlight['title'], flags=re.IGNORECASE)
#         new_message = re.sub(re.escape(search), f'<mark>{search.upper()}</mark>', highlight['message'], flags=re.IGNORECASE)
#         new_dict_row = {'id': highlight['id'],
#                         'submission_time': highlight['submission_time'],
#                         'view_number': highlight['view_number'],
#                         'title': new_title,
#                         'message': new_message,
#                         'vote_number': highlight['vote_number'],
#                         'image': highlight['image'],
#                         }
#         new_results.append(new_dict_row)
#
#     return new_results