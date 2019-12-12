def allowed_file(filename):
    """
    Verifies if the file extension is valid
    :param filename:
    :return:
    """
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
