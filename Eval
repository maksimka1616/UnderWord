from telethon import events
from config import client, owner
import asyncio
import io
import traceback
from html import escape
from contextlib import redirect_stdout


def escape_html(text):
    return escape(str(text))


def register_handlers():
    handlers = []

    @client.on(events.NewMessage(pattern='^/e\s+(.+)$'))
    async def eval_command(event):
        if event.sender_id != owner:
            return
        code = event.pattern_match.group(1)
        message = await event.respond("Выполняю...", parse_mode="html")
        await event.delete()
        stdout = io.StringIO()

        exec_globals = {
            'client': client,
            'event': event,
            'asyncio': asyncio,
            'print': lambda *args, sep=" ", end="\n": print(*args, sep=sep, end=end, file=stdout)
        }

        try:

            exec_locals = {}
            with redirect_stdout(stdout):
                exec(
                    f"""
async def _():
    try:
        global result
        result = None
        async def temp():
          return {code}
        exec_result = await temp()
        if exec_result is not None:
          result = str(exec_result)
    except Exception as e:
        print(traceback.format_exc())
""",
                    exec_globals,
                    exec_locals
                )

                await exec_locals['_']()

            result = stdout.getvalue()
            if not result.strip():
                result = exec_locals.get('result', '')
                if result is None or not result:
                    try:
                        result = str(eval(code, exec_globals, exec_locals))
                    except:
                        result = "Успешно"

            response = (f'💻<b> Код:</b>'
                        f'\n<pre><code class="language-python">{escape_html(code)}</code></pre>'
                        f'\n'
                        f'\n✅<b> Результат:</b>'
                        f'\n<pre><code class="language-python">{escape_html(result)}</code></pre>')

            await message.edit(response)
        except Exception as e:
            error = traceback.format_exc()
            response = (f'💻<b> Код:</b>'
                        f'\n<pre><code class="language-python">{escape_html(code)}</code></pre>'
                        f'\n'
                        f'\n🚫<b> Ошибка:</b>'
                        f'\n<pre><code class="language-error">{escape_html(error)}</code></pre>')
            await message.edit(response)

    handlers.append(eval_command)
    return handlers
