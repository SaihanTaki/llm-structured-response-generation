## LLM Structured Response Generation

**Run any of the command below**
```bash
python langchain_structured_output.py | jq
```
```bash
python opeani_structured_output.py | jq
```
```bash
python gemini_structured_output.py | jq
```
**Output**
```bash
{
  "chapters": [
    {
      "SI": 1,
      "title": "Plants",
      "start": 6,
      "end": 16
    },
    {
      "SI": 2,
      "title": "Food and digestion",
      "start": 18,
      "end": 30
    },
    {
      "SI": 3,
      "title": "The circulatory system",
      "start": 32,
      "end": 40
    },
    {
      "SI": 4,
      "title": "Respiration",
      "start": 42,
      "end": 52
    },
    {
      "SI": 5,
      "title": "Reproduction and development",
      "start": 54,
      "end": 66
    },
    {
      "SI": 6,
      "title": "States of matter",
      "start": 68,
      "end": 78
    },
    {
      "SI": 7,
      "title": "Elements and compounds",
      "start": 80,
      "end": 90
    },
    {
      "SI": 8,
      "title": "Mixtures",
      "start": 92,
      "end": 106
    },
    {
      "SI": 9,
      "title": "Material changes",
      "start": 108,
      "end": 122
    },
    {
      "SI": 10,
      "title": "Measuring motion",
      "start": 124,
      "end": 134
    },
    {
      "SI": 11,
      "title": "Sound",
      "start": 136,
      "end": 146
    },
    {
      "SI": 12,
      "title": "Light",
      "start": 148,
      "end": 160
    },
    {
      "SI": 13,
      "title": "Magnetism",
      "start": 162,
      "end": 174
    }
  ]
}
```

### Important Links
1. [Sturcutred Output using Langchain and LLM APIs](https://python.langchain.com/docs/how_to/structured_output/)

2. [Sturcutred Output using Openai API](https://platform.openai.com/docs/guides/structured-outputs)

3. [Sturcutred Output using Gemini API](https://ai.google.dev/gemini-api/docs/structured-output?lang=python)