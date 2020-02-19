import argparse
import json

parser = argparse.ArgumentParser(description = 'Fetches information about the given autonomous system (AS) and related interconnection points (IXPs)')
parser.add_argument("ASN",
                    help="Autonomous System Number")
args = parser.parse_args()

print('=========================\nAS Relationships\n=========================')

found_rel = False
rel_file = open("./as_rel.txt", "r", encoding='latin-1')

rel_mapping = {
	'0': 'P2P Link',
	'-1': 'Customer',
	'1': 'Provider'
}
rels = dict()

for line in rel_file:
	info = line.strip().split()
	if info[0] == args.ASN:
		rels[int(info[1])] = rel_mapping[info[2]]
		if not found_rel:
			found_rel = True

if found_rel:
	print('\nASN\t|\tRelationship\n')
	for ASN in sorted(rels.keys()):
		print('{}\t|\t{}'.format(ASN, rels[ASN]))

rel_file.close()

if not found_rel:
	print("\nERROR:\n\tASN not found in file\n\t\tas_rel.txt\n\tfrom\n\t\thttps://www.caida.org/data/as-taxonomy/\n")

print('\n=========================\nIXP Details\n=========================')

found_ip = False
ip_addr_file = open("./ix-asns_201910.json", "r", encoding="latin-1")

ixp_file = open("./ixs_201910.json", "r", encoding="latin-1")

for line in ip_addr_file:
	info = json.loads(line.strip())
	if info['asn'] == int(args.ASN):
		print('\nIXP ID\t:\t{}\n\tIPv4 Addresses:\t{}\n\tIPv6 Addresses:\t{}'.format(info['ix_id'], info['ipv4'], info['ipv6']))
		for line in ixp_file:
			ixp_info = json.loads(line.strip())
			if ixp_info['ix_id'] == info['ix_id']:
				ixp = {
					'name' : 'N/A',
					'city' : 'N/A',
					'state' : 'N/A',
					'country' : 'N/A',
					'region' : 'N/A',
					'prefixes' : {
						'ipv4' : 'N/A',
						'ipv6' : 'N/A'
					},
					'url': 'N/A'
				}
				ixp_k = ixp_info.keys()
				for k in ixp.keys():
					if k in ixp_k:
						ixp[k] = ixp_info[k]
				print('\tName:\t\t{}\n\tCity:\t\t{}\n\tState:\t\t{}\n\tCountry:\t{}\n\tRegion:\t\t{}\n\tIPv4 Prefixes:\t{}\n\tIPv6 Prefixes:\t{}\n\tURL:\t\t{}'\
					.format(ixp['name'], ixp['city'], ixp['state'], ixp['country'], ixp['region'], ixp['prefixes']['ipv4'], ixp['prefixes']['ipv6'], ixp['url']))

		if not found_ip:
			found_ip = True

ip_addr_file.close()
ixp_file.close()

if not found_ip:
	print("\nERROR:\n\tASN not found in file\n\t\tix-asns_201910.json\n\tfrom\n\t\thttps://www.caida.org/data/ixps/\n")

print('\n=========================\nAutonomous System Details\n=========================')

class_mapping = {
	't1': 'Large ISP',
	't2': 'Small ISP',
	'edu': 'University',
	'ix': 'IXP',
	'nic': 'NIC',
	'comp': 'Customer',
	'abstained': 'Undefined'
}

found_attr = False
attr_file = open("./as2attr.txt", "r", encoding='latin-1')

for line in attr_file:
	info = line.strip().split('\t')
	if info[0] == args.ASN:
		print("\nAS Number:\t{}\nOrg Record:\t{}\nProviders:\t{}\nPeers:\t\t{}\nCustomers:\t{}\nNumber of /24 prefixes:\t{}\nAdvertised IP Prefixes:\t{}\nAS Class:\t{}\n"
			.format(info[0], info[1].strip(), info[2].strip(), info[3].strip(), info[4].strip(), info[5].strip(), info[6].strip(), class_mapping[info[7]]))
		found_attr = True
		break

attr_file.close()

if not found_attr:
	print("\nERROR:\n\tASN not found in file\n\t\tas2attr.txt\n\tfrom\n\t\thttps://www.caida.org/data/as-taxonomy/\n")
