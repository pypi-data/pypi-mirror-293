<div align="center">

**FADE: Empowering everyone to detect fallacies in real time with ease!**
<h3>

[[Our Website]](https://aiflowsolutions.github.io/site-agi-flow-solutions/) | [[Our Research Website]](https://aiflowsolutions.github.io/site-agi-flow-research-robotics/) | [[pré-print FADE paper]](docs\assets\Automating_fallacy_detection.pdf)


</h3>
</div>
## Table of contents

- [Overview](#overview)
- [Roadmap](#roadmap)
- [Installation](#installation)
- [Setting up FADE](#setting-up-fade)
- [Contribuition](#contribuition)
- [Issue Reporting](#issue-reporting)
- [Contact us](#contact-us)
- [License](#license)


## Overview
FADE is a project aimed at detecting fallacies in various forms of speech. Upgrading and optimizing this tool will enable the identification of unethical, manipulative, and persuasive discourse from politicians, influencers, and even our friends and families.

## Roadmap
- Implement a video-transcription feature
- Optimize current prompt system
- Fine-tune a LLM to test if the results are better

## Installation
We recommend setting up a virtual environment before starting to work with FADE:
- Create a virtual environment: `python -m venv .venv`
- Activate your virtual environment: `.\.venv\Scripts\activate`

To begin using our library, simply install it via pip:
`pip install fade`

## Setting Up FADE
Before running the bellow script create a `.env` file and place your API Key inside it: `GROQ_API_KEY="your_api_key"`. 

### Simple detection in string
```python
from src.fade.fallacy_detector import detect_fallacy

phrase = "I'm better than you because I'm taller than you"

print(detect_fallacy(phrase))
```

### Simple detection in speech-to-text
For this feature you have to setup you google cloud feature  first and your google-cloud-speech api. 

```python
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.fade.transcription_features.live_transcription import main as lt
from src.fade.fallacy_detector import *

text = lt()

print(detect_fallacy(text))
```
## Contribuition
FADE is open-source and we welcome contributions. If you're looking to contribute, please:

- Fork the repository.
- Create a new branch for your feature.
- Add your feature or improvement.
- Send a pull request.

## Issue Reporting

If you encounter any problems while using our library, please don't hesitate to [create an issue](https://github.com/AiFlowSolutions/MADS/issues) on GitHub. When reporting issues, please provide as much detail as possible, including:

- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Any error messages or stack traces

Your feedback is valuable to us and will help improve the library for everyone. Thank you for contributing to the project!

## Contact Us

If you have any questions, suggestions, or feedback regarding FADE, please feel free to reach out to us:

- **Email**: [diogofranciscop@hotmail.com](mailto:diogofranciscop@hotmail.com)
- **Email**: [duarte.gcgcomes@gmail.com](duarte.gcgcomes@gmail.com)

We are committed to improving FADE based on your input and look forward to hearing from you!

## Ackonwledgments
A heartfelt thank you to all the contributors of the [Fallacie score board repo](https://github.com/latent-variable/FallacyScoreboard). Your dedication and hard work have been instrumental in making this project possible. We deeply appreciate the entire community's support and involvement.

## License
FADE is released under the MIT License.