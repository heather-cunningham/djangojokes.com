from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    """ Class for storing static files. """
    location = 'static'
    default_acl = 'public-read' ## ACL = "Access Control List"
    file_overwrite = True
## END class


class PublicMediaStorage(S3Boto3Storage):
    """ Class for storing public media files. """
    location = 'media/public'
    default_acl = 'public-read' 
    file_overwrite = False
## END class


class PrivateMediaStorage(S3Boto3Storage):
    """ Class for storing private media files. """
    location = 'media/private'
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False
## END class