'''
Script for migrating all of the tags for the markdown 
files to be the metadata that is at the beginning of them

'''
import json
import base64
import os

import boto3
import mistune
from urllib.parse import urlencode

from dotenv import load_dotenv
load_dotenv()

# Get all aws resources
ph_client = boto3.client('s3',
	aws_access_key_id=os.getenv('PH_AWS_ACCESS_KEY_ID'),
	aws_secret_access_key=os.getenv('PH_AWS_SECRET_ACCESS_KEY'))

brian_client = boto3.client('s3')

markdown = mistune.Markdown()


CONFIG_LIMIT = '---'

# Characters that are allowed in S3 tags that aren't alphanumeric.
# This means almost no punctuation in blog post titles because
# one of the tags for the post-objects is the title
ALLOWED_SPEC_CHARS = ['+','_','-','=','.',':','/',' ']
print('start')


object_list = brian_client.list_objects(Bucket='blogposts-brian')['Contents'];

count = 0
for object in object_list:

	response = brian_client.get_object(Bucket='blogposts-brian', Key=object['Key'])

	body = response['Body'].read()


	config, content = body.decode('utf-8').split(CONFIG_LIMIT)
	config_dict = json.loads(config)


	tagset = dict()

	for key in config_dict:
		tag = config_dict[key]
		if key == 'tags':
			continue

		if key == 'title':
			for ch in tag:
				if not (ch.isalnum() or ch in ALLOWED_SPEC_CHARS):
					print('Invalid title Character:', ch, ' Hexcodes:', ch.encode('utf-8'))
					tag = tag.replace(ch,'')

		tagset[key] = str(tag)

	query = ''
	for tag in tagset:
		query += tag + '=' + tagset[tag] + '&'

	query = query[:-1]

	ph_client.put_object(
		Body=content,
		Key=object['Key'],
		Bucket='blog-posts-pantherhackers',
		Tagging=query
	)

	
	count += 1
print(count, 'lines updated')