# from minio import Minio
# from minio.error import S3Error


# def main():
#     # create client with the MinIo server playground ,its access key
#     # and secret key
#     client = Minio(
#         "localhost:9000",
#         access_key="BlII7v7e8YGnJfJEopwC",
#         secure=False,
#         secret_key="HiWjT6Fhy9DeDhRETfOSHRPnNm8Rh9VwcfDcZkcv",
#     )

#     # the file to upload,change this path if needed

#     source_file = "/home/ganesh/Downloads/ganesh.jpeg"

#     # the destination bucket and filename on the MinIo server
#     bucket_name = "test-bucket"
#     destination_file = "kunwar.jpeg"

#     # make the bucket if doesnot exits
#     found = client.bucket_exists(bucket_name)
#     if not found:
#         client.make_bucket(bucket_name)
#         print("Created bucket", bucket_name)

#     else:
#         print("Bucket", bucket_name, "already exits")

#     # upload the file ,remaining it in the process
#     client.fput_object(bucket_name, destination_file, source_file)
#     print(
#         source_file,
#         "successfully uploaded  as objects",
#         destination_file,
#         "to bucket",
#         bucket_name,
#     )


# if __name__ == "__main__":
#     try:
#         main()

#     except S3Error as exc:
#         print("error occurred", exc)

# # ===========start the minio server =============================IMPORTANT TOPIC
# # sudo systemctl start minio.servicess


# # RESOURCES FOR THE FILE UPLOADER
# # https://min.io/docs/minio/linux/developers/python/minio-py.html
