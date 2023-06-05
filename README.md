# freetext_jupyter

This is a IPyWidget that interfaces with the Kording Lab `freetext` server. The freetext server is an automatic text feedback system that can be used to provide feedback to students on their written responses to questions.

## Overview

This widget takes the form of a simple text box. The student is presented with the prompt text and a place to answer the question. Upon submitting, the `freetext` server engages a large language model with general knowledge as well as fine-grained knowledge about the question (provided by the instructor) to generate feedback for the student. The feedback is then displayed to the student under the text area, in near-real time, without waiting for a human instructor.

As in all LLM-based tools, caveat emptor: the feedback is not always correct, and it is not always useful. But it is often correct, and it is often useful. The feedback is not meant to replace human instructors, but rather to augment them. The feedback is meant to be used as a starting point to engage meaningful discussion between the students and the instructor.

## Installation

```bash
pip install freetext_jupyter
```

## Usage

```python
from freetext_jupyter import FreetextWidget

FreetextWidget(
    # This ID is generated by the instructor by creating a new assignment in
    # the freetext server. For more information, see the freetext documentation
    # for your community's server.
    "07b2c3ef-0f97-46bc-a11e-fc5c06c381c2"
)
```

https://github.com/KordingLab/fretext-jupyter/assets/693511/090a2445-7867-4428-a28a-d5f3a2c96f68