# this file is used to start scrapyd with twistd -y

from engine import get_application
application = get_application()

# MetricsReporter(config)
