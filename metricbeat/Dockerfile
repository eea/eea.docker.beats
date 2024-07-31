FROM docker.elastic.co/beats/metricbeat:7.17.23
USER root
RUN apt-get update -q \
 && apt-get install -y python python-yaml \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* \
 && mv /usr/local/bin/docker-entrypoint /usr/local/bin/metricbeat-entrypoint 

COPY docker-entrypoint generate_configuration.py /usr/local/bin/

COPY metricbeat.yml /usr/share/metricbeat/metricbeat.yml

