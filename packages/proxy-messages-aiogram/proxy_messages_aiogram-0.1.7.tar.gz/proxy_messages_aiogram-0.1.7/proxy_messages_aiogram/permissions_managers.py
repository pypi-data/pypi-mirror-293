from aiogram import Bot
from aiogram.types import ChatMemberAdministrator, ChatMemberRestricted


class CheckPermission(object):
    bot: Bot
    chat_id: int

    chat_is_existing: bool
    chat_is_forum: bool
    bot_can_manage_topics: bool
    missed_permissions: list[str]

    def __init__(self, bot: Bot, chat_id: int) -> None:
        self.bot = bot
        self.chat_id = chat_id

        self.chat_is_existing = False
        self.chat_is_forum = False
        self.bot_can_manage_topics = False
        self.missed_permissions = []

    async def check(self):
        try:
            self._target_chat = await self.bot.get_chat(self.chat_id)

        except BaseException:
            return

        self.chat_is_existing = True
        self.chat_is_forum = self._target_chat.is_forum

        self._target_chat_bot_member = await self.bot.get_chat_member(self.chat_id, self.bot.id)

        self.bot_is_admin = isinstance(self._target_chat_bot_member, ChatMemberAdministrator)

        for target_permission_name in [
            # 'can_send_audios',
            # 'can_send_documents',
            # 'can_send_photos',
            # 'can_send_videos',
            # 'can_send_video_notes',
            # 'can_send_voice_notes',
            # 'can_send_polls',
            # 'can_send_other_messages',
            # 'can_add_web_page_previews',
            # 'can_change_info',
            # 'can_invite_users',
            'can_pin_messages',
            'can_manage_topics',
        ]:
            if not getattr(self._target_chat_bot_member, target_permission_name, False):
                self.missed_permissions.append(target_permission_name)

    def missed_permissions_to_text(self):
        text = ''
        for missed_permission in self.missed_permissions:
            text += f'- {missed_permission}\n'
        return text
