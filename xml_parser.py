import xml.etree.ElementTree as ET
import os
from urllib.request import urlopen
# import ssl
# import requests

# TODO: Eventually, you should move these to a config file or something. Call it 'data_sources.cfg' or something like that.
senate_xml_location = 'https://www.gpo.gov/fdsys/bulkdata/BILLS/115/1/s/BILLS-115s106is.xml'

# Source: https://www.federalregister.gov/developers/api/v1
federal_register_api = "https://www.federalregister.gov/api/v1"
# Search all Federal Register documents published since 1994.
federal_register_documents_resource = "/documents."
federal_register_documents_formats = ["json", "csv"]
federal_register_documents_fields = ["abstract", "action", "agencies", "agency_names", "body_html_url", "crf_refences", "citation", "comment_url", "comments_close_on", "correction_of", "corrections", "dates", "docket_id", "docket_ids", "document_number", "effective_on", "end_page", "excerpts", "executive_order_notes", "executive_order_number", "full_text_xml_url", "html_url", "images", "json_url", "mods_url", "page_length", "pdf_url", "president", "public_inspection_pdf_url", "publication_date", "raw_text_url", "regulation_id_number_info", "regulation_id_numbers", "regulations_dot_gov_info", "regulations_dot_gov_url", "significant", "signing_date", "start_page", "subtype", "title", "toc_doc", "toc_subject", "topics", "type", "volume"]
federal_register_documents_per_page = "20"
federal_register_documents_order = ["relevance", "newest", "oldest", "executive_order_number"]

# Fetches all agency details.
federal_register_agencies_resource = "/agencies"

doc_format = "json"
executive_orders_source = federal_register_api + federal_register_documents_resource + "json" + "?order=" + "newest" + "&presidential_document_type=" + "executive_order&=" + "donald-trump"
print("EXEC STRING:\t\t", executive_orders_source)

executive_xml_location = ''

congress_session = ['113','114','115']
chamber = ['house', 'senate']
# https://github.com/usgpo/bulk-data/blob/master/Bills-Summary-XML-User-Guide.md
house_bills = [{"bill" : "hr"}, {"joint_resolution" : "hjres"}, {"concurrent_resolution" : "hconres"}]
senate_bills = [{"bill" : "s", "joint_resolution" : "sjres", "concurrent_resolution" : "sconres" }] 
measure_type = ['hr', 'sres']
# xml_location = "https://www.gpo.gov"
bills = []
# tree = ET.ElementTree(file='work.xml')


# ignoreElems = ['displayNameKey', 'displayName']
def get_json_data(json_path):
	f = urlopen(json_path)
	r = f.read()
	# tree = ET.fromstring(r)

	write_to_file(r, 'exec_orders.json')

	# return tree


'''
	Gets the bulk congressional bill data
'''
def get_xml_data(xml_path):
	# print('get_congressional_bills\n')

	f = urlopen(xml_path)
	r = f.read()
	tree = ET.fromstring(r)

	write_to_file(r, extract_file_name(xml_path))

	return tree


def extract_file_name(filepath_string):
	s = filepath_string.split("/")
	print("\n\n\n",s[-1])
	return s[-1]




'''
'''
def write_to_file(text_to_publish, new_file_name):
	# NOTE: SHOULD USE THE ORIGINAL NAME OF THE BILL HERE.
	with open(new_file_name, 'wb') as fd:
		# for chunk in r.(chunk_size=128):
		fd.write(text_to_publish)


'''
	Prints an XML structure recursively
'''
def printRecur(indent, root):
	# print('printRecur\n')

	"""Recursively prints the tree."""
	# if root.tag in ignoreElems:
	# return
	print(' '*indent + '%s: %s' % (root.tag.title(), root.attrib.get('name', root.text)))
	# global indent
	indent += 4
	for elem in root.getchildren():
		printRecur(indent, elem)
	indent -= 4


# root = tree.getroot()

senate_xml_tree = get_xml_data(senate_xml_location)
get_json_data(executive_orders_source)

# tree = ET.ElementTree(file=xml_location)
# print(dir(xml_tree.text))
# root = tree.getroot()
indent = 0
printRecur(indent, senate_xml_tree)
# import ssl
# import urllib.request

# ctx = ssl.create_default_context()
# ctx.check_hostname = False
# ctx.verify_mode = ssl.CERT_NONE
# url_string = "https://www.gpo.gov"

# try:
# 	with urllib.request.urlopen(url_string, context=ctx) as u, \
# 			open(file_name, 'wb') as f:
# 		f.write(u.read())
# except Exception as e:
# 	print("NO", e)
# # printRecur(root)