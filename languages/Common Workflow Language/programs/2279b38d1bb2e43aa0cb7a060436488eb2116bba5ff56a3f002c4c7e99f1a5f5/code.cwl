cwlVersion: v1.0
class: Workflow

inputs:
  message: string

outputs:
  response: File

steps:
  step1:
    run: hello.cwl
    in:
      message: message
    out:
      [response]