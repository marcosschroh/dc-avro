## 0.12.0 (2025-01-28)

### Feat

- **diff**: context and unified type diff added

## 0.11.0 (2025-01-27)

### Feat

- **diff**: diff improved. Parameter --num-lines introduced when --only-deltas is set to True. Diff styles improved

## 0.10.0 (2025-01-20)

### Feat

- diff schema improved

## 0.9.3 (2024-10-23)

### Fix

- python38 support dropped

## 0.9.2 (2024-10-23)

### Fix

- make more flexible dataclasses-avroschema dependency

## 0.9.1 (2024-10-18)

### Fix

- updated to latest dataclases-avroschemas

## 0.9.0 (2024-03-11)

### BREAKING CHANGE

- Now we use --model-type to know the type of Model that has to be generated: https://marcosschroh.github.io/dataclasses-avroschema/model_generator/#usage

### Refactor

- --base-class replaced by --model-type when generating models from schemas

## 0.8.0 (2024-01-02)

### Feat

- add generate fake data command

## 0.7.1 (2023-10-26)

### Fix

- Rename repos referrences in docs

## 0.7.0 (2023-10-25)

### Feat

- Implement lint command and pre-commit mode

## 0.6.5 (2023-05-29)

### Fix

- drop python37 support

## 0.6.4 (2023-03-22)

### Fix

- dependencies updated

## 0.6.3 (2023-03-06)

### Fix

- set markup to False when render python models

## 0.6.2 (2023-03-02)

### Fix

- dataclasses-avroschema should not have a specific version pinned

## 0.6.1 (2023-02-25)

### Feat

- schema diff command added

### Fix

- project version due commitizen
- dependencies updated

## 0.5.0 (2023-02-03)

### Feat

- deserialization command added

## 0.4.0 (2023-02-02)

### Feat

- serialization command added

## 0.3.0 (2023-02-01)

### Feat

- add command to gererate python models from schemas

## 0.2.0 (2023-02-01)

### Feat

- validate command added

### Fix

- unittests aded. ruff config added
