import flet as ft
from dataclasses import dataclass


@dataclass
class Message:
    user_name: str = '',
    text: str = '',
    message_type: str = 'chat_message',
    like: int = 0


class ChatMessage(ft.Row):
    def __init__(self, message: Message):
        super().__init__()
        like_text = ft.Text(message.like)

        def increment_like(e):
            message.like += 1
            like_text.value = message.like
            self.update()

        self.vertical_alignment = "start"
        self.controls = [
            ft.Row(
                controls=[
                    ft.Container(
                        expand=True,
                        content=ft.Text(
                            message.text,
                            width=200,
                            selectable=True
                        ),
                    ),
                    ft.Container(
                        expand=True,
                        content=ft.IconButton(
                            icon=ft.icons.THUMB_UP_OUTLINED,
                            on_click=increment_like,
                        ),
                    ),
                    like_text,
                ]
            )
        ]

    def get_initials(self, user_name: str):
        if user_name is None:
            return ' '
        return user_name[:1].capitalize()

    def get_avatar_color(self, user_name: str):
        colors_lookup = [
            ft.colors.AMBER,
            ft.colors.BLUE,
            ft.colors.BROWN,
            ft.colors.CYAN,
            ft.colors.GREEN,
            ft.colors.INDIGO,
            ft.colors.LIME,
            ft.colors.ORANGE,
            ft.colors.PINK,
            ft.colors.PURPLE,
            ft.colors.RED,
            ft.colors.TEAL,
            ft.colors.YELLOW,
        ]
        return colors_lookup[hash(user_name) % len(colors_lookup)]


def main(page: ft.Page):
    page.horizontal_alignment = "stretch"
    page.title = "Flet Chat"
    page.window_width = 400
    page.window_height = 800

    # def join_chat_click(e):
    #     if not join_user_name.value:
    #         join_user_name.error_text = "Name cannot be blank!"
    #         join_user_name.update()
    #     else:
    #         page.session.set("user_name", join_user_name.value)
    #         page.dialog.open = False
    #         new_message.prefix = ft.Text(f"{join_user_name.value}: ")
    #         page.pubsub.send_all(
    #             Message(
    #                 user_name=join_user_name.value,
    #                 text=f"{join_user_name.value} has joined the chat.",
    #                 message_type="login_message"
    #             )
    #         )
    #         page.update()

    def send_message_click(e):
        if new_message.value != "":
            page.pubsub.send_all(
                Message(
                    page.session.get("user_name"),
                    new_message.value,
                    message_type="chat_message")
            )
            new_message.value = ""
            new_message.focus()
            page.update()

    def on_message(message: Message):
        if message.message_type == "chat_message":
            m = ChatMessage(message)
        elif message.message_type == "login_message":
            m = ft.Text(message.text, italic=True, color=ft.colors.WHITE, size=12)
        chat.controls.append(m)
        chat.controls.append(ft.Divider())
        page.update()

    page.pubsub.subscribe(on_message)

    # A dialog asking for a user display name
    # join_user_name = ft.TextField(
    #     label="Enter your name to join the chat",
    #     autofocus=True,
    #     on_submit=join_chat_click,
    # )
    # page.dialog = ft.AlertDialog(
    #     open=True,
    #     modal=True,
    #     title=ft.Text("Welcome!"),
    #     content=ft.Column([join_user_name], width=300, height=70, tight=True),
    #     actions=[ft.ElevatedButton(text="Join chat", on_click=join_chat_click)],
    #     actions_alignment="end",
    # )

    # Chat messages
    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )

    # A new message entry form
    new_message = ft.TextField(
        hint_text="Write a message...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        on_submit=send_message_click,
    )

    # Add everything to the page
    page.add(
        ft.Container(
            content=chat,
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=5,
            padding=10,
            expand=True,
        ),
        ft.Row(
            [
                new_message,
                ft.IconButton(
                    icon=ft.icons.SEND_ROUNDED,
                    tooltip="Send message",
                    on_click=send_message_click,
                ),
            ]
        ),
    )
    new_message.value = '教育教育教育教育教育教育教育教育教育教育教育教育教育'
    send_message_click(page.event_handlers)


if __name__ == '__main__':
    ft.app(port=8500, target=main, view=ft.WEB_BROWSER)
