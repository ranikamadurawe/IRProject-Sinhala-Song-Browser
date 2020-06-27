# IRProject-Sinhala-Song-Browser
This repo contains all code required for the implementation of a Sinhala Song Lyrics Engine for module CS4642
## Project Requirements
* Angular 8.3.23
* Python 3.6.9
* ElasticSearch 7.7.0

Additionally preimplemented tokenizers and stemmers from the following projects have been integrated
* Singling Tokenizer https://github.com/ysenarath/sinling
* Sinhala Stemmer https://github.com/shilpasayura/sinhala-nltk/tree/master/sinhala-stemmer

The following Utility tools have also been used
* Scrapy ElasticSearch pipeline https://github.com/jayzeng/scrapy-elasticsearch
* Elasticdump Tool https://www.npmjs.com/package/elasticdump

## Project Structure
### 1. angularSE
Contains the code for the Angular 8 based Search Engine Implementation. Issue the following command in this directory to run the Search Engine on port 4200
```
ng serve
```
### 2. esIndexBackup
Contains the backup files for the used elastic search analyzer, mapping and data use. Utilize the following commands to import the json file to an elasticSearch Index
```
elasticdump   --input=final_elasticsearch_<type>.json --output=http://<your-es-instance>/<your-index>   --type=<type>
```
### 3. lyricsScraper
Contains the Scrapy web crawler which was used to scrape web pages for music data.
    ```
    scrapy crawl sinhalasongbook -o <optional_data_file>
    ```
The scraoer automatcally sends data the specified elasticsearch index specified in the settings.py file
  ```
ELASTICSEARCH_SERVERS = ['localhost']
ELASTICSEARCH_INDEX = '<your-index>'
ELASTICSEARCH_INDEX_DATE_FORMAT = '%Y'
ELASTICSEARCH_TYPE = 'items'
ELASTICSEARCH_UNIQ_KEY = '<your-item-type>'
 ```

### 4. searchEngine
Contains the Flask server which is used to implement the backend server of the Search Engine. Use the following code to run the flask server on port 5000
```
python server.py
```
