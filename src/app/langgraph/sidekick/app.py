import gradio as gr
from src.app.langgraph.sidekick.sidekick import Sidekick

from src.app.settings import get_settings

settings = get_settings()


async def setup():
    sidekick = Sidekick()
    await sidekick.setup()
    return sidekick


async def process_message(sidekick: Sidekick, message, success_criteria, history):
    if sidekick:
        results = await sidekick.run_superstep(message, success_criteria, history)
        return results, sidekick
    return history, sidekick


async def reset():
    new_sidekick = Sidekick()
    await new_sidekick.setup()
    return "", "", None, new_sidekick


def free_resources(sidekick: Sidekick):
    print("Cleaning up")
    try:
        if sidekick:
            sidekick.cleanup()
    except Exception as e:
        print(f"Exception during cleanup: {e}")


with gr.Blocks(title="Sidekick", theme=gr.themes.Default(primary_hue="emerald")) as ui:
    gr.Markdown("##Personal Co-Worker")
    sidekick = gr.State(delete_callback=free_resources)

    with gr.Row():
        chatbot = gr.Chatbot(label="Sidekick", height=300)
    with gr.Group():
        with gr.Row():
            message = gr.Textbox(
                show_label=False, placeholder="Your request to the Sidekick"
            )
        with gr.Row():
            success_criteria = gr.Textbox(
                show_label=False, placeholder="What are your success criteria?"
            )
    with gr.Row():
        reset_button = gr.Button("Reset", variant="stop")
        go_button = gr.Button("Go!", variant="primary")

    ui.load(setup, [], [sidekick])
    message.submit(
        process_message,
        [sidekick, message, success_criteria, chatbot],
        [chatbot, sidekick],
    )
    success_criteria.submit(
        process_message,
        [sidekick, message, success_criteria, chatbot],
        [chatbot, sidekick],
    )
    go_button.click(
        process_message,
        [sidekick, message, success_criteria, chatbot],
        [chatbot, sidekick],
    )
    reset_button.click(reset, [], [message, success_criteria, chatbot, sidekick])


ui.launch(inbrowser=True)
