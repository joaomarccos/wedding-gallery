from uuid import uuid4


class GalleryService:
    def __init__(self, db, s3):
        self.db = db
        self.bucket = s3.Bucket('wedding-gallery-bkt')
        self.s3 = s3

    def get_paginated_items(self, page, limit=10, filters=None):
        """
        obtain all items in gallery collection with pagination feature
        :param filters: filter
        :param page: number of the page
        :param limit: max items per page
        :return:
        """
        pass

    def _count_items(self, filters=None):
        """
        Get the total number of items of gallery collection
        :type filters: filter
        :return:
        """
        pass

    def put_item(self, photo, file):
        """
        Put an item on gallery collection
        :param file: uploaded image
        :param photo: dict with item metadata
        :return:
        """
        obj_key = uuid4().hex
        obj_name = obj_key + '.' + file.filename.split('.')[-1]
        self.bucket.upload_fileobj(file, obj_name)
        object_acl = self.s3.ObjectAcl('wedding-gallery-bkt', obj_name)
        object_acl.put(ACL='public-read')
        photo.url = f'https://wedding-gallery-bkt.s3.amazonaws.com/{obj_name}'
        photo.save()
