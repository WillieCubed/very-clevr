import gradio as gr
import numpy as np


DEMO_TITLE = "Very CLEVR"

DEMO_DESCRIPTION = """
# Overview

This is a system that analyzes concepts. It uses a model trained on the CLEVR
dataset coupled with some other fancy extras to identify concepts within
data presented to it.

## Usage

Right now, the demo is kind of broken. Here's how it's supposed to work:

- Upload an image
- Click submit
- See the concepts that were identified

# How It Works

~~Not at all~~

Magic.
"""

IMAGE_WIDTH = 512
IMAGE_HEIGHT = 512
IMAGE_SIZE = (IMAGE_WIDTH, IMAGE_HEIGHT)


class VeryClevrApp:
    """A wrapper for the app being run interactively."""

    def run(self, *args):
        text, image = args
        return (
            "Hello " + text + "!!",
            {},
            image / 255,
        )


def launch_interactive_demo(share_publicly=False):
    """Launches an interactive demo for inference of the Very CLEVR system.

    This starts the system using Gradio

    Args:
        share_publicly (bool): True if the demo should expose a public URL that connects to the client's device.
    """
    app = VeryClevrApp()

    color_map = {}

    demo = gr.Interface(
        title=DEMO_TITLE,
        description=DEMO_DESCRIPTION,
        fn=lambda text, image: app.run(text, image),
        inputs=[
            gr.inputs.Textbox(label="Input"),
            gr.inputs.Image(label="Input image", shape=IMAGE_SIZE),
        ],
        outputs=[
            gr.outputs.Textbox(label="Concept Name"),
            gr.outputs.HighlightedText(
                label="Concept identifiers", color_map=color_map
            ),
            gr.outputs.Image(label="Transformed Image"),
        ],
    )

    demo.launch(share=share_publicly)
