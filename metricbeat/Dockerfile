FROM docker.elastic.co/beats/metricbeat:7.16.2
USER root
RUN yum install -y python-yaml
RUN mv /usr/local/bin/docker-entrypoint /usr/local/bin/metricbeat-entrypoint 
COPY docker-entrypoint generate_configuration.py /usr/local/bin/
COPY metricbeat.yml /usr/share/metricbeat/metricbeat.yml
