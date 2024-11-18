<figure>
  <img src="icon.png" alt="description" >
</figure>

## Bio Dataset Manager: easily encode biological sequences into tensors

<hr>

[![Coverage](https://codecov.io/github/tacclab/bio_dataset_manager/coverage.svg?branch=main)](https://codecov.io/gh/tacclab/bio_dataset_manager)
![Unit Tests](https://github.com/tacclab/bio_dataset_manager/actions/workflows/main.yml/badge.svg)<br>
[![Powered by TaccLab](https://img.shields.io/badge/powered%20by-TaccLab-orange.svg?style=flat&colorA=E1523D&colorB=007D8A)](https://tacclab.org)<br> 
[![License](https://img.shields.io/github/license/tacclab/bio_dataset_manager.svg)](https://github.com/tacclab/bio_dataset_manager/blob/main/LICENSE)<br>

## Authors:
<hr>
   - Fabio Bove | fabio.bove.dr@gmail.com<br> 
   - Eugenio Bertolini |  <br> 

## What is it?
<hr>
Bio Data Manager is a Python project designed for managing and processing bio-sequence data, including DNA, proteins, and SMILES strings. This tool facilitates the encoding of these sequences into tensors, which can then be used for AI computations and complex model implementations.


## Project Structure
<hr>

- `bio_data_manager/`: Contains core modules for bioinformatics sequence processing and management.
- `bio_sequences/`: Handles various operations related to biological sequences such as DNA and protein.


## Usage
<hr>

1. Install it as a library
   - Using `CPU`:
      ```bash
      pip install git+ssh://git@github.com/tacclab/bio_data_manager.git@0.0.1
      ```
   - Using `CUDA`:
      ```bash
      pip install git+ssh://git@github.com/tacclab/bio_data_manager.git@0.0.1[cuda] -f https://download.pytorch.org/whl/torch_stable.html
      ```
2. Examples of the code can be found in the `usage_examples.py` file.
```python
    from bio_dataset_manager import BioDataset, BioDataloader
    from bio_sequences import DnaSequence, ProteinSequence, SmilesSequence
```


## Contributing
<hr>
Feel free to submit issues or pull requests if you'd like to contribute to this project.


## License
<hr>

[![License](https://img.shields.io/github/license/tacclab/bio_dataset_manager.svg)](https://github.com/tacclab/bio_dataset_manager/blob/main/LICENSE)<br>


