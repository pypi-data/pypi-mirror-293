from elasticsearch import Elasticsearch

ES_CLOUD_ID = "lm-datasets:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJDk1N2U5ODIwZDUxNTQ0YWViMjk0MmQwNzI1NjE0OTQ2JDhkN2M0OWMyZDEzMTRiNmM4NDNhNGEwN2U4NDE5NjRl"
ES_API_KEY = "R0ZDSjNvOEJ1MEw4LVVWVjZSZ0I6Mi1HM1F6SktSWTJTZk9Bby02RDJiZw=="
ES_INDEX_NAME = "c4"


def es_init(timeout: int = 30) -> Elasticsearch:

   """
   :param config: Path to the config yaml file, containing `cloud_id` and `api_key` fields.
   :return: Authenticated ElasticSearch client.
   """
   cloud_id = ES_CLOUD_ID
   api_key = ES_API_KEY

   es = Elasticsearch(
       cloud_id=cloud_id,
       api_key=api_key,
       retry_on_timeout=True,
       http_compress=True,
       request_timeout=timeout,

   )

   return es


# def main():
if __name__ == "__main__": 
   es = es_init()
   # Regex query
   query = {
       "query": {
           "regexp": {
               "text": {
                   "value": "there are m.*y",
                   "flags": "ALL",
                    "case_insensitive": True,
                    "max_determinized_states": 10000,
                    
               }
           }
       }
   }

   # Execute the query
   response = es.search(index=ES_INDEX_NAME, body=query, size=10, request_timeout=30)
   print("response =>")
   print("\t", response)

   # Print results
   for hit in response['hits']['hits']:
       print(hit["_source"])

   breakpoint()




# if __name__ == "__main__": 
#     main()