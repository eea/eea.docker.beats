#!/usr/bin/env python

import yaml
import os
import distutils.util

es_url = os.getenv('ES_URL')
es_user = os.getenv('ES_USER')
es_password = os.getenv('ES_PASSWORD', '')
kibana_url = os.getenv('KIBANA_URL')
tags = os.getenv('TAGS')
rancher_env = os.getenv('RANCHER_ENV')
hostname = os.getenv('HOSTNAME')
enable_metrics = os.getenv('ENABLE_METRICS_LOG')

filename = "/usr/share/metricbeat/metricbeat.yml"

file = open(filename)
yaml_doc = yaml.load(file)

if es_url is not None and es_user is not None:
  yaml_doc['output.elasticsearch'] = { 'hosts': es_url , 'username': es_user , 'password': es_password }
elif es_url is not None and es_user is None:   
  yaml_doc['output.elasticsearch'] = { 'hosts': es_url }

if kibana_url is not None:
  yaml_doc['setup.kibana'] = { 'host': kibana_url }


if tags is not None:
  yaml_doc['tags'] =  tags.split(',')

if  rancher_env is not None:
  yaml_doc['name'] = hostname
  yaml_doc['fields_under_root'] = 'true'
  yaml_doc['fields'] = { 'rancher.environment' : rancher_env }
 
if enable_metrics is not None:
  if enable_metrics == 'True':
    yaml_doc['logging.metrics.enabled'] = 'true'
  else:
    yaml_doc['logging.metrics.enabled'] = 'false'

with open(filename, "w") as f:
  yaml.dump(yaml_doc, f, default_flow_style = False)

