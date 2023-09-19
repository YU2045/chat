import flet as ft
from dataclasses import dataclass

import uuid

WIDTH = 400
HEIGHT = 800


@dataclass
class Message:
    id: uuid.UUID = ''
    session_id: str = ''
    text: str = ''
    message_type: str = "chat_message"
    like: int = 0


def main(page: ft.Page):
    class MessageRow(ft.UserControl):
        def __init__(self, message: Message, width: int = 800):
            super().__init__()
            self.vertical_alignment = "start"
            self.message = message
            self.likes = ft.Text(self.message.like)
            self.width = width
            self.like_button = ft.IconButton(
                ft.icons.THUMB_UP_OUTLINED, on_click=increment_like, data=self.message
            )

        def build(self):
            return ft.Row(
                controls=[
                    ft.Text(
                        self.message.text, selectable=True, width=self.width * 0.7
                    ),
                    self.like_button,
                    self.likes,
                ],
            )

    page.window_width = WIDTH
    page.window_height = HEIGHT
    page.horizontal_alignment = "stretch"
    page.title = "Flet Chat"

    def send_message_click(e):
        if new_message.value != '':
            page.pubsub.send_all(
                Message(
                    uuid.uuid4(),
                    page.session_id,
                    new_message.value,
                    message_type='chat_message',
                )
            )
            new_message.value = ''
            new_message.focus()
            page.update()

    def increment_like(e):
        message = e.control.data
        message.like += 1
        message.message_type = 'increment'
        page.pubsub.send_all(message)
        page.update()

    def on_message(message: Message):
        if message.message_type == 'chat_message':
            m = MessageRow(message, WIDTH)

            if page.session_id == message.session_id:
                m.like_button = ft.IconButton(
                    ft.icons.THUMB_UP,
                    opacity=0.5,
                    disabled=True,
                )

            chat.controls.append(m)

        elif message.message_type == 'increment':
            id = message.id
            for row in chat.controls:
                if row.message.id == id:
                    m = row
                    break

            m.likes.value = m.message.like
            m.update()

        page.update()

    page.pubsub.subscribe(on_message)

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


if __name__ == '__main__':
    ft.app(port=12500, target=main, view=ft.WEB_BROWSER)
