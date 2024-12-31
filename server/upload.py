import os
import requests

# 此脚本用于初始化服务器索引，请勿滥用😇

# 配置
UPLOAD_URL = "http://127.0.0.1:1180/upload"  # 服务器地址
UPLOAD_FOLDER = ""  # 要上传的文件夹路径
UPLOAD_BY = ""  # 上传者名称
DELETE_PASSWORD = ""  # 删除密码

def batch_upload(folder):
    files_uploaded = 0
    errors = []

    for root, dirs, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "rb") as f:
                    files = {"file": (file, f, "audio/midi")}
                    data = {
                        "upload_by": UPLOAD_BY,
                        "delete_password": DELETE_PASSWORD,
                    }
                    response = requests.post(UPLOAD_URL, files=files, data=data)
                    if response.status_code == 200:
                        print(f"Successfully uploaded: {file}")
                        files_uploaded += 1
                    else:
                        error_message = response.json().get("message", "Unknown error")
                        print(f"Failed to upload {file}: {error_message}")
                        errors.append((file, error_message))
            except Exception as e:
                print(f"Error uploading {file}: {e}")
                errors.append((file, str(e)))

    print(f"\nBatch upload completed. Total files uploaded: {files_uploaded}")
    if errors:
        print("Errors occurred during upload:")
        for file, error in errors:
            print(f"  - {file}: {error}")

if __name__ == "__main__":
    batch_upload(UPLOAD_FOLDER)
