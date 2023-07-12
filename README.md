# data-collector-with-no-pii
Delivery: `02-flask-app`, a web UI that collects the user input, detect and redact PII, and save it to server

## 01-aws-comprehend-builtin

Detect PII with AWS Comprehend.

See the docs:

- https://docs.aws.amazon.com/comprehend/latest/dg/how-pii.html

- https://docs.aws.amazon.com/code-library/latest/ug/python_3_comprehend_code_examples.html

### Usage

1. Get AWS profile (`~/.aws/credentials`)

2. Once the credential is set up, we can use boto3 client:

```
session = boto3.Session(profile_name='saml')
comp_client = session.client('comprehend')
comp_detect = ComprehendDetect(comp_client)
```

See https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html#shared-credentials-file 

3. Use virtual env in jupyter lab

```
python -m ipykernel install --user --name=.venv
```

Refresh lab page. The kernel `.venv` will be available.

4. Use evaluation.py

Install dependency: 

```
python -m spacy download en_core_web_md
```