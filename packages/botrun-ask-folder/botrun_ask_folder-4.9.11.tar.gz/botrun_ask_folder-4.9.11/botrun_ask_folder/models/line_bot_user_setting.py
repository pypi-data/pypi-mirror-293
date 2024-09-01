from pydantic import BaseModel
from datetime import datetime
import pytz


class LineBotUserSetting(BaseModel):
    user_id: str
    model_name: str = ""  # 默認模型
    created_at: str = datetime.now(pytz.timezone("Asia/Taipei")).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    updated_at: str = datetime.now(pytz.timezone("Asia/Taipei")).strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    def refresh_timestamp(self):
        self.updated_at = datetime.now(pytz.timezone("Asia/Taipei")).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
