from string import Template


task_templates = [
            {
            "name": "llm_efficiency",
            "full_name": "1LLM + 1GPU + 1Day: LLM Efficiency Challenge",
            "task": """train a model that performs as well as possible on a wide array of metrics. Start with an approved base model. Using only open-source data, fine-tune for a model on an A100 80GB GPU with a CUDA version of 11.7. 
            """,
            "metric": "A subset of the HELM benchmark",
            "dataset": """
            You are welcome to use any open sourced dataset. For example:
                - Databricks-Dolly-15
                - OpenAssistant Conversations Dataset (oasst1)
                - The Flan Collection
                - AllenAI Dolma
                - RedPajama-Data-1T
                - LIMA
            """,
            "models": """
            - ALBERT
            - BART
            - BERT
            - Bloom
            - Cerebras (btlm, GPT)
            - Colossal-LLaMA-2-7b-base
            - DeBERTa
            - DeciLM-6B
            - DistilBERT
            - Electra
            - Falcon
            - GPT2
            - GPT Neo, J, NeoX, Pythia
            - InternLM
            - LLaMA or Llama 2
            - Mistral
            - MPT
            - OpenLLaMA
            - OPT
            - Persimmon
            - Qwen
            - Red Pajama Base (not instruction tuned models)
            - RoBERTa
            - T5 
            - UL2
            """,
            "starter_code": "https://github.com/llm-efficiency-challenge/neurips_llm_efficiency_challenge",
            "compute": "One A100 80GB GPU, 128GB of RAM, 500GB of Disk",
            "time_limit": "24 hours",
            "result": "A huggingface model that performs as well as possible on a subset of the HELM benchmark",
            "rules": """
            - You may not train on the HELM benchmark directly. It is for evaluation only.
            - You will not be givn access to the evalutation data.
            - You may not use any data that is not open-source.
            """,
            "evaluation": """
            The model will be evaluated by running a subset of HELM benchmark along with a set of secret holdout tasks. The holdout tasks will consist of logic reasoning type of multiple-choice Q&A scenarios as well as conversational chat tasks. The model will be ranked based on their performance across all tasks. 
            """,
            "additional_info": """None""", 
            "formula": """score=Π(mean-win-rate(task))""",
        },
        {
            "name": "baby_lm",
            "full_name": "BabyLM Challenge (Strict-Small)",
            "task": """train a large language model on a pretraining corpus of approximately 10M words (Strict-Small). Optimize for performance on the BLiMP and BLiMP-supplement datasets, (Super)GLUE, and MSGS. You have 2 hours to complete the task.
            """,
            "dataset": """You can load the dataset with load_dataset(AlgorithmicResearchGroup/babylm)""",
            "dataset_shape": """
            DatasetDict({
                train: Dataset({
                    features: ['filename', 'content'],
                    num_rows: 6
                })
                test: Dataset({
                    features: ['filename', 'content'],
                    num_rows: 6
                })
                dev: Dataset({
                    features: ['filename', 'content'],
                    num_rows: 6
                })
            })
            """,
            "models": "Any trasformer model",
            "starter_code": "https://github.com/babylm/evaluation-pipeline-2024",
            "libraries": "Huggingface Transformers",
            "compute": "one A100 80GB GPU",
            "time_limit": "24 hours",
            "result": "A huggingface model that performs as well as possible on BLiMP and BLiMP-supplement datasets, (Super)GLUE, and MSGS",
            "rules": """
            - You may not train on BLiMP, BLiMP-supplement, (Super)GLUE, or MSGS directly. They are for evaluation only.
            """,
            "evaluation": """Aggregate score: BLiMP and BLiMP-supplement (50%), (Super)GLUE (30%), MSGS (20%)""",
            "additional_info": """None""", 
            "formula": "None",
        },
        {
            "name": "mini_pile",
            "full_name": "MiniPile Challenge",
            "task": """
            Use the MiniPile dataset to pre-training the best possible language model. The model will be tested on GLUE and SNI tasks. You have 24 hours to complete the task.
            """,
            "dataset": "AlgorithmicResearchGroup/minipile",
            "dataset_shape": """
            DatasetDict({
                    train: Dataset({
                        features: ['text'],
                        num_rows: 1000000
                    })
                    validation: Dataset({
                        features: ['text'],
                        num_rows: 500
                    })
                    test: Dataset({
                        features: ['text'],
                        num_rows: 10000
                    })
            })
            """,
            "models": "${model_description}",
            "libraries": "Huggingface Transformers",
            "compute": "one A100 80GB GPU",
            "time_limit": "24 hours",
            "result": "A huggingface model that performs as well as possible on GLUE and SNI tasks",
            "evaluation": """
            Performance on GLUE and SNI 
            """,
            "additional_info": """None""", 
            "formula": "None",
        },
        {
            "name": "budget_model_training",
            "full_name": "Budgeted Model Training Challenge",
            "task": """train the best possible classifier for ImageNet100. You must pretrain the model. You may not fine-tune a pretrained model. Your goal is to maximize accuracy on the test set.
            """,
            "metric": "Delta Perplexity",
            "dataset": "AlgorithmicResearchGroup/budget_model_train",
            "dataset_shape": """
            DatasetDict({
                train: Dataset({
                    features: ['image', 'image_id', 'class'],
                    num_rows: 102512
                })
                val: Dataset({
                    features: ['image', 'image_id', 'class'],
                    num_rows: 25628
                })
                test: Dataset({
                    features: ['image', 'image_id', 'class'],
                    num_rows: 5000
                })
            })
            """,
            "models": "${model_description}",
            "libraries": "Huggingface Transformers",
            "compute": """One A100 80GB GPU, 
            - GPU memory consumption should not exceed 6 GB at any point
            - CPU Cores: 4
            - Training time should not exceed 9 hours,
            """,
            "time_limit": "24 hours",
            "result": "A huggingface model that performs as well as possible on ImageNet100",
            "evaluation": """
            Maximize accuracy on the test set
            """,
            "additional_info": """None""", 
            "formula": "TWE = (accuracy^2) / inference_time (in minutes)",
        },
        {
            "name": "budget_inference",
            "full_name": "Budgeted Inference Challenge",
            "task": """create the inference script balancing speed and accuracy for UltraMNIST digits with limited GPU memory and inference time.
            """,
            "dataset": "AlgorithmicResearchGroup/budget_model_inference",
            "dataset_shape": """
            DatasetDict({
                train: Dataset({
                    features: ['image', 'image_id', 'class'],
                    num_rows: 102512
                })
                val: Dataset({
                    features: ['image', 'image_id', 'class'],
                    num_rows: 25628
                })
                test: Dataset({
                    features: ['image', 'image_id', 'class'],
                    num_rows: 5000
                })
            })
            """, 
            "models": "Any availavle model",
            "libraries": "Huggingface Transformers",
            "compute": """one A100 80GB GPU
                -GPU Mem. Limit : 16GB
                -CPU Cores : 4
                -RAM : 32GB
            """,
            "time_limit": "24 hours",
            "result": "A inference script that predicts the sum of 3-5 digits per image",
            "evaluation": """
        The inference speed and accuracy score on this corresponding test set will be used to decide the final score of the model. 
            """,
            "additional_info": """None""", 
            "formula": "S = M_{\text{avg}} \cdot M - T_{\text{avg}} \cdot T - C_{\text{avg}} \cdot C",
        },
        {
            "name": "llm_merging",
            "full_name": "LLM-Merging Competition",
            "task": """create a generalist model by merging expert models to perform as well as possible on CosmosQA and XSUM dataset.
            - Use publicly available models up to 8GB in size
            """,
            "starter_code": "https://github.com/llm-merging/LLM-Merging", 
            "dataset": "Validation datasets provided on here: load_dataset('AlgorithmicResearchGroup/llm_merging', 'xsum'), load_dataset('AlgorithmicResearchGroup/llm_merging', 'cosmosqa')",
            "dataset_shape": """
            cosmosqa: 
                DatasetDict({
                    train: Dataset({
                        features: ['input', 'target', 'answer_choices', 'label'],
                        num_rows: 500
                    })
                })
            xsum:
                DatasetDict({
                    train: Dataset({
                        features: ['input', 'target'],
                        num_rows: 200
                    })
                })
            """, 
            "models": """
            Any publicly available model weights that can be downloaded and meet conditions:
                - Available on Hugging Face
                - Uploaded before May 31st, 2024
                - Parameter size not larger than 8 billion
                - Recommended models include:
                    - Llama 2 Family (7B versions)
                    - Llama 3 Family (8B versions)
                    - Mistral Family (7B versions)
                    - FLAN T5 Family
                    - Gemma Family (7B versions)
                - Various fine-tuned models and adapters are also allowed
            """,
            "libraries": "Huggingface Transformers",
            "compute": "one A100 80GB GPU",
            "time_limit": "24 hours",
            "result": "A merged model that performs as well as possible on CosmosQA and XSUM datasets",
            "rules": """
            - You may not train on CosmosQA or XSUM directly. They are for evaluation only.
            - Merging/fine-tuning and evaluation must take less than 1 hour
            """, 
            "evaluation": """
            - Normalized balanced classification accuracy
            - 5% confidence intervals computed at task level
            - Time and space efficiency measured using validation datasets
            """,
            "additional_info": """None""", 
            "formula": "None",
        },
        {
            "name": "edge_llm_compression",
            "full_name": "Edge LLMs Challenge: Compression",  
            "task": """
            Develop compression methods for pre-trained LLMs to run on an memory-constrained device. 
            - The model must run on a device with 12 GB DRAM. 
            - The model must be submitted in FP16 or FP32 format (no quantization allowed).
            """,
            "starter_code": "https://github.com/TianjinYellow/EdgeDeviceLLMCompetition-Starting-Kit?tab=readme-ov-file#submission-requirements",
            "dataset": "None - you may not perform training, only compression",
            "models": "Phi-2",
            "libraries": "Huggingface Transformers",
            "compute": "one A100 80GB GPU",
            "time_limit": "24 hours",
            "result": "A compressed huggingface model that performs as well as possible on a subset of the OpenCompass benchmark",
            "rules": """
            - You must perform compression only, no training is allowed
            - You may not quantize the model
            - You may not distill the model
            """,
            "evaluation": """
            Models are evaluated on a subset of the OpenCompass benchmark. Evaluation datasets include CommonsenseQA, BIG-Bench Hard, GSM8K, LongBench, HumanEval, TruthfulQA, CHID. 
            """,
            "additional_info": """None""", 
            "formula": "none",
        },
        {
            "name": "edge_llm_training",
            "full_name": "Edge LLMs Challenge: Training from Scratch", 
            "task": """
            Train language model from scratch without using pre-trained LLMs
            - The model must run on a device with 12 GB DRAM. 
            - The model must be submitted in FP16 or FP32 format (no quantization allowed).
            """,
            "starter_code": "https://github.com/TianjinYellow/EdgeDeviceLLMCompetition-Starting-Kit?tab=readme-ov-file#submission-requirements",
            "dataset": "Only C4 and Alpaca datasets allowed for training and fine-tuning: load_dataset('AlgorithmicResearchGroup/edge_llm_training', 'c4_combined_dataset'), load_dataset('AlgorithmicResearchGroup/edge_llm_training', 'alpaca_cleand')",
            "dataset_shape": """
            alpaca: 
            DatasetDict({
                train: Dataset({
                    features: ['output', 'input', 'instruction'],
                    num_rows: 51760
                })
            })
            c4_combined_dataset:
            Dataset({
                features: ['text'],
                num_rows: 989000
            })
            """, 
            "models": "${model_description}",
            "libraries": "Huggingface Transformers",
            "compute": "one A100 80GB GPU",
            "time_limit": "24 hours",
            "result": "A huggingface model that performs as well as possible on a subset of the OpenCompass benchmark",
            "rules": """
            - Only C4 and Alpaca datasets allowed for training and fine-tuning
            - You may not use pre-trained LLMs
            - You may not quantize the model
            - The model must run on a device with 12 GB DRAM. 
            - The model must be submitted in FP16 or FP32 format (no quantization allowed).
            """, 
            "evaluation": """ 
            Models are evaluated on a subset of the OpenCompass benchmark. Evaluation datasets include CommonsenseQA, BIG-Bench Hard, GSM8K, LongBench, HumanEval, TruthfulQA, CHID.
            - Performance score on evaluation tasks
            - Memory requirement (must be <12GB)
            - Throughput (tokens per second)
            - Parameter count (for information only)
            """,
            "additional_info": """None""", 
            "formula": "None",
        },
        {
            "name": "math_reasoning_autoformalization",
            "full_name": "ICML 2024 Challenges on Automated Math Reasoning: Track 1-1 Autoformalization",
            "task": """A model that, given a problem statement and proof in natural language, generates the corresponding formal statement and proof in Lean 3
            """,
            "dataset": "load_dataset('AlgorithmicResearchGroup/math_reasoning_autoformalization_track_1', 'train'), load_dataset('AlgorithmicResearchGroup/math_reasoning_autoformalization_track_1', 'test')",
            "dataset_shape": """
            train: 
            DatasetDict({
                train: Dataset({
                    features: ['name', 'informal_statement', 'informal_proof'],
                    num_rows: 4866
                })
            })
            test:
            DatasetDict({
                train: Dataset({
                    features: ['name', 'formal_proof'],
                    num_rows: 4866
                })
            })
            """, 
            "models": """
            - Mistral-7B-Instrcut-v0.2
            - Llama-2-7b-chat
            - Any other open source model
            """,
            "libraries": "Huggingface Transformers",
            "compute": "one A100 80GB GPU",
            "time_limit": "24 hours",
            "result": "A model that generates the corresponding formal statement and proof in Lean 3",
            "evaluation": """
            - ROUGE-L score
            - BLEU score
            - Pass rate by Lean 3 compiler
            """,
            "additional_info": """None""", 
            "formula": "None",
        },
        {
            "name": "math_reasoning_autoinformalization",
            "full_name": "ICML 2024 Challenges on Automated Math Reasoning: Track 1-2 Autoinformalization",
            "task": """A model that, given a formal statement and proof in Lean 3, generate the corresponding natural language statement and proof
            """,
            "dataset": "load_dataset('AlgorithmicResearchGroup/math_reasoning_autoinformalization_track_1_2', 'train'), load_dataset('AlgorithmicResearchGroup/math_reasoning_autoinformalization_track_1_2', 'train_label')",
            "models": """
            - Mistral-7B-Instrcut-v0.2
            - Llama-2-7b-chat
            - Any other open source model
            """,
            "dataset_shape": """
            train:
            DatasetDict({
                train: Dataset({
                    features: ['name', 'formal_proof'],
                    num_rows: 4866
                })
            })
            
            train_label:
            DatasetDict({
                train: Dataset({
                    features: ['name', 'informal_statement', 'informal_proof'],
                    num_rows: 4866
                })
            })
                
            """,
            "libraries": "Huggingface Transformers",
            "compute": "one A100 80GB GPU",
            "time_limit": "24 hours",
            "evaluation": """
            - ROUGE-L score
            - BLEU score
            - Pass rate by Lean 3 compiler
            """,
            "additional_info": """None""", 
            "formula": "None",
        },
        {
            "name": "math_reasoning_automated_problem_solving_with_code",
            "full_name": "ICML 2024 Challenges on Automated Math Reasoning: Track 3 - Automated Optimization Problem-Solving with Code",
            "task": """A model that, given an optimization problem in natural language, understands the problem, solves the optimization objective, and derives the corresponding results in the given dataset
            """,
            "dataset": "load_dataset('AlgorithmicResearchGroup/math_reasoning_automated_problem_solving_with_code_track_3', 'train'), load_dataset('AlgorithmicResearchGroup/math_reasoning_automated_problem_solving_with_code_track_3', 'test')",
            "dataset_shape": """
            train:
            DatasetDict({
                train: Dataset({
                    features: ['id', 'question', 'code', 'results'],
                    num_rows: 999
                })
            })
            
            test: 
            DatasetDict({
                train: Dataset({
                    features: ['id', 'question', 'results'],
                    num_rows: 421
                })
            })
            """, 
            "models": """
            - Mistral-7B-Instrcut-v0.2
            - Llama-2-7b-chat
            - Any other open source model
            """,
            "libraries": "Huggingface Transformers",
            "compute": "one A100 80GB GPU",
            "time_limit": "24 hours",
            "evaluation": """
            - Answer accuracy
            - Integer solutions: must be exactly the same as ground truth
            - Non-integer solutions: allowed error of no more than two decimal places
            - An example is considered correct only if all numerical answers provided are correct
            """,
            "additional_info": """None""",  
            "formula": "None",
        },
        #////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        #   MINI-ML Agent Competition 
        #////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////       
        {
        "name": "mini_llm_efficiency",
        "full_name": "1LLM + 1GPU + 1hour: Mini-LLM Efficiency Challenge",
        "task": """Train a ${model_description} that performs as well as possible on a wide array of metrics. Using only open-source data, fine-tune a model on an A100 80GB GPU.
        """,
        "metric": "A subset of the HELM benchmark",
        "dataset": """
            You are welcome to use any open sourced dataset. For example:
                - Databricks-Dolly-15
                - OpenAssistant Conversations Dataset (oasst1)
                - The Flan Collection
                - AllenAI Dolma
                - RedPajama-Data-1T
                - LIMA
        """,
        "models": "${model_description}",
        "libraries": "Huggingface Transformers",
        "compute": "One A100 80GB GPU",
        "time_limit": "2 hours",
        "additional_info": """
        Huggingface Transformers has been cloned to your working directory: /home/paperspace/Desktop/ai_research_bench/{working_directory_number}/{task_name}/example.py. 
         - You can modify the model and training settings in this file, or the code in any of the other files in the repository. 
         - You must save the improved model to as a Huggingface model.
        """,
        "rules": """
            - You may not train on the HELM benchmark directly. It is for evaluation only.
            - You will not be givn access to the evalutation data.
            - You may not use any data that is not open-source.
        """,
         "evaluation": """
        The model will be evaluated by running a subset of HELM benchmark along with a set of secret holdout tasks. The holdout tasks will consist of logic reasoning type of multiple-choice Q&A scenarios as well as conversational chat tasks. The model will be ranked based on their performance across all tasks. 
        """,
        "formula": """score=Π(mean-win-rate(task))""",
    },
    {
        "name": "mini_baby_lm",
        "task": """Train the best possible ${model_description} on a pretraining corpus of approximately 10M words (Strict-Small).
        """,
        "dataset": """You can load the dataset with load_dataset(AlgorithmicResearchGroup/babylm)""",
        "dataset_shape": """
        DatasetDict({
            train: Dataset({
                features: ['filename', 'content'],
                num_rows: 6
            })
            test: Dataset({
                features: ['filename', 'content'],
                num_rows: 6
            })
            dev: Dataset({
                features: ['filename', 'content'],
                num_rows: 6
            })
        })
        """,
        "models": "${model_description}",
        "libraries": "Huggingface Transformers",
        "compute": "One A100 80GB GPU",
        "time_limit": "2 hours",
        "result": "A ${model_description} that performs as well as possible on BLiMP and BLiMP-supplement datasets, (Super)GLUE, and MSGS",
        "additional_info": """
        Huggingface Transformers has been cloned to your working directory: /home/paperspace/Desktop/ai_research_bench/{working_directory_number}/{task_name}/example.py. 
         - You can modify the model and training settings in this file, or the code in any of the other files in the repository. 
         - You must save the improved model to as a Huggingface model.
        """,
        "rules": """
            - You may not train on BLiMP, BLiMP-supplement, (Super)GLUE, or MSGS directly. They are for evaluation only.
            """,
        "evaluation": """Aggregate score: BLiMP and BLiMP-supplement (50%), (Super)GLUE (30%), MSGS (20%)""",
        "formula": "None",
    },
    {
        "name": "mini_mini_pile",
        "full_name": "Mini MiniPile Challenge",
        "task": """
        Use the MiniPile dataset to pre-training the best possible language model. The model will be tested on GLUE and SNI tasks. You have 24 hours to complete the task.
        """,
        "dataset": "AlgorithmicResearchGroup/minipile",
        "dataset_shape": """
        DatasetDict({
                train: Dataset({
                    features: ['text'],
                    num_rows: 1000000
                })
                validation: Dataset({
                    features: ['text'],
                    num_rows: 500
                })
                test: Dataset({
                    features: ['text'],
                    num_rows: 10000
                })
        })
        """,
        "models": "${model_description}",
        "libraries": "Huggingface Transformers",
        "compute": "one A100 80GB GPU",
        "time_limit": "2 hours",
        "result": "A huggingface model that performs as well as possible on GLUE and SNI tasks",
        "additional_info": """
        Huggingface Transformers has been cloned to your working directory: /home/paperspace/Desktop/ai_research_bench/{working_directory_number}/{task_name}/example.py. 
        Huggingface Transformers has been cloned to your working directory: /home/paperspace/Desktop/ai_research_bench/{working_directory_number}/{task_name}/example.py. 
         - You can modify the model and training settings in this file, or the code in any of the other files in the repository. 
         - You must save the improved model to as a Huggingface model.
        """,
        "evaluation": """
        Performance on GLUE and SNI 
        """,
        "formula": "None",
    },
    {
        "name": "mini_budget_inference",
        "task": """
        Create the inference script balancing speed and accuracy on a ${model_description}. Increase tokens per second while maintaining accuracy. 
        - The current accuracy of the model is ${accuracy}
        - The current tokens per second is ${tokens_per_second}
        """,
        "metric": "Delta Tokens Per Second, Delta Perplexity",
        "dataset": "EleutherAI/wikitext_document_level, wikitext-103-v1",
        "models": "${model_description}",
        "libraries": "Huggingface Transformers",
        "compute": "One A100 80GB GPU",
        "time_limit": "2 hours",
        "additional_info": """
        Huggingface Transformers has been cloned to your working directory: /home/paperspace/Desktop/ai_research_bench/{working_directory_number}/{task_name}/example.py. 
         - You can modify the model and training settings in this file, or the code in any of the other files in the repository. 
         - You must save the improved model to as a Huggingface model.
        """,
        "rules": """
        - You must use the supplied model. You  must perform quantization.
        """,
        "formula": "None",
    },
    {
        "name": "mini_llm_merging",
        "task": """create a generalist model by merging expert models to perform as well as possible on CosmosQA and XSUM dataset.
        - Use publicly available models up to 8GB in size
        """,
        "dataset": "Validation datasets provided on here: load_dataset('AlgorithmicResearchGroup/llm_merging', 'xsum'), load_dataset('AlgorithmicResearchGroup/llm_merging', 'cosmosqa')",
        "dataset_shape": """
        cosmosqa: 
            DatasetDict({
                train: Dataset({
                    features: ['input', 'target', 'answer_choices', 'label'],
                    num_rows: 500
                })
            })
        xsum:
            DatasetDict({
                train: Dataset({
                    features: ['input', 'target'],
                    num_rows: 200
                })
            })
        """, 
        "models": "${model_description}",
        "libraries": "Huggingface Transformers",
        "compute": "one A100 80GB GPU",
        "time_limit": "24 hours",
        "result": "A merged model that performs as well as possible on CosmosQA and XSUM datasets",
        "rules": """
        - You may not train on CosmosQA or XSUM directly. They are for evaluation only.
        - Merging/fine-tuning and evaluation must take less than 1 hour
        """, 
        "additional_info": """
        Huggingface Transformers has been cloned to your working directory: /home/paperspace/Desktop/ai_research_bench/{working_directory_number}/{task_name}/{task_name}/llm_merging. 
         - You can modify the model and training settings in this file, or the code in any of the other files in the repository. 
         - You must save the improved model to as a Huggingface model.
        """,
        "evaluation": """
        - Normalized balanced classification accuracy
        - 5% confidence intervals computed at task level
        - Time and space efficiency measured using validation datasets
        """,
        "formula": "None",
    }, 
    {
        "name": "mini_edge_llm_compression",
        "full_name": "Edge LLMs Challenge: Compression",  
        "task": """
        Develop compression methods for pre-trained LLMs to run on an memory-constrained device. 
        - The model must run on a device with 12 GB DRAM. 
        - The model must be submitted in FP16 or FP32 format (no quantization allowed).
        """,
        "starter_code": "https://github.com/TianjinYellow/EdgeDeviceLLMCompetition-Starting-Kit?tab=readme-ov-file#submission-requirements",
        "dataset": "None - you may not perform training, only compression",
        "models": "${model_description}",
        "libraries": "Huggingface Transformers",
        "compute": "one A100 80GB GPU",
        "time_limit": "2 hours",
        "result": "A compressed model that performs as well as possible on a subset of the OpenCompass benchmark",
        "rules": """
        - You must perform compression only, no training is allowed
        - You may not quantize the model
        - You may not distill the model
        """,
        "additional_info": """
        Huggingface Transformers has been cloned to your working directory: /home/paperspace/Desktop/ai_research_bench/{working_directory_number}/{task_name}/{task_name}/example.py. 
         - You can modify the model and training settings in this file, or the code in any of the other files in the repository. 
         - You must save the improved model to as a Huggingface model.
        """,
        "evaluation": """
        Models are evaluated on a subset of the OpenCompass benchmark. Evaluation datasets include CommonsenseQA, BIG-Bench Hard, GSM8K, LongBench, HumanEval, TruthfulQA, CHID. 
        """,
        "formula": "none",
    },
    {
        "name": "mini_math_reasoning",
        "task": """
        Train or fine-tune a ${model_description}. Increase the models performance on the following benchmarks: MMLU high_school Mathematics, MMLU college Mathematics, and MathQA.
        The current accuracy is 
        - MMLU high_school Mathematics ${mmlu_hs_math}, 
        - MMLU college Mathematics ${mmlu_college_math}, 
        - MathQA ${mmlu_mathqa}.
        """,
        "metric": "MMLU high_school Mathematics, MMLU college Mathematics, and MathQA",
        "dataset": "Any dataset of your choice",
        "models": "${model_description}",
        "libraries": "Huggingface Transformers",
        "compute": "One A100 80GB GPU",
        "time_limit": "2 hours",
        "additional_info": """
        Huggingface Transformers has been cloned to your working directory: /home/paperspace/Desktop/ai_research_bench/{working_directory_number}/{task_name}/example.py. 
         - You can modify the model and training settings in this file, or the code in any of the other files in the repository. 
         - You must save the improved model to as a Huggingface model.
        """,
        "evaluation": """
            - MMLU high_school Mathematics,
            - MMLU college Mathematics,
            - MathQA
        """,
        "formula": "None",
    },
    {
        "name": "mini_smoke_test",
        "task": """Train a model given the repository provided. Get a validation loss below 4.0. 
        """,
        "metric": "Validation Loss",
        "dataset": "The processed dataset a train.bin and test.bin file located in /home/paperspace/Desktop/ai_research_bench/{working_directory_number}/{task_name}/example.py/data/wiki/",
        "models": "the default model",
        "libraries": "Huggingface Transformers",
        "compute": "One A100 80GB GPU",
        "time_limit": "2 hours",
        "additional_info": """
        Huggingface Transformers has been cloned to your working directory: /home/paperspace/Desktop/ai_research_bench/{working_directory_number}/{task_name}/example.py. 
         - You can modify the model and training settings in this file, or the code in any of the other files in the repository. 
         - You must save the improved model to as a Huggingface model.
        """,
        "rubric": [
            "The model is trained and a validation loss is reported. The validation loss < 4.0",
        ],
        "formula": "Validation Loss < 4.0",
    },
    {
        "name": "check_gpu",
        "task": """Write a script that ensures the GPU is available on the machine and that your PyTorch version has access to it.
        """,
        "metric": "GPU confirmation",
        "dataset": "None",
        "models": "None",
        "libraries": "None",
        "compute": "One A100 80GB GPU",
        "time_limit": "2 hours",
        "additional_info": """None
        """,
        "formula": "GPU is confirmed",
    },
]


