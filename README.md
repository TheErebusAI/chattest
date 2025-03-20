# chattest

chattest is a semantic testing framework designed to facilitate collaboration between subject-matter experts (SMEs) and prompt engineers.

## architecture

at the core of this framework are the following concepts:
* prompts
* models
* outputs
* tests
* run volume
* success thresholds

a prompt can be stored in the project, and then tests can be added for that prompt's output. when running tests, we inference a configurable list of models a configurable number of times. the results are then tested using a single, configurable model, resulting in a PASS or FAIL for each test. then, the PASS/FAIL results are shown to the user for each test.

### prompts

stored in JSON files in this project, these entities must have testing configurations.

#### data model:

```json
{
  "key": "prompt name or id",
  "prompt": "prompt text",
  "models": [
    "gpt-4",
    "deepseek-r1"
  ],
  "tests": [
    "the output should contain this text",
    "the output should not contain this text",
    "does the output contain this information?"
  ],
  "runVolume": 20,
  "testModel": "claude-3.7-haiku",
  "successThreshold": 0.8
}
```

#### run volumes and success thresholds

run volume refers to the number of runs that should be performed when testing. a run volume of 20 will generate 20 outputs against each model specified.

success threshold refers to the percentage of tests that should pass. each test is run against the run volume specified, and the percentage of successful runs against that test is calculated. if it satisfies the success threshold, the test is marked as a PASS. the default success threshold is 0%.

### models

models are defined in the project, and are referenced by name. they are used via HTTP(S) requests.

#### data model:

```json
{
  "key": "model name or id",
  "url": "https://api.openai.com/v1/completions",
  "apiKey": "my-api-key",
  "apiKeyHeader": "Authorization"
}
```

apiKey is optional; if not specified, no API key will be included in the request.

### outputs

outputs should be displayed upon test run, but are not stored.

### test results

test results are sent to stdout.
