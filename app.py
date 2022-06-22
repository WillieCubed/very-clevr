"""A quick script for casual use.

This script is also the one that is launched for the Gradio Hugging Face demo.

```bash
python app.py
```
"""

from very_clevr.app.demo import launch_interactive_demo

if __name__ == "__main__":
    launch_interactive_demo()
