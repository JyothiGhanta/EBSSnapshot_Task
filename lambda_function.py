import json
import boto3
import datetime

today = datetime.date.today()
today_string = today.strftime('%Y/%m/%d')
def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    regions_des = ec2.describe_regions().get('Regions')
    regions = [ region['RegionName'] for region in regions_des]

    for region_name in regions:
        #print('Instances in EC2 Region {0}:'.format(region_name))
        ec2 = boto3.resource('ec2', region_name = region_name)
        instances = ec2.instances.filter(
         Filters = [{
              'Name': 'tag:priority',
              'Values': ['high']
                   }]
            )
        for i in instances.all():
            for tag in i.tags: 
                if tag['Key'] == 'priority' and tag['Value'] == 'high' and i.state == 'stopped':
                   print('Found snapshot  tagged instance with id: {0}, state: {1}'.format(i.id,i.state['Name']))
                   vols = i.volumes.all()
                   print(vols)
                   for v in vols:
                       print('{0} is attached to volume {1}, proceeding to snapshot'.format(i.id, v.id))
                       response = cloudwatch.put_metric_data(
        MetricData = [
            {
                'MetricName': 'snapshot',
                'Dimensions': [
                    {
                        'Name': 'PURCHASES_SERVICE',
                        'Value': 'CoolService'
                    },
                    {
                        'Name': 'APP_VERSION',
                        'Value': '1.0'
                    },
                ]
            },
        ],
        Namespace = 'snapshot'
    )
                       snapshot = v.create_snapshot(
                       Description = 'Snapshot of {0}, on volume {1} - Created {2}'.format(i.id, v.id, today_string),)
                       snapshot.create_tags( 
                                Tags=[{
                                       'Key': 'auto_snapshot',
                                        'Value': 'true'
                                     }, {
                                       'Key': 'volume',
                                       'Value': v.id
                                     }, {
                                       'Key': 'CreatedOn',
                                       'Value': today_string
                                      },])

       
