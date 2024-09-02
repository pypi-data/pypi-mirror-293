from cbr_shared.aws.s3.S3_DB__CBR import S3_DB__CBR

class S3_DB__Server_Requests(S3_DB__CBR):

    def setup(self):
        pass

    def folder_name(self):
        return 'server-requests'

