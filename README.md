# wild-rydes-api-auth
[![Serverless](http://public.serverless.com/badges/v3.svg)](http://www.serverless.com)
[![License](https://img.shields.io/badge/License-BSD%202--Clause-orange.svg)](https://opensource.org/licenses/BSD-2-Clause)
<!-- [![Build Status](https://travis-ci.org/ServerlessOpsIO/%%PROJECT%%.svg?branch=master)](https://travis-ci.org/ServerlessOpsIO/%%PROJECT%%) -->
Example AWS API Gateway custom authorizer service.

__DO NOT USE IN A PRODUCTION ENVIRONMENT!!!__

This service is not secure, intended to be secure, or even fully functional. It's only purpose is to demonstrate some concepts or setup scenarios for [ServerlessOps workshops](https://github.com/ServerlessOpsIO/serverlessops-workshops).

## Usage

Key IDs should be API Gateway names and _DateTime_ is the range key which allows for multiple keys for an API Gateway. A typical entry will look as follows.

```
{
  "Id": "user0-wild-rydes-api-auth",
  "Key": "cfbc2139e0298dbe738b941f45175991fbafb208490e5e3c3b5d1d439e65fba0",
  "DateTime": 1546030603,
  "Active": true,
  "TTL": 0
}
```

The Authorizer function will get the API Gateway REST Id from the methodArn and use that to lookup the API Gateway name. The service will then check if _authorizationToken_ is a valid token for that API Gateway.

```
{
    "type": "TOKEN",
    "methodArn": "arn:aws:execute-api:us-east-2:144121712529:hfelovcbek/training-dev/GET/foobar",
    "authorizationToken": "cfbc2139e0298dbe738b941f45175991fbafb208490e5e3c3b5d1d439e65fba0"
}
```

