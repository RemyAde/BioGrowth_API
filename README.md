# BioGrowth_API

BioGrowth_API is a Python-based API designed to help small-scale and middle-scale farmers access scientifically engineered agricultural products. The project provides tools for data processing, visualization, and statistical analysis to enhance agricultural productivity.

## Table of Contents
- Description
- Installation
- Usage
- Contributing
- License
- Contact

## Description
BioGrowth_API is created to assist farmers by providing access to scientifically engineered agricultural products. The API offers various functionalities for managing and analyzing biological growth data, making it easier for farmers to make informed decisions.

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/RemyAde/BioGrowth_API.git
    ```
2. Navigate to the project directory:
    ```sh
    cd BioGrowth_API
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
1. Navigate to the app directory:
    ```sh
    cd app
    ```
2. Add the following environment variables to the `.env` file:
    ```env
    algorithm=<your_algorithm>
    email=<your_email>
    password=<your_password>
    DEV_DATABASE_URL=<your_database_url>
    secret_key=<your_secret_key>
    ```
3. Start the API:
    ```sh
    python main.py
    ```
4. Access the API at `http://localhost:8000`.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## License
This project is licensed under the MIT License.

## Contact
For any inquiries or issues, please contact the repository owner.