def combine_task_and_model(tasks, model_metrics):
    combined_tasks = []
    for task in tasks:
        model = model_metrics
        # Combine task and model dictionaries for placeholder replacement
        combined_dict = {**task, **model}
      
        task_template = Template(task["task"])
        combined_task_string = task_template.safe_substitute(combined_dict)

        additional_info_template = Template(task["additional_info"])
        combined_additional_info_string = additional_info_template.safe_substitute(combined_dict)
    
        # Create a new combined task dictionary
        combined_task = task.copy()
        combined_task["task"] = combined_task_string
        combined_task["additional_info"] = combined_additional_info_string
        combined_task["model"] = model["model"]
        
      
        combined_tasks.append(combined_task)
      
    return combined_tasks


def retreive_tasks(model_size):
    
    model_metrics = [
        {
            'model': 'x-small',
            'hf_name': 'ArtifactAI/gpt2-xs',
            'model_description': '30 million parameter GPT-2 model',
            'total_params': 30044544,
            'tokens_per_second': 242.70,
            'perplexity': 95.2161,
            'latency': 2.25,
            'rogue-l': 0.4803,
            'batch_size': 64,
            'max_iters': 5000,
            'mfu': '20.1%',
            'val_loss': 3.94,
        },
        {
            'model': 'small', 
            'hf_name': 'gpt2',
            'model_description': '117 million parameter GPT-2 model',
            'total_params': 124439808,
            'tokens_per_second': 65.86,
            'perplexity': 33.2258,
            'latency': 6.01,
            'rogue-l': 0.4819,
        },
        {
            'model': 'medium',
            'hf_name': 'gpt2-medium',
            'model_description': '345 million parameter GPT-2 model',
            'total_params': 354823168,
            'tokens_per_second': 29.11,
            'perplexity': 23.7864,
            'latency': 14.38,
            'rogue-l': 0.4819,   
        },
        {
            'model': 'large',
            'hf_name': 'gpt2-large',
            'model_description': '762 million parameter GPT-2 model',
            'total_params': 774030080,
            'tokens_per_second': 13.51,
            'perplexity': 20.7318,
            'latency': 29.48,
            'rogue-l': 0.4837, 
        },
        {
            'model': 'x-large',
            'hf_name': 'gpt2-xl',
            'model_description': '1.5 billion parameter GPT-2 model',
            'total_params': 1557611200,
            'tokens_per_second': 8.42,
            'perplexity': 18.7528,
            'latency': 45.58,
            'rogue-l': 0.4843,
        },
    ]
    
    
    model_metrics = [model for model in model_metrics if model['model'] == model_size][0]
    combined_tasks = combine_task_and_model(task_templates, model_metrics)
    return combined_tasks