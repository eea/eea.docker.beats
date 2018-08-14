# eea.docker.beats
ElasticSearch Beats docker custom images



## Metricbeat

Based on docker.elastic.co/beats/metricbeat with a default configuration enabled. Sends monitoring information ( cpu, disk, ram, etc ) to elasticsearch.

### Documentation

https://www.elastic.co/guide/en/beats/metricbeat/current/index.html

### Default configuration

By default, has docker module enabled, so it sends all docker container system performance stats to elasticsearch.

https://github.com/eea/eea.docker.beats/blob/master/metricbeat/metricbeat.yml

### Environment variables

*   CONFIG - to set-up a custom configuration
*   ES_URL - elasticsearch url
*   ES_USER - elasticsearch username for authentification in elasticsearch
*   ES_PASSWORD - elasticsearch user password
*   KIBANA_URL - kibana url, can be provided for dashboard creation, but is not necessary
*   RANCHER_METADATA - "yes" to include information extracted from rancher metadata ( rancher.environment - environment name and beat.name - hostname of the server that has the metricbeat container)
*   TAGS - to add extra information in tag field in elasticsearch
*   ENABLE_METRICS_LOG - false by default, to remove internal metrics from log
*   TZ - Timezone


### Setting up kibana dashboards

Needs to be done only once, from shell command on the container. For a kibana that runs on https ( ES credentials will be used for authentification ) :

    ./metricbeat setup -E setup.kibana.host=kibana.devel2cph.eea.europa.eu:443 -E setup.kibana.protocol="https" --dashboards

## Heartbeat

Based on docker.elastic.co/beats/heartbeat. Can run checks on icmp, tcp or http. 

### Documentation

https://www.elastic.co/guide/en/beats/heartbeat/current/index.html

### Configuration

Needs a configuration file or variable to run


### Environment variables

*   CONFIG - to set-up a configuration
*   ES_URL - elasticsearch url
*   ES_USER - elasticsearch username for authentification in elasticsearch
*   ES_PASSWORD - elasticsearch user password
*   KIBANA_URL - kibana url, can be provided for dashboard creation, but is not necessary

### Setting up kibana dashboards

Needs to be done only once, from shell command on the container. For a kibana that runs on https:

    ./heartbeat setup -E setup.kibana.host=kibana.devel2cph.eea.europa.eu:443 -E setup.kibana.protocol="https" --dashboards

## Setting up elasticsearch stack

### Rancher template
In rancher, use the Elastic 6 stack: https://github.com/eea/eea.rancher.catalog/tree/master/templates/elastic6-engine.

### Configuration

You can use the default configuration with the following changes:


* ElasticSearch client exposed port - empty
* Cerebro  client exposed port - mandatory, must be unique
* Kibana  client exposed port - empty
* Heap size ( data nodes ) - at least double, if not more than the default value
* Memory limit in byte ( data nodes ) - increase this to be more than heap size, recommended double heap size
* Read only username 
* Read only user password
* Username with write access - this will be used in all beats configuration
* Password for RW Username - this will be used in all beats configuration
* Data volumes driver - local if on CPH
* Data volume driver options - empty if on CPH


### Certificate

For enabling https on elasticsearch and kibana, you need to add the certificate(s) to rancher.

You can use letsencrypt rancher stack to generate them.

### LB configuration

If you use letsencrypt, add the necessary LB services as specified in its documentation.

#### Elasticsearch

1. Add 2 Service Rules - same host, port 80 ( HTTP )  and 443 (HTTPS)  respectively, both targetting the es-client service from the ES stack, port 9200.
2. For the HTTP service rule, add on Backend ( click Show backends ) "force_ssl"
3. Add custom haproxy.cfg:
```
backend force_ssl
    redirect scheme https code 301 if ! { ssl_fc }
```

#### Kibana

1. Add 2 Service Rules - same host, port 80 ( HTTP )  and 443 (HTTPS)  respectively, both targetting the kibana service from the ES stack, port 5601.
2. For the HTTP service rule, add on Backend ( click Show backends ) "force_ssl"
3. Add custom haproxy.cfg ( if exists you do not need to add this twice) :
```
backend force_ssl
    redirect scheme https code 301 if ! { ssl_fc }
```
#### Kibana authentification

4. Create SHA512 passwords for ES write user and Kibana "guest" user
     mkpasswd -m sha-512 password
5. Note the BACKEND name used by the kibana 443 service - 
443_{REPLACE_DOTS_WITH_UNDERLINE_IN_HOST}_

6. Add kibana authentification in haproxy.cfg:

```
global
 userlist ES
   user guest password SHA512GUESTRASS
   user rw password SHA512RWPASS

backend 443_BACKEND_
  acl AuthOK_ES http_auth(ES)
  http-request auth realm ES if !AuthOK_ES
```

### Metricbeat - rancher

To prepare the deploy, you need to request access from all the hosts to the elasticsearch url.

To deploy, use this template: https://github.com/eea/eea.rancher.catalog/tree/master/infra-templates/metricbeat

Default values are already set in rancher, you only need to add the elasticsearch password.

Upgrade/rollback is done the standard way.


### Heartbeat - rancher

You only need one container for all your monitoring.

To prepare the deploy, you need to request access from the container to the elasticsearch url and the urls you will be monitoring.

To deploy, use this template: https://github.com/eea/eea.rancher.catalog/tree/master/infra-templates/heartbeat

You need to set the elasticsearch password, and provide the configuration. To disable logging, please include `logging.metrics.enabled: false` line in the configuration.

#### Upgrade

To add a new check, you will need to upgrade the stack with the new configuration. Make sure that you are saving the new configuration in the SVN.


