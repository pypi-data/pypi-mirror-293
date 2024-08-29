# XPRIZE 2024 - Few-shot classification of Brazil nut trees in satellite imagery

The XPRIZE is a global competition designed to inspire and incentivize groundbreaking innovations that address some of the world's most pressing challenges. Established in 1995 by Peter Diamandis, the first XPRIZE was the Ansari XPRIZE, which awarded $10 million to the first team to build a private spacecraft capable of carrying passengers to the edge of space twice within two weeks. Since then, XPRIZE competitions have expanded to various fields, including health, energy, education, and the environment, offering substantial cash prizes to teams that achieve specific, ambitious goals. The idea is to catalyze technological advancements and solutions that might not emerge as quickly—or at all—without the motivation of a high-stakes competition.

This project explores the use of self-supervised representation learning to enhance the few-shot classification of Brazil nut trees in satellite imagery. By applying self-supervised techniques, the model learns robust features from large volumes of _unlabeled_ satellite data, which can then be adapted with minimal labeled samples. This methodology addresses the common challenge of limited labeled data in remote sensing, aiming to improve the detection and classification accuracy of Brazil nut trees. The project’s outcomes could significantly contribute to more effective monitoring and conservation practices in the Amazon rainforest.

## Setup and Installation

To get started, follow the steps below to set up your environment.

### 1. Install `rye`

If you haven't installed [`rye`](https://rye.astral.sh/) yet, you can do so by following these instructions:

#### For macOS and Linux:

Open your terminal and run the following command:

```bash
curl -sSf https://rye.astral.sh/get | bash
```

### 2. Install Dependencies

Once rye is installed, sync the project dependencies by running:

```bash
rye sync
```

## Running the Application

To run the application, ensure you have saved the pretrained encoder in ./models/encoder.onnx and placed your data in the ./data/ directory.

### Running the Streamlit App

Start the application with the following command:

```bash
rye run dev
```

This will start the Streamlit app and open it in your default browser.
