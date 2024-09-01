"""
配置文件
"""

from typing import Dict, List, Optional, Union, Set, Any

from nonebot import get_plugin_config
from nonebot.drivers.websockets import logger
from pydantic import Field, BaseModel, field_validator


class Guild(BaseModel):
    """频道配置"""

    # 频道ID，QQ适配器不需要频道ID
    guild_id: Optional[str] = None
    # 子频道ID
    channel_id: str
    # 适配器类型
    adapter: Optional[str] = None
    # Bot ID 优先使用所选Bot发送消息
    bot_id: Optional[str] = None


class Group(BaseModel):
    """群配置"""

    # 群ID
    group_id: str
    # 适配器类型
    adapter: Optional[str] = None
    # Bot ID
    bot_id: Optional[str] = None


class Server(BaseModel):
    """服务器配置"""

    # 服务器群列表
    group_list: List[Group] = []
    # 服务器频道列表
    guild_list: List[Guild] = []
    # 是否开启 Rcon 消息
    rcon_msg: bool = False
    # 是否开启 Rcon 命令
    rcon_cmd: bool = False


class MCQQConfig(BaseModel):
    """配置"""

    command_header: Union[str, List[str], Set[str]] = {"mcc"}
    """命令头"""

    command_priority: int = 98
    """命令优先级，1-98，消息优先级=命令优先级 - 1"""

    command_block: bool = True
    """命令消息是否阻断后续消息"""

    rcon_result_to_image: bool = False
    """是否将 Rcon 命令执行结果转换为图片"""

    send_group_name: bool = False
    """是否发送群聊名称"""

    display_server_name: bool = False
    """是否发送服务器名称"""

    say_way: str = "说："
    """用户发言修饰"""

    server_dict: Dict[str, Server] = Field(default_factory=dict)
    """服务器配置"""

    guild_admin_roles: List[str] = ["频道主", "超级管理员"]
    """频道管理员角色"""

    chat_image_enable: bool = False
    """是否启用 ChatImage MOD"""

    cmd_whitelist: List[str] = ["list", "tps", "banlist"]
    """命令白名单"""

    @field_validator("command_header")
    @classmethod
    def validate_command_header(cls, v: Any) -> Set[str]:
        if isinstance(v, str):
            return {v}
        elif isinstance(v, list):
            return set(v)
        elif isinstance(v, set):
            return v
        else:
            raise ValueError("command_header must be str or list or set")

    @field_validator("command_priority")
    @classmethod
    def validate_priority(cls, v: int) -> int:
        if 98 >= v >= 1:
            return v
        raise ValueError("mcqq command priority must bigger than 1 and smaller than 98")

    @field_validator("rcon_result_to_image")
    @classmethod
    def validate_rcon_result_to_image(cls, v: bool) -> bool:
        try:
            import pillow
            return True
        except ImportError:
            logger.warn("Pillow not installed, please install it to use rcon result to image")
            return False


class Config(BaseModel):
    """配置项"""

    mc_qq: MCQQConfig = MCQQConfig()


plugin_config: MCQQConfig = get_plugin_config(Config).mc_qq
