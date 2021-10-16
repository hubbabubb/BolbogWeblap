import re
import bcrypt
from werkzeug.utils import secure_filename
from PIL import Image


def hash_password(plain_text_password):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


def allowed_file(filename):
    extensions = ["PNG", "JPG", "JPEG", "GIF"]

    if "." not in filename:
        return False
    extension = filename.rsplit(".", 1)[1]
    if extension.upper() in extensions:
        return True
    else:
        return False


def get_image_name(image):
    filename = secure_filename(image.filename)
    image_name = "images/" + filename
    return image_name


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


def image_direction(image_name):
    image = Image.open('static/' + image_name)
    direction = 'equal'
    if image.width/image.height > 1:
        direction = 'horizontal'
    elif image.width/image.height < 1:
        direction = 'vertical'

    return direction
