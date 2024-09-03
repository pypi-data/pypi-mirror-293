import os
import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider

def check_and_upload(source_path, target_path, file_list):
    if file_list is []:
        return 
    
    auth = oss2.ProviderAuthV4(EnvironmentVariableCredentialsProvider())
    bucket = oss2.Bucket(auth, 'https://oss-cn-huhehaote.aliyuncs.com', 'gzhlaker-experiment', region="cn-huhehaote")
    
    for file_name, file_description in file_list:
        
        oss_path = os.path.join(target_path, file_name)
        local_path = os.path.join(source_path, file_name)
        readme_path = os.path.join(target_path, "readme.txt")
        
        resule_position = 0
        
        oss_exists = bucket.object_exists(oss_path)
        local_exists = os.path.exists(local_path)
        
        if local_exists and not oss_exists:
            bucket.put_object_from_file(oss_path, local_path)
            resule = bucket.append_object(readme_path, resule_position, f"{file_name}:{file_description}\n")
            resule_position = resule.next_position
        elif oss_exists and not local_exists:
            bucket.get_object_to_file(oss_path, local_path)
        elif not oss_exists and not local_exists:
            print("无可用文件")

def get_file_name(path):
  """
  获取一个文件夹下的所有名称
  """
  files = []
  for file in os.listdir(path):
      files.append(file)
  return files

def check_path(path):
    if not os.path.exists(path):
        os.system(f"mkdir -p {path}")