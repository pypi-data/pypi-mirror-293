# XoT: A Modular X of Thought Library

XoT is a Python library designed to facilitate the creation, sharing, and training of X of Thought (XoT) agents.
These agents are implemented using modular components known as Strategies, allowing for flexible and composable reasoning systems. Inspired by PyTorch's modular design, DSPy's signature-based approach, and Hugging Face's emphasis on shareability, XoT offers a powerful framework for building multi-modal reasoning pipelines that can be fine-tuned and shared across different tasks and domains.

# Installation
```bash
pip install xot
```

# TODO
# Example Usage

## Loading strategy from hub
```python
from xot import AutoStrategy
from datasets import load_dataset

strat = AutoStrategy.from_pretrained('PrimeIntellect/Numina-TIR')
ds = load_dataset('openai/gsm8k')
print(strat)

for q, a in zip(ds['question'], ds['answer'])
    output, log = strat(q, output_log=True)
    print(output, a)
```

## Creating your own strategy and pushing it to the hub
```python
import xot

# Define a simple strategy
class MyStrategy(xot.Strategy):
    def __init__(self):
        super().__init__()
        self.rationale = xot.steps.Rationale("Provide detailed image prompt to improve aesthetics")
        self.image_gen = xot.steps.AutoImageGenerator.from('black-forest-labs/FLUX.1-dev')

    def forward(self, input: str):
        prompt = self.rationale(input)
        image = self.image_gen(prompt)
        return image

strat = MyStrategy()
print(strat)

img = strat("porsche 911")
img.save('porsche_911.png')

strat.push_to_hub('my_username')
```

# Getting Started
To get started with XoT, check out the [documentation](/) which provides detailed guides on creating strategies, fine-tuning them and sharing your work with the community.

# Core Concepts

## Strategy
A Strategy in XoT is the overarching blueprint that defines how an agent thinks and reasons. It encapsulates the following components:

- **Objective / Vision:** The high-level goal or purpose of the strategy.
- **Policy / Constitution:** The guiding principles or methods used to achieve the objective.

## Configuration
Configuration is where the fine-tuning happens. It allows users to customize the behavior of their strategies through:

- **Hyperparameters:** Key variables that influence the behavior of the strategy.
- **Distributions:** Ranges or specific values that hyperparameters can take, enabling higher diversity trajectories for synthetic data generation.

## Step
A Step represents a single unit of reasoning or action within a strategy.
Steps are defined by their Signatures—a general template describing what the step should accomplish without being tied to a specific implementation.

Steps can be categorized as:
- Reasoning:
  - Rationale: Logic or explanation behind decisions.
  - Explainer: Components that provide understandable justifications.
- Tools:
  - ImageGenerator: Generates images based on input data.
  - Calculator: Performs arithmetic or logical calculations.
  - Terminal: Executes shell commands or scripts.
  - WebSearch: Queries the web for information.
  - FunctionCall: Calls a specific function or API.
- Modality Adapters:
  - TextToImage: Converts text input to an image format.
  - ImageToText: Converts image input to a text format.
  - ...and more for Audio, Video, Graphs, Time series, etc.
- Memory Interfaces:
  - ShortTerm: Components managing short-term memory.
  - LongTerm: Components managing long-term memory.
  - Working: Components for active, working memory.
- Diversifier:
  - Components specialized in generating diverse training data, crucial for robust strategy development.


## Metrics
XoT includes built-in Metrics to evaluate the performance of strategies and individual steps.
Metrics help in understanding the effectiveness, efficiency, and accuracy of the reasoning process.

## Visualizer
The Visualizer provides tools for inspecting and understanding the behavior of strategies and steps.
This feature is crucial for debugging, sharing and communicating strategies with others.

# Key Features
- PyTorch-inspired Composability: Design reasoning components using a familiar and flexible modular system akin to PyTorch’s nn.Module, but for thought processes.
- Modality-Agnostic Design: Supports a wide range of input and output modalities, including text, image, audio, video, graphs, and more.
- Strategy Sharing and Fine-Tuning: Emphasis on reusing and fine-tuning existing strategies rather than starting from scratch, making it easy to adapt strategies to new tasks.
- Dataset Generation and Trajectory Evaluation: Built-in support for creating diverse datasets and evaluating the paths taken by reasoning strategies.
- Flexible Configuration System: Customize your strategies with fine-grained control over prompts, weights, and other hyperparameters.
- Agent Support: Special subsets of strategies designed for memory-intensive tasks, with support for various types of memory interfaces.

# Contributing
Contributions to XoT are very much welcome!
If you'd like to contribute, please check out [contributing guide]().

# License
XoT is licensed under the MIT License. See the [LICENSE]() file for more information.
