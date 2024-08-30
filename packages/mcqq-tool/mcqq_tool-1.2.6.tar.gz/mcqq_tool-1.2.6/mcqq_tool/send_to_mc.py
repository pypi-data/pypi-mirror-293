import json
from typing import List, Union, Callable, Optional, Awaitable

from nonebot import logger, get_bot
from nonebot.adapters.minecraft import Bot
from nonebot.adapters.minecraft.utils import DataclassEncoder
from nonebot.adapters.qq import Bot as QQBot
from nonebot.internal.matcher import Matcher
from nonebot.adapters.onebot.v11 import Bot as OneBot
from nonebot.adapters.qq import GuildMessageEvent as QQGuildMessageEvent
from nonebot_plugin_guild_patch import GuildMessageEvent as OneBotGuildMessageEvent
from nonebot.adapters.onebot.v11 import GroupMessageEvent as OneBotGroupMessageEvent
from nonebot.adapters.qq import GroupAtMessageCreateEvent as QQGroupAtMessageCreateEvent

from .config import plugin_config
from .model import (
    QQ_GROUP_ID_LIST,
    QQ_GUILD_ID_LIST,
    ONEBOT_GROUP_ID_LIST,
    ONEBOT_GUILD_ID_LIST,
)
from .parse_qq_msg import (
    parse_qq_msg_to_base_model,
    parse_qq_msg_to_rcon_model,
    parse_qq_screen_cmd_to_rcon_model,
)


def __get_mc_bot(server_name: str) -> Union[Bot, None]:
    """
    获取服务器 Bot
    :param server_name: 服务器名称
    :return: 服务器 Bot
    """
    try:
        return get_bot(server_name)
    except KeyError:
        logger.warning(f"[MC_QQ]丨未找到服务器 {server_name} 的 Bot")
    except ValueError:
        logger.warning(f"[MC_QQ]丨{server_name} 无可用 Bot")
    return None


def __get_server_list_by_event(func: Callable[..., Awaitable]) -> Callable:
    """
    通过事件获取服务器列表
    :param func: 发送 rcon cmd 至目标服务器的函数
    :return: 装饰后的发送函数
    """

    async def event_check(
            matcher: Matcher,
            bot: Union[QQBot, OneBot],
            event: Union[
                QQGuildMessageEvent, QQGroupAtMessageCreateEvent, OneBotGroupMessageEvent, OneBotGuildMessageEvent
            ],
            command_type: Optional[str] = "",
            is_cmd: bool = False,
            command: Optional[str] = "",
    ) -> str:
        temp_result = "返回结果：\n"
        if isinstance(event, QQGroupAtMessageCreateEvent):
            server_list = QQ_GROUP_ID_LIST.get(event.group_id)
            temp_result = "\n返回结果：\n"
        elif isinstance(event, QQGuildMessageEvent):
            server_list = QQ_GUILD_ID_LIST.get(event.channel_id)
        elif isinstance(event, OneBotGroupMessageEvent):
            server_list = ONEBOT_GROUP_ID_LIST.get(str(event.group_id))
        else:
            server_list = ONEBOT_GUILD_ID_LIST.get(f"{event.guild_id}:{event.channel_id}")
        return await func(
            matcher=matcher,
            server_list=server_list,
            bot=bot,
            event=event,
            is_cmd=is_cmd,
            command_type=command_type,
            command=command,
            temp_result=temp_result
        )

    return event_check


def __inject_server_list(func: Callable[..., Awaitable[str]]) -> Callable:
    """
    检查服务器列表是否为空
    :param func: 发送 rcon cmd 至目标服务器的函数
    :return: 装饰后的发送函数
    """

    @__get_server_list_by_event
    async def wrapper(
            matcher: Matcher,
            server_list: Optional[List[str]],
            bot: Union[QQBot, OneBot],
            event: Union[
                QQGuildMessageEvent, QQGroupAtMessageCreateEvent, OneBotGroupMessageEvent, OneBotGuildMessageEvent
            ],
            is_cmd: bool,
            command_type: Optional[str],
            command: Optional[str],
            temp_result: str,
    ):
        if server_list:
            return await func(
                server_list=server_list,
                bot=bot,
                event=event,
                is_cmd=is_cmd,
                command=command,
                command_type=command_type,
                temp_result=temp_result
            )
        elif is_cmd:
            return await matcher.finish("该群聊没有对应的服务器，无法发送")
        else:
            return

    return wrapper


