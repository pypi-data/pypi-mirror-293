# Archon - Create and Benchmark LLM Chains with JSON
As the number of large language models available increases, using different models in tandem can provide better results than one alone. Archon provides a modular framework for sampling, ranking, and fusing model responses with just a JSON config file. Check out our [Quick Start](#quick-start) guide to get started.
![Archon Overview Diagram](readme_assets/archon-overview.svg)


#### Table of Contents

- [Quick Start](#quick-start)
    - [Archon Installation](#archon-installation)
    - [Multi-Model Setup](#multi-model-setup)
    - [More Examples](#more-examples)
- [Benchmarks](#benchmarks)
    - [Add Your Own Benchmark](#add-your-own-benchmark)
- [Resources](#resources)

## Quick Start 
<a target="_blank" href="https://colab.research.google.com/drive/17EFD6ggW0rk5Qz-vBwOhP9RhCnLYviTt#scrollTo=ymybYfBTt4gu">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

### Archon Installation
We recommend using Archon within the archon/ directory of this repsitory. Our environment can be set up with
```
conda env create -f archon_env.yml
conda activate archon_env
pip install -r requirements.txt
````

Archon configs are instantiated via the [Archon](https://github.com/ScalingIntelligence/Archon/blob/main/archon/archon.py#L176) class in `archon.py`. Get started by cloning the repository and navigating to our [quickstart.py](https://github.com/ScalingIntelligence/Archon/blob/main/archon/quickstart.py) or creating your own starter file that imports our Archon class. 
```python
from archon import Archon
```
Archon is also publicly available for use at https://pypi.org/project/archon-ai/. You can run these examples from your own file after installing the latest Archon version.
```
pip install archon-ai
```

### Basic Example
Here's where the magic happens. Archon works by taking in a config file in JSON format that specifies the architecture you want to run and its available parameters. 
Say I want to ask GPT 4 Turbo a question and output a singular response. We could create a config that looks like this:
```
archon_config = {
    "name": "gpt-4-turbo-quickstart",
    "layers": [
         [
            {
                "type": "generator",
                "model": "gpt-4-turbo",
                "model_type": "OpenAI_API",
                "checkpoint": "",
                "top_k": 1,
                "temperature": 0.7,
                "max_context_length": 2048,
                "samples": 1
            }
        ]
    ]
}
```
To generate a response:
```python
# archon_config can also be stored and read from a file. Then passed to Archon()
archon = Archon(archon_config)

testing_instruction = [{"role": "user", "content": "How do I make a cake?"}]

response = archon.generate(testing_instruction)

print(response)
```
### Basic Multi-Model Setup
<a target="_blank" href="https://colab.research.google.com/drive/14ohSRBD9mDympZk0MO0MumWnjA4tCk1e#scrollTo=ZrxjlqILrWla">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

Let's move on to something more complicated. Let's say I want to sample Qwen 2 from Together 10 times, have Claude 3.5 Sonnet critique the responses, and then use both the original response and the critiques to generate an improved final output using Qwen 1.5 as the fuser. Here's what our config would look like:
```
archon_config =  {
    "name": "archon-testing",
    "layers": [
        [   
            {
                "type": "generator"
                "model": "Qwen/Qwen2-72B-Instruct",
                "model_type": "Together_API",
                "checkpoint": "",
                "temperature": 0.7,
                "max_context_length": 2048,
                "samples": 10
            }
        ],
        [
            {
                "type": "critic",
                "model": "claude-3-5-sonnet-20240620",
                "model_type": "Anthropic_API",
                "checkpoint": "",
                "temperature": 0.7,
                "max_context_length": 8192,
                "samples": 1
            }
        ],
        [
            {
                "type": "fuser",
                "model": "Qwen/Qwen1.5-110B-Chat",
                "model_type": "Together_API",
                "checkpoint": "",
                "top_k": 1,
                "temperature": 0.7,
                "max_context_length": 2048,
                "samples": 1
            }
        ]
    ]
}


```
### Advanced Multi-Model Setup
Finally, let's create an archon config that showcases multiple layers of generations, critics, and fusing. We'll start with 10 different generators models, critic the outputs, create 10 different fuses of the crticed responses (using the same models as the  generators), rank the outputs, and end with a fuser layer to merge the ranked responses.
![Advanced Architecture](readme_assets/archon-architecture-example.svg)
You'll notice each layer is defined within it's own array block and contains references to the models used in the layer.

```JSON
{
    "name": "quickstart-advanced",
    "layers": [
        [   
            {
                "type": "generator",
                "model": "gpt-4o",
                "model_type": "OpenAI_API",
                "checkpoint": "",
                "temperature": 0.7,
                "max_context_length": 2048, 
                "samples": 1
            },
            {
                "type": "generator",
                "model": "claude-3-5-sonnet-20240620",
                "model_type": "Anthropic_API",
                "checkpoint": "",
                "temperature": 0.7,
                "max_context_length": 2048,
                "samples": 1
            },
            {
                "type": "generator",
                "model": "Qwen/Qwen2-72B-Instruct",
                "model_type": "Together_API",
                "checkpoint": "",
                "temperature": 0.7,
                "max_context_length": 2048,
                "samples": 1
            },
            {
                "type": "generator",
                "model": "microsoft/WizardLM-2-8x22B",
                "model_type": "Together_API",
                "checkpoint": "",
                "temperature": 0.7,
                "max_context_length": 2048,
                "samples": 1
            },
            {
                "type": "generator",
                "model": "Qwen/Qwen1.5-110B-Chat",
                "model_type": "Together_API",
                "checkpoint": "",
                "temperature": 0.7,
                "max_context_length": 2048,
                "samples": 1
            },
            {
                "type": "generator",
                "model": "Qwen/Qwen1.5-72B-Chat",
                "model_type": "Together_API",
                "checkpoint": "",
                "temperature": 0.7,
                "max_context_length": 2048,
                "samples": 1
            },
            {
                "type": "generator",
                "model": "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
                "model_type": "Together_API",
                "checkpoint": "",
                "temperature": 0.7,
                "max_context_length": 2048,
                "samples": 1
            },
            {
                "type": "generator",
                "model": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
                "model_type": "Together_API",
                "checkpoint": "",
                "temperature": 0.7,
                "max_context_length": 2048,
                "samples": 1
            },
            {
                "type": "generator",
                "model": "mistralai/Mixtral-8x22B-Instruct-v0.1",
                "model_type": "Together_API",
                "checkpoint": "",
                "temperature": 0.7,
                "max_context_length": 2048,
                "samples": 1
            },
            {
                "type": "generator",
                "model": "databricks/dbrx-instruct",
                "model_type": "Together_API",
                "checkpoint": "",
                "temperature": 0.7,
                "max_context_length": 2048,
                "samples": 1
            }
        ],
        [
            {
                "type": "critic",
                "model": "Qwen/Qwen2-72B-Instruct",
                "model_type": "Together_API",
                "checkpoint": "",
                "temperature": 0.7,
                "max_context_length": 2048,
                "samples": 1
            }
        ],
        [
            {
                "type": "fuser",
                "model": "gpt-4o",
                "model_type": "OpenAI_API",
                "checkpoint": "",
                "temperature": 0.7,
                "max_context_length": 2048, 
                "samples": 1
            },
            {
                "type": "fuser",
                "model": "claude-3-5-sonnet-20240620",
                "model_type": "Anthropic_API",
                "checkpoint": "",
                "temperature": 0.7,
                "max_context_length": 2048,
                "samples": 1
            },
            {
                "type": "fuser",
                "model": "Qwen/Qwen2-72B-Instruct",
                "model_type": "Together_API",
                "checkpoint": "",
                "temperature": 0.7,
                "max_context_length": 2048,
                "samples": 1
            },
            {
                "type": "fuser",
                "model": "microsoft/WizardLM-2-8x22B",
                "model_type": "Together_API",
                "checkpoint": "",
                "temperature": 0.7,
                "max_context_length": 2048,
                "samples": 1
            },
            {
                "type": "fuser",
                "model": "Qwen/Qwen1.5-110B-Chat",
                "model_type": "Together_API",
                "checkpoint": "",
                "temperature": 0.7,
                "max_context_length": 2048,
                "samples": 1
            },
            {
                "type": "fuser",
                "model": "Qwen/Qwen1.5-72B-Chat",
                "model_type": "Together_API",
                "checkpoint": "",
                "temperature": 0.7,
                "max_context_length": 2048,
                "samples": 1
            },
            {
                "type": "fuser",
                "model": "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
                "model_type": "Together_API",
                "checkpoint": "",
                "temperature": 0.7,
                "max_context_length": 2048,
                "samples": 1
            },
            {
                "type": "fuser",
                "model": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
                "model_type": "Together_API",
                "checkpoint": "",
                "temperature": 0.7,
                "max_context_length": 2048,
                "samples": 1
            },
            {
                "type": "fuser",
                "model": "mistralai/Mixtral-8x22B-Instruct-v0.1",
                "model_type": "Together_API",
                "checkpoint": "",
                "temperature": 0.7,
                "max_context_length": 2048,
                "samples": 1
            },
            {
                "type": "fuser",
                "model": "databricks/dbrx-instruct",
                "model_type": "Together_API",
                "checkpoint": "",
                "temperature": 0.7,
                "max_context_length": 2048,
                "samples": 1
            }
        ],
        [
            {
                "type": "ranker",
                "model": "claude-3-5-sonnet-20240620",
                "model_type": "Anthropic_API",
                "top_k": 5,
                "checkpoint": "",
                "temperature": 0.7,
                "max_context_length": 2048,
                "samples": 1
            }
        ],
        [
            {
                "type": "fuser",
                "model": "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
                "model_type": "Together_API",
                "checkpoint": "",
                "temperature": 0.7,
                "max_context_length": 2048,
                "samples": 1
            }
        ]
    ]
}
```

### More Examples
Under ```archon/configs```, you can find more examples of increasingly complex LLM network-style systems <br />
Two systems we wanted to highlight: <br />
Improving GPT 4o using Archon <br />
<a target="_blank" href="https://colab.research.google.com/drive/14ohSRBD9mDympZk0MO0MumWnjA4tCk1e#scrollTo=ZrxjlqILrWla">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>
<br />
Using only open-sourced LLMs to outperform GPT 4o <br />
<a target="_blank" href="https://colab.research.google.com/drive/1mhXNc6xfR6CxrHv_tF2xcr5xzKmnA9nD#scrollTo=ZrxjlqILrWla">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

## Benchmarks
Once you have created a config, you can leverage pre-existing benchmark frameworks to assess accuracy. We provide classes for [AlpacaEval](https://github.com/tatsu-lab/alpaca_eval), [ArenaHardAuto](https://github.com/lm-sys/arena-hard-auto), and [MT Bench](https://huggingface.co/spaces/lmsys/mt-bench). The classes are under ```archon/benchmarks.py``` where you can modify the input question files under the class ```load_dataset()``` call.
Here is an example command for running your config against ArenaHardAuto:
```
python3 archon/gen_answers.py --benchmark arena_hard_auto --config archon/configs/<your-config-file>.json --output_dir outputs --parallel 16
```
This will run the model structure specified in your config file against the question set specified under the ArenaHardAuto class and output the responses in `.jsonl` format under an `outputs` folder. 

### Add Your Own Benchmark
To add your benchmark, you must edit the benchmarks.py file and add your benchmark class. The 'Benchmark' class can be used as a base class for interfacing between gen_answers.py and your benchmark. Lastly, make sure to add your evaluation to 'BENCHMARK_CLASSES' so it can be used as an argument in gen_answers.py

## Resources
### Inspiration
- 📚 [PyTorch](https://github.com/pytorch/pytorch/): placeholder
- 📚 [DSPy](https://github.com/stanfordnlp/dspy): placeholder
- 📚 [ARES](https://github.com/stanford-futuredata/ARES.git): placeholder
- 📚 [TextGrad](https://github.com/zou-group/textgrad?tab=readme-ov-file): placeholder

### Citation
```bibtex
@article{placeholder,
      title={Archon: Bending the Scaling Curves with Model Ensembling, Sampling, and Ranking},
      author={placeholder},
      year={2024},
      eprint={placeholder},
      archivePrefix={arXiv}
}
```

