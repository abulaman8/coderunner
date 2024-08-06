
    FROM python
    # FROM python:3.8-slim

    WORKDIR /app

    RUN apt-get update && apt-get install -y     wget     unzip     && rm -rf /var/lib/apt/lists/*

    # Download and extract the zip file
    ARG ZIP_URL=http://192.168.1.31:3000/media/qn_src/11d31c43456f396d1e340a7dc4069a175562e73c927f295c3bf53795f4a3aca2.zip
    RUN wget -O temp.zip $ZIP_URL && unzip temp.zip && rm temp.zip

    # Download the additional Python file
    ARG PYTHON_FILE_URL=http://192.168.1.31:3000/media/qn_test/11d31c43456f396d1e340a7dc4069a175562e73c927f295c3bf53795f4a3aca2.py
    RUN wget -O script.py $PYTHON_FILE_URL

    # If requirements.txt exists, install the requirements
    RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
    COPY . /app

    CMD ["tail", "-f", "/dev/null"]

    