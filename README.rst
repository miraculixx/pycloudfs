\#\#Pycloudfs A collection of helper classes/scripts to ease access to
s3, gridfs and other storages (will be added later).

\#\#Usage
`` ` # gridfs  from pycloudfs import GridFSHelper gf = GridFSHelper() gf.mongo_url = 'mongodb://localhost:27017/mydb' gf.collection = 'mycollection' gf.get_list() print gf.get_file('Untitled.txt', asfile=True)._id gf.get_file('dummy.txt') gf.put_file('newfile.txt')  #s3 # keys can also be read from local environment from pycloudfs import S3Helper s3 = S3Helper(bucket='test', aws_access_key_id="key", aws_secret_access_key="secret") s3.get_list() s3.download_file('uploadtest.crypt') ``\`
