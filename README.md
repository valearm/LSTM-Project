## Installation

You will need to have Python 3.x and the following libraries installed:
- numpy
- tensorflow
- keras
- art

You can install these libraries using pip by running the following command:

'''pip install requirements.txt'''

## Usage

You will need to have a data file containing past lottery results. This file should be in a comma-separated format, with each row representing a single draw and the numbers in ascending order, rows are in new line without comma. Dont use white spaces. Last row number must have nothing after last number.

Once you have the data file, you can run the `main.py` script to train the model and generate predictions. 
To scrape data from the web an example is given in the "webscraping.py" file which does a webscraping from a Italian lottery game called "Vinci Casa".
