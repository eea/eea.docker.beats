FROM docker.elastic.co/beats/metricbeat-oss:6.8.3
USER root
RUN yum install -y python-yaml
RUN mv /usr/local/bin/docker-entrypoint /usr/local/bin/metricbeat-entrypoint 
COPY docker-entrypoint generate_configuration.py /usr/local/bin/
COPY metricbeat.yml /usr/share/metricbeat/metricbeat.yml
