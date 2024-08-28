# google_drive_helper/google_drive_explorer.py
from google_drive_helper.src.auth import AuthManager
from google_drive_helper.src.drive_manager import DriveManager


class GoogleDriveExplorer(AuthManager, DriveManager):
    def __init__(
        self, credentials_json="credentials.json", credentials_pickle="token.pickle"
    ):
        # 初始化 AuthManager 並取得認證
        AuthManager.__init__(self, credentials_json, credentials_pickle)
        # 初始化 DriveManager 並創建 Drive 服務
        DriveManager.__init__(self, self.creds)

    def list_drives(self, query=None):
        """列出共用雲端硬碟"""
        return self.list_shared_drives(query)

    def find_folder(self, drive_name, folder_path=None):
        """根據資料夾名稱和路徑找到資料夾的 ID"""

        # 取得共用雲端硬碟的 ID
        drive_id = self.list_shared_drives(drive_name)
        if not drive_id:
            print(f"Drive '{drive_name}' not found.")
            return None

        # 如果 folder_path 為 None 或空字符串，列出雲端硬碟中的所有資料夾
        if not folder_path:
            return self.list_folders_in_drive(drive_id)

        # 根據路徑查找特定資料夾
        folder_id = self.find_folder_by_path(drive_id, folder_path)
        if folder_id:
            return folder_id

        print(f"Folder '{folder_path}' not found in drive '{drive_name}'.")
        return None
