# google_drive_helper/google_drive_uploader.py
from google_drive_helper.src.auth import AuthManager
from google_drive_helper.src.drive_manager import DriveManager
from google_drive_helper.src.file_uploader import FileUploader


class GoogleDriveUploader(AuthManager, DriveManager, FileUploader):
    def __init__(
        self, credentials_json="credentials.json", credentials_pickle="token.pickle"
    ):
        # 初始化 AuthManager 並取得認證
        AuthManager.__init__(self, credentials_json, credentials_pickle)
        # 初始化 DriveManager 並創建 Drive 服務
        DriveManager.__init__(self, self.creds)
        # 初始化 FileUploader 並準備好上傳服務
        FileUploader.__init__(self, self.drive_service)

    def upload_to_drive(
        self, drive_name, drive_folder_path, upload_file_path, mimetype=None
    ):
        """整合方法：列出共用雲端硬碟、找到目標資料夾並上傳檔案"""
        drive_id = self.list_shared_drives(drive_name)
        if drive_id:
            target_folder_id = self.find_folder_by_path(drive_id, drive_folder_path)
            if target_folder_id:
                print(f"Ready to upload to folder ID: {target_folder_id}")
                self.upload_file(target_folder_id, upload_file_path, mimetype)
            else:
                print("Target folder not found or inaccessible.")
        else:
            print("Shared drive not found.")
