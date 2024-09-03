from cbr_shared.aws.s3.S3_DB__CBR import S3_DB__CBR

S3_FOLDER__SERVER_REQUESTS = 'server-requests'

class S3_DB__Server_Requests(S3_DB__CBR):

    def s3_folder_server_requests(self):
        return S3_FOLDER__SERVER_REQUESTS
