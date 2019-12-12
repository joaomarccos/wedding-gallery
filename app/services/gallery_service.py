from uuid import uuid4

from models.photo_model import Photo


class GalleryService:
    def __init__(self, db, s3):
        self.db = db
        self.bucket = s3.Bucket('wedding-gallery-bkt')
        self.s3 = s3

    def get_paginated_items(self, page, limit=10, order_by='timestamp', **filters):
        """
        obtain all items in gallery collection with pagination feature
        :param order_by: field used to sort
        :param filters: filter
        :param page: number of the page
        :param limit: max items per page
        :return:
        """

        offset = (page - 1) * limit
        items = Photo.objects(**filters).order_by(order_by).skip(offset).limit(limit)
        total_items = self._count_items(**filters)
        has_next_page = (total_items // page if page > 0 else 1) > limit
        has_prev_page = page > 1 and total_items > 0
        return {
            'page': page,
            'totalItems': total_items,
            'items': list(map(lambda i: i.to_dict(), [ob.to_mongo() for ob in items])),
            'hasNext': has_next_page,
            'hasPrev:': has_prev_page
        }

    @staticmethod
    def _count_items(**filters):
        """
        Get the total number of items of gallery collection
        :type filters
        :return:
        """
        return Photo.objects(**filters).count()

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
