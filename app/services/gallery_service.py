from uuid import uuid4

from mongoengine import DoesNotExist, MultipleObjectsReturned

from models.photo_model import Photo


class GalleryService:
    def __init__(self, s3):
        self.bucket = s3.Bucket('wedding-gallery-bkt')
        self.s3 = s3

    def get_paginated_items(self, page, limit=5, order_by='likes', **filters):
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
        calc_pages = round(total_items / limit)
        total_pages = calc_pages if calc_pages > 0 else 1
        has_next_page = (total_items // page if page > 0 else 1) > limit
        has_prev_page = page > 1 and total_items > 0
        photos = list(map(lambda i: i.to_dict(), [ob.to_mongo() for ob in items]))
        photos.reverse()
        return {
            'page': page,
            'totalItems': total_items,
            'totalPages': total_pages,
            'items': photos,
            'hasNext': has_next_page,
            'hasPrev': has_prev_page
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

    @staticmethod
    def activate_photo(photo_id):
        """
        Set the photo active status to True
        :param photo_id: Photo ID (Object ID)
        :return: None
        """
        try:
            Photo.objects(id=photo_id).update_one(set__active=True)
            return True
        except DoesNotExist:
            return False

    @staticmethod
    def like_photo(photo_id):
        """
        Increment the number of likes of a photo
        :param photo_id: Photo ID (Object ID)
        :return: number of likes
        """
        try:
            Photo.objects(id=photo_id).update_one(inc__likes=1)
            return Photo.objects(id=photo_id).get().to_mongo().to_dict()['likes']
        except (DoesNotExist, MultipleObjectsReturned):
            return 0