@__inject_server_list
async def __send_common_to_target_server(
        server_list: Optional[List[str]],
        bot: Union[QQBot, OneBot],
        event: Union[
            QQGuildMessageEvent, QQGroupAtMessageCreateEvent, OneBotGroupMessageEvent, OneBotGuildMessageEvent
        ],
        is_cmd: bool,
        command_type: Optional[str],
        command: Optional[str],
        temp_result: str
) -> str:
    """
    发送命令到目标服务器
    :param is_cmd: 是否为命令
    :param server_list: 服务器列表
    :param command: 命令
    :param temp_result: 临时结果
    :return: 去除末尾换行符的结果
    """
    for server_name in server_list:
        if mc_bot := __get_mc_bot(server_name):
            server_config = plugin_config.server_dict.get(server_name)

            send_temp_result = f"发送至服务器：{server_name} "

            if is_cmd:
                send_temp_result += f"命令：{command} "

                if server_config.rcon_cmd and mc_bot.rcon:
                    if command_type == "title":
                        title = command.split("\n") if "\n" in command else (command, "")
                        title_cmd = f'title @a title ["{title[0].strip()}"]'
                        title_result = (await mc_bot.send_rcon_cmd(command=title_cmd))[0]
                        if title[1]:
                            subtitle_cmd = f'title @a subtitle ["{title[1].strip()}"]'
                            title_result += (await mc_bot.send_rcon_cmd(command=subtitle_cmd))[0]
                        send_temp_result += f"结果：{title_result}"
                    elif command_type == "command":
                        response = await mc_bot.send_rcon_cmd(command=command)
                        send_temp_result += f"结果：{response[0]}\n"
                    else:
                        cmd = parse_qq_screen_cmd_to_rcon_model(command_type, command)
                        response = await mc_bot.send_rcon_cmd(command=cmd)
                        send_temp_result += f"结果：{response[0]}\n"
                elif server_config.rcon_cmd and not mc_bot.rcon:
                    send_temp_result += "选择了Rcon发送命令，但无rcon可用，无法发送命令\n"
                else:
                    if command_type == "title":
                        title = command.split("\n") if "\n" in command else (command, "")
                        await mc_bot.send_title(title=title[0].strip(), subtitle=title[1].strip())
                    elif command_type == "action_bar":
                        await mc_bot.send_actionbar(message=command)
                    else:
                        await mc_bot.send_msg(message=command)
                        send_temp_result += "结果：没有可用的命令发送，请检查Rcon或其他配置"
                        continue
                    send_temp_result += "结果：成功\n"

            else:
                send_temp_result += "消息："

                if server_config.rcon_msg and mc_bot.rcon:
                    msg, text = await parse_qq_msg_to_rcon_model(bot=bot, event=event)
                    msg_json_data = json.dumps(msg, cls=DataclassEncoder)
                    send_temp_result += f"{text} "
                    response = await mc_bot.send_rcon_cmd(command=f"tellraw @a {msg_json_data}")
                    send_temp_result += f"结果：{response[0]}\n"

                elif server_config.rcon_msg and not mc_bot.rcon:
                    send_temp_result += "选择了Rcon发送消息，但无rcon未开启，无法发送消息\n"

                else:
                    msg, text = await parse_qq_msg_to_base_model(bot=bot, event=event)
                    send_temp_result += f"{text}\n"
                    await mc_bot.send_msg(message=msg)

            temp_result += send_temp_result

        else:
            temp_result += f"{server_name}：未找到服务器 Bot\n"

    temp_result = temp_result.removesuffix("\n")
    logger.debug(f"[MC_QQ]丨{temp_result}")

    return temp_result if is_cmd else ""


async def send_command_to_target_server(
        matcher: Matcher,
        bot: Union[QQBot, OneBot],
        event: Union[
            QQGuildMessageEvent,
            QQGroupAtMessageCreateEvent,
            OneBotGroupMessageEvent,
            OneBotGuildMessageEvent
        ],
        command: str
):
    """
    发送命令到目标服务器
    :param matcher: 命令匹配器
    :param bot: Bot对象
    :param event: 事件
    :param command: 命令
    :return: 去除末尾换行符的结果
    """
    return await __send_common_to_target_server(
        matcher=matcher,
        bot=bot,
        event=event,
        is_cmd=True,
        command_type="command",
        command=command
    )


async def send_action_bar_to_target_server(
        matcher: Matcher,
        bot: Union[QQBot, OneBot],
        event: Union[
            QQGuildMessageEvent, QQGroupAtMessageCreateEvent, OneBotGroupMessageEvent, OneBotGuildMessageEvent
        ],
        action_bar
):
    """
    发送actionbar到目标服务器
    :param matcher: 命令匹配器
    :param bot: Bot对象
    :param event: 事件
    :param action_bar: actionbar
    :return: 去除末尾换行符的结果
    """
    return await __send_common_to_target_server(
        matcher=matcher,
        bot=bot,
        event=event,
        is_cmd=True,
        command_type="action_bar",
        command=action_bar
    )


async def send_title_to_target_server(
        matcher: Matcher,
        bot: Union[QQBot, OneBot],
        event: Union[
            QQGuildMessageEvent, QQGroupAtMessageCreateEvent, OneBotGroupMessageEvent, OneBotGuildMessageEvent
        ],
        arg: str,
):
    """
    发送title到目标服务器
    :param matcher: 命令匹配器
    :param bot: Bot对象
    :param event: 事件
    :param arg: title
    :return: 去除末尾换行符的结果
    """
    return await __send_common_to_target_server(
        matcher=matcher,
        bot=bot,
        event=event,
        is_cmd=True,
        command_type="title",
        command=arg
    )


async def send_message_to_target_server(
        matcher: Matcher,
        bot: Union[QQBot, OneBot],
        event: Union[
            QQGuildMessageEvent,
            QQGroupAtMessageCreateEvent,
            OneBotGroupMessageEvent,
            OneBotGuildMessageEvent
        ]
):
    """
    发送消息到目标服务器
    :param matcher: 命令匹配器
    :param bot: Bot对象
    :param event: 事件
    :return: 去除末尾换行符的结果
    """
    return await __send_common_to_target_server(
        matcher=matcher,
        bot=bot,
        event=event,
        is_cmd=False,
    )


__all__ = [
    "send_title_to_target_server",
    "send_command_to_target_server",
    "send_message_to_target_server",
    "send_action_bar_to_target_server",
]
