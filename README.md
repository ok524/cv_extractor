# CV Extractor

Input: Resume (Image, PDF, docx, LinkedIn profile)

Output: Database of structured Resume

Process:
- File to plaintext
- Plaintext process
- Terms extraction
- Write to database
- Display and query data

## Architecture

- Frontend: React
- Backend: Python 3.6+ (Fast API)
    - [Algorithm](https://github.com/KEEP-EDU-HK/keep_clap/tree/master/SoftSkillExtraction)
- Database: PostgreSQL (JSONB)

## Folder structure

- app (API)

- web (Frontend)


## Development

```
cd cv_extractor/app
source nenv/bin/activate
```

1. API app
```
cd cv_extractor/app
uvicorn main:app --reload
```

2. RabbitMQ + Database
```
cd cv_extractor
docker-compose --env-file ./database/.env up
```

3. Worker for write db
```
cd cv_extractor/app
python3 dbworker/main.py
```

4. Worker for extract info
```
export PYTHONIOENCODING=utf8
export TIKA_SERVER_JAR="file:///omar_prj/app/202108_tool_convert_plaintext/vgdocx/tika-server.jar"
cd cv_extractor/app
python3 cvworker/main.py
```

5. Web
```
cd cv_extractor/web
yarn start
```

### Architecture diagram

- [CV extractor - Architecture](https://app.diagrams.net/#G1GVSMvMNJHijZdG54S2mhAIJn4IxNdout)

## Test app

```
python3 test/main.py
```

### Individual development
```
python3 makeplaintext/main.py
```
Output text folder: app/output_files


```
python3 extract/main.py
```

## Reference

### Python

- [Unittest in Python](https://www.codingame.com/playgrounds/10614/python-unit-test-with-unittest)

### Extraction

- [Top 1,000 Baby Names of 2020](https://www.verywellfamily.com/top-1000-baby-girl-names-2757832)
- [Email extraction](https://www.thepythoncode.com/article/extracting-email-addresses-from-web-pages-using-python)
- [First name](https://github.com/philipperemy/name-dataset)

### React

- [Update context from children](https://stackoverflow.com/questions/41030361/how-to-update-react-context-from-inside-a-child-component)

### Publish/Subscribe

- [RabbitMQ tutorial](https://aio-pika.readthedocs.io/en/latest/rabbitmq-tutorial/5-topics.html)

### Tools to entity

- [Brat](https://brat.nlplab.org/manual.html)
