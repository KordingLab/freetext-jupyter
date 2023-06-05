"""
A standalone Python file that implements a textbox widget for Jupyter notebooks.
There is a textbox and a submit button. When the submit button is clicked,
the textbox is disabled and the text is sent to the server. This can take a
while, so the button is disabled until the server responds and the text of
the button is replaced with a loading indicator.
The submission is a POST and has a body that looks like this:

```json
{
  "assignment_id": "string", // will be provided in the constructor of FreetextWidget
  "submission_string": "string" // the text the student wrote in the textbox
}
```

When the server responds,
the textarea is re-enabled and the button is re-enabled with the original
text. Below the textbox is a div that will be populated with the server's
response, per the following spec:
The response is a JSON array that looks like this:

```json
{
    "feedback_string": "string",
    "source": "string",
    "location": [
      "string",
      "string"
    ]
}
```

The `feedback_string` is the feedback that should be displayed to the user; the
rest can be ignored for now. Each item of feedback should be displayed as its
own paragraph.
"""


import requests
from ipywidgets import widgets, Layout


class FreetextWidget:
    def __init__(
        self,
        assignment_id: str,
        button_text="Submit",
        server_base_url="http://localhost:9900",
    ):
        self.assignment_id = assignment_id
        self.textbox = widgets.Textarea()
        # Styling for textbox
        self.textbox.layout.width = "auto"
        self.textbox.layout.height = "auto"
        self.textbox.layout.border = "solid 1px"
        self.textbox.layout.padding = "0.5em"
        self.textbox.layout.margin = "0.5em"
        self.textbox.layout.resize = "both"
        # Sans-serif font:
        self.textbox.layout.font_family = "sans-serif"
        self.textbox.layout.font_size = "16px"
        self.prompt = widgets.HTML()

        # Placeholder text (until it's replaced by the server round-trip):
        self.textbox.placeholder = f"Loading question {assignment_id}..."

        # Asynchronously load the question text from the server:
        response = requests.get(f"{server_base_url}/assignments/{assignment_id}")
        if response.status_code != 200:
            self.textbox.placeholder = (
                f"Error when getting question: {response.status_code}: {response.text}"
            )
            return

        self.textbox.placeholder = ""
        self.prompt.value = response.json()["student_prompt"]

        self.button = widgets.Button(
            description=button_text, layout=Layout(width="auto")
        )

        self.feedback = widgets.HTML()
        self.server_base_url = server_base_url

        self.button.on_click(self.submit_text)

        self.container = widgets.VBox(
            [self.prompt, self.textbox, self.button, self.feedback]
        )

    def submit_text(self, _):
        self.textbox.disabled = True
        self.button.disabled = True
        self.button.description = "Loading..."

        data = {
            "assignment_id": self.assignment_id,
            "submission_string": self.textbox.value,
        }
        response = requests.post(f"{self.server_base_url}/feedback", json=data)

        if response.status_code != 200:
            self.feedback.value = (
                f"Error when getting feedback: {response.status_code}: {response.text}"
            )
            return

        feedback_strings = [fb["feedback_string"] for fb in response.json()]
        feedback_html = "<br>".join(f"<p>{s}</p>" for s in feedback_strings)
        self.feedback.value = feedback_html

        self.textbox.disabled = False
        self.button.disabled = False
        self.button.description = "Submit"

    def display(self):
        display(self.container)
