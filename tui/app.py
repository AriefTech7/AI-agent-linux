from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import (
    Header,
    Footer,
    Static,
    Input,
    ListView,
    ListItem,
    Label,
)
from textual import work


class AlexiTUI(App):

    CSS = """
    Screen {
        background: #0d1117;
    }

    #main {
        height: 1fr;
    }

    #sidebar {
        width: 20%;
        border: solid #30363d;
        padding: 1;
    }

    #chat {
        width: 60%;
        border: solid #30363d;
        padding: 1;
    }

    #status {
        width: 20%;
        border: solid #30363d;
        padding: 1;
    }

    #chat-log {
        height: 1fr;
        overflow-y: auto;
    }

    #message-input {
        dock: bottom;
    }

    .title {
        text-style: bold;
    }
    """

    BINDINGS = [
        ("ctrl+c", "quit", "Quit"),
        ("ctrl+n", "new_chat", "New Chat"),
    ]

    def __init__(self, agent,thread_id):
        super().__init__()

        self.agent = agent

        self.thread_id = thread_id

        self.chat_content = ""

    def compose(self) -> ComposeResult:

        yield Header()

        with Horizontal(id="main"):

            with Vertical(id="sidebar"):

                yield Static(
                    "HISTORY",
                    classes="title",
                )

                yield ListView(
                    ListItem(
                        Label("> New Chat")
                    )
                )

            with Vertical(id="chat"):

                yield Static(
                    "ALEXI CHAT",
                    classes="title",
                )

                yield Static(
                    self.chat_content,
                    id="chat-log",
                )

                yield Input(
                    placeholder="Ketik pesan...",
                    id="message-input",
                )

            with Vertical(id="status"):

                yield Static(
                    "STATUS",
                    classes="title",
                )

                yield Static(
                    "● Agent    ONLINE\n"
                    "● Memory   ONLINE\n"
                    "● Tools    READY"
                )

        yield Footer()

    async def on_input_submitted(
        self,
        event: Input.Submitted,
    ) -> None:

        message = event.value.strip()

        if not message:
            return

        event.input.value = ""

        self.chat_content += (
            f"\nYou:\n{message}\n\n"
            f"Alexi:\n"
        )

        self.update_chat()

        # Jangan await agent langsung di event handler.
        # Jalankan sebagai Textual worker.
        self.process_message(message)

    def update_chat(self):

        chat = self.query_one(
            "#chat-log",
            Static,
        )

        chat.update(
            self.chat_content
        )

    @work(exclusive=True)
    async def process_message(
        self,
        message: str,
    ):

        config = {
            "configurable": {
                "thread_id": self.thread_id
            }
        }

        try:

            async for msg, metadata in self.agent.astream(
                {
                    "messages": [
                        (
                            "user",
                            message,
                        )
                    ]
                },
                config=config,
                stream_mode="messages",
            ):

                if not msg.content:
                    continue

                # Hanya tampilkan output model
                # jika metadata tersedia.
                node = metadata.get(
                    "langgraph_node"
                )

                # Filter ini bisa Anda sesuaikan
                # dengan nama node graph Anda.
                if node:

                    content = msg.content

                    if isinstance(content, str):

                        self.chat_content += content

                        self.update_chat()

            self.chat_content += "\n"

            self.update_chat()

        except Exception as error:

            self.chat_content += (
                f"\n\n[ERROR]\n{error}\n"
            )

            self.update_chat()

    def action_new_chat(self):

        import uuid

        self.thread_id = str(
            uuid.uuid4()
        )

        self.chat_content = (
            "Percakapan baru dibuat.\n"
        )

        self.update_chat()