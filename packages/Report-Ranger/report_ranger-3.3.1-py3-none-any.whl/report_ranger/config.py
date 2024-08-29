import os
from platformdirs import user_config_dir
import yaml
import logging
import copy
import report_ranger

log = logging.getLogger(__name__)


# This is to fill in the defaults so there's not too many variables
config = {
    "default_template": '',
    "default_input_file": 'reportbody.md',
    "default_output_file": 'report-preview.md',
    "format": '',
    "verbose": False,
    # The template mapper. This gives the locations of template files for each template.
    "templatemapper": {
    },
    # Additional template mapper files to link.
    "templatemappers": [
    ],
    # Files with additional
    "includes": {
    }
}

envvars = {
    'RR_TEMPLATE': "default_template",
    'RR_INPUT_FILE': 'default_input_file',
    'RR_OUTPUT_FILE': 'default_input_file',
    'RR_VERBOSE': 'verbose',
    'RR_TEMPLATEMAPPERS': 'templatemappers'
}

def get_config_from_file(file):
    try:
        with open(file, 'r') as vf:
            config = yaml.safe_load(vf)
            log.debug(f"Processing config file {file}")
            return config
    except:
        log.debug(f"Could not open config file {file}")
        return {}

def get_config(arg_file = None):
    final_config = copy.copy(config)
    
    for config_location in [user_config_dir('reportranger', 'Volkis') + '/config.yml', 'config.yml']:
        if config_location:
            final_config.update(get_config_from_file(config_location))

    final_config['templatemapper']["sample"] = os.path.join(os.path.dirname(os.path.realpath(report_ranger.__file__)),"default-templates/sample-template/rr-sample-template.md") # Add in the sample template
    final_config['templatemapper']["plain"] = os.path.join(os.path.dirname(os.path.realpath(report_ranger.__file__)),"default-templates/plain-template/rr-plain-template.md") # Add in the sample template
    
    for config_location in [user_config_dir('reportranger', 'Volkis') + '/config.yml', 'config.yml']:
        if config_location:
            final_config.update(get_config_from_file(config_location))

    # Sort out environment variables
    for envvar in envvars.keys():
        log.debug(f"Getting envvar {envvar}")
        var = os.getenv(envvar)
        log.debug(f"Got {var}")
        if var != None:
            log.debug(f"Setting config variable {envvars[envvar]} to {var} from environment variable {envvar}")
            if isinstance(final_config[envvars[envvar]], dict):
                final_config[envvars[envvar]] += var.split(':')
            final_config[envvars[envvar]] = var
    
    for config_location in [arg_file]:
        if config_location:
            final_config.update(get_config_from_file(config_location))
    
    return final_config

