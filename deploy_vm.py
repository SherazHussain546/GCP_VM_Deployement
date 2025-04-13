import googleapiclient.discovery

def create_vm(project, zone, instance_name):
    compute = googleapiclient.discovery.build('compute', 'v1')

    config = {
        'name': instance_name,
        'machineType': f"zones/{zone}/machineTypes/e2-standard-2",
        'disks': [{
            'boot': True,
            'autoDelete': True,
            'initializeParams': {
                'sourceImage': 'projects/ubuntu-os-cloud/global/images/family/ubuntu-2004-lts',
                'diskSizeGb': '250'
            }
        }],
        'networkInterfaces': [{
            'network': 'global/networks/default',
            'accessConfigs': [{'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}]
        }],
        'tags': {'items': ['http-server', 'https-server']},
        'metadata': {
            'items': [{
                'key': 'startup-script',
                'value': '''#!/bin/bash
                sudo apt update
                sudo apt install apache2 -y
                echo "<h1>Hello World from $(hostname)</h1>" | sudo tee /var/www/html/index.html
                sudo systemctl enable apache2
                sudo systemctl start apache2
                '''
            }]
        }
    }

    return compute.instances().insert(
        project=project,
        zone=zone,
        body=config
    ).execute()

# --- RUN THE FUNCTION ---
create_vm(
    project='vmcheck-sheraz',
    zone='us-central1-a',
    instance_name='instance-sheraz-ca'
)
