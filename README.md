# personal-pods
This allows you to create your own PODS (Personal Online DataStore) for use in the SOLID (SOcially LInked Data) ecosystem

## Steps to create a PODS in Amazon AWS

1. Create an Amazon AWS account (if necessary)
1. Log in to the AWS Console using the Root Account (https://aws.amazon.com/console/)
1. Create a PODS_User account (NOTE: you should NOT use your Root account to manage your Personal PODS)
    1. Use https://lightsail.aws.amazon.com/ls/docs/en_us/articles/amazon-lightsail-managing-access-for-an-iam-user as a guide
    1. Create a new IAM Lightsail Policy
    1. Create a new IAM Lightsail Group, add the policy to the group
    1. Create a new IAM Lightsail User, add the user to the group
1. Create a new EC2 instance using Amazon Lightsail
    1. Create a basic Ubuntu Instance
1. Reserve a Static IP address
    1. In the AWS Lightsail Console, click on the Networking tab for your PODS
    1. Click the "Attach Static IP" button
1. Open up port 443 on the Firewall for HTTPS traffic
    1. In the AWS Lightsail Console, click on the Networking tab for your PODS
    1. Under the Firewall section, add a new rule
        1. HTTPS, TCP, 443, Any IP address
1. Create DNS "A record" for your static IP address
    1. A, scott.littlepath.org, 54.212.93.142
1. Install Caddy2 web server
    1. https://caddyserver.com/v2
    1. Follow these instructions to install/configure Caddy2: 
        1. https://caddyserver.com/docs/install
        1. For the new Caddy user for Ubuntu, see: https://github.com/LittlePath/personal-pods/blob/master/CreateNewUser.md
        1. Copy this `caddy.service` file to `/etc/systemd/system/caddy.service`: https://github.com/LittlePath/personal-pods/blob/master/caddy.service
        1. Copy this `Caddyfile` file to `/etc/caddy/Caddyfile` : https://github.com/LittlePath/personal-pods/blob/master/Caddyfile
            1. NOTE: Be sure to change the first line to match your DNS name
    1. Visit https://your.pods.address in a browser to verify that Caddy2 is up and running on port 443. 


## Steps to manage PODS using the python script

To create a PODS (Personal Online DataStore)
1. Configure AWS
    1. To install the AWS CLI v2 tools, see https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html
    1. Run `aws configure` to set your aws credentials. Your aws user needs to have access to iam and lightstail permissions
1. Set up python libraries
    1. Create your python virtual env with `virtualenv .venv -p python3`
    1. Start it with `source .venv/bin/activate`
    1. Install libraries with `pip install -r requirements.txt`
1. Run `PODS_USER=<preferred-pods-name> python3 create_pods.py`
    1. You can enter the IP address printed in the `python3 create_pods.py` command output in your browser to see Caddy running

To delete a PODS (Personal Online DataStore) created with the python script above 
1. Run `PODS_USER=<preferred-pods-name> python3 teardown_pods.py`

### Possible Issues
Not enough access - Check your IAM role permissions
Availability zone not valid - It is currently hardcoded to `'us-east-1a'` and should be parameterized as an argument for the script.

### Remaining Work
1. After creating a PODS IAM user, switch to using that user for creating the Lightsail instance (we don't want to use a root user for Lightsail for least priviledge reasons)
2. Automate DNS creation
3. Automate Caddy setup following the steps in this section 'Steps to create a PODS in Amazon AWS'