'''
Script for migrating all of the tags for the markdown 
files to be the metadata that is at the beginning of them

'''
import json
import base64

import boto3
import mistune


client = boto3.client('s3')
s3 = boto3.resource('s3')
bucket = s3.Bucket('blog-posts-pantherhackers')

markdown = mistune.Markdown()

CONFIG_LIMIT = '---'

ALLOWED_SPEC_CHARS = ['+','_','-','=','.',':','/',' ']
print('start')

client.upload_file('upload.py', 'blog-posts-pantherhackers', 'upload.py')

for object in client.list_objects(Bucket='blog-posts-pantherhackers'):

	s3_file_pointer = s3.Object('blog-posts-pantherhackers', object.key)
	file = object.get()

	body = file['Body'].read().decode('utf-8')

	config = body.split(CONFIG_LIMIT)[0]

	config_dict = json.loads(config)


	tagset = dict()
	tagset['TagSet'] = []

	print(object)