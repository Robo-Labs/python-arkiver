from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import pandas as pd
import json
import sys
import os 

def getFields(selector):
  queryStr = introspection_query = """
  query IntrospectionQuery {
    __schema {
      queryType { name }
      mutationType { name }
      subscriptionType { name }
      types {
        ...FullType
      }
      directives {
        name
        description
        locations
        args {
          ...InputValue
        }
      }
    }
  }
  fragment FullType on __Type {
    kind
    name
    description
    fields(includeDeprecated: true) {
      name
      description
      args {
        ...InputValue
      }
      type {
        ...TypeRef
      }
      isDeprecated
      deprecationReason
    }
    inputFields {
      ...InputValue
    }
    interfaces {
      ...TypeRef
    }
    enumValues(includeDeprecated: true) {
      name
      description
      isDeprecated
      deprecationReason
    }
    possibleTypes {
      ...TypeRef
    }
  }
  fragment InputValue on __InputValue {
    name
    description
    type { ...TypeRef }
    defaultValue
  }
  fragment TypeRef on __Type {
    kind
    name
    ofType {
      kind
      name
      ofType {
        kind
        name
        ofType {
          kind
          name
          ofType {
            kind
            name
            ofType {
              kind
              name
              ofType {
                kind
                name
                ofType {
                  kind
                  name
                }
              }
            }
          }
        }
      }
    }
  }
  """
  query = gql(queryStr)
  result = client.execute(query)
  fields = []
  selectorPlural = selector + "s"
  for obj in result['__schema']['types']:
    if obj['name'] == selector:
      for field in obj['fields']:
        fields.append(field['name'])
  return fields

def createQuery(selector, fields):
  queryStr = '''
  query MyQuery($limit: Int!, $skip: Int!) {{
    {selector}(limit: $limit, skip: $skip) {{'''.format(selector=selector)
  for field in fields:
    queryStr +=  '\n    ' + field
  queryStr += "\n }\n}"
  return queryStr

def execPageQuery(queryStr):
  query = gql(queryStr)
  match len(sys.argv):
    case 5:
        params = {"limit": int(sys.argv[4]), "skip": 0}
    case 6:
        params = {"limit": int(sys.argv[4]), "skip": int(sys.argv[5])}
    case default:
        params = {"limit": 1000, "skip": 0}

  result = client.execute(query, variable_values=params)
  endResult = []
  while(len(result[selectorPlural]) > 0):
    endResult.append(result[selectorPlural])
    params["skip"] = params["skip"]+params["limit"]
    result = client.execute(query, variable_values=params)
  return endResult

if len(sys.argv) > 3:
    transport = AIOHTTPTransport(url=sys.argv[3])
else:
    transport = AIOHTTPTransport(url="http://0.0.0.0:4000/graphql")

client = Client(transport=transport, fetch_schema_from_transport=True)

selector = sys.argv[1]
selectorPlural = selector + "s"
fields = getFields(selector)
queryStr = createQuery(selectorPlural, fields)
endResult = execPageQuery(queryStr)

dfList = []
for itemBatch in endResult:
    df = pd.DataFrame(itemBatch)
    dfList.append(df)
df = pd.concat(dfList)
dir_path = os.path.dirname(os.path.realpath(__file__))
pathOutput = dir_path + '/' + sys.argv[2]
df.to_csv (pathOutput, index = None)
    

