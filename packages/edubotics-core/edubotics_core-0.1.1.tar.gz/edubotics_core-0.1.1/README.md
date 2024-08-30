---
title: AI Class Tutor -- Dev
description: An LLM based AI class tutor with RAG on DL4DS course
emoji: 🐶
colorFrom: red
colorTo: green
sdk: docker
app_port: 7860
---
# DL4DS Tutor 🏃

![Build Status](https://github.com/edubotics-ai/edubot-core/actions/workflows/push_to_hf_space.yml/badge.svg)
![License](https://img.shields.io/github/license/edubotics-ai/edubot-core)
![GitHub stars](https://img.shields.io/github/stars/edubotics-ai/edubot-core)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)


Check out the configuration reference at [Hugging Face Spaces Config Reference](https://huggingface.co/docs/hub/spaces-config-reference).

You can find a "production" implementation of the Tutor running live at [DL4DS Tutor](https://dl4ds-dl4ds-tutor.hf.space/)  from the
Hugging Face [Space](https://huggingface.co/spaces/dl4ds/dl4ds_tutor). It is pushed automatically from the `main` branch of this repo by this
[Actions Workflow](https://github.com/DL4DS/dl4ds_tutor/blob/main/.github/workflows/push_to_hf_space.yml) upon a push to `main`.

A "development" version of the Tutor is running live at [DL4DS Tutor -- Dev](https://dl4ds-tutor-dev.hf.space/) from this Hugging Face
[Space](https://huggingface.co/spaces/dl4ds/tutor_dev). It is pushed automatically from the `dev_branch` branch of this repo by this
[Actions Workflow](https://github.com/DL4DS/dl4ds_tutor/blob/dev_branch/.github/workflows/push_to_hf_space_prototype.yml) upon a push to `dev_branch`.

## Setup

Please visit [setup](https://dl4ds.github.io/dl4ds_tutor/guide/setup/) for more information on setting up the project.

## Running Locally

1. **Clone the Repository**
   ```bash
   git clone https://github.com/edubotics-ai/edubot-core
   ```

2. Create your app in the apps folder. (An example is the `apps/ai_tutor` app)
   ```
   cd apps
   mkdir your_app
   ```

2. **Put your data under the `apps/your_app/storage/data` directory**
   - Add URLs in the `urls.txt` file.
   - Add other PDF files in the `apps/your_app/storage/data` directory.

3. **To test Data Loading (Optional)**
   ```bash
   cd apps/your_app
   python -m edubotics_core.dataloader.data_loader --links "your_pdf_link" --config_file config/config.yml --project_config_file config/project_config.yml
   ```

4. **Create the Vector Database**
   ```bash
   cd apps/your_app
   python -m edubotics_core.vectorstore.store_manager --config_file config/config.yml --project_config_file config/project_config.yml
   ```

6. **Run the FastAPI App**
   ```bash
   cd apps/your_app
   uvicorn app:app --port 7860 
   ```

## Documentation

Please visit the [docs](https://dl4ds.github.io/dl4ds_tutor/) for more information.


## Docker 

The HuggingFace Space is built using the `Dockerfile` in the repository. To run it locally, use the `Dockerfile.dev` file.

```bash
docker build --tag dev  -f Dockerfile.dev .
docker run -it --rm -p 7860:7860 dev
```

## Contributing

Please create an issue if you have any suggestions or improvements, and start working on it by creating a branch and by making a pull request to the `dev_branch`.

Please visit [contribute](https://dl4ds.github.io/dl4ds_tutor/guide/contribute/) for more information on contributing.

## Future Work

For more information on future work, please visit [roadmap](https://dl4ds.github.io/dl4ds_tutor/guide/readmap/).
