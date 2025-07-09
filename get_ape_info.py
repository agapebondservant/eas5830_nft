from web3 import Web3
from web3.providers.rpc import HTTPProvider
from web3.middleware import ExtraDataToPOAMiddleware
import requests
import json
import traceback

bayc_address = "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"
contract_address = Web3.to_checksum_address(bayc_address)

# You will need the ABI to connect to the contract
# The file 'abi.json' has the ABI for the bored ape contract
# In general, you can get contract ABIs from etherscan
# https://api.etherscan.io/api?module=contract&action=getabi&address=0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D
with open('ape_abi.json', 'r') as f:
    abi = json.load(f)


url = "https://bsc-testnet.infura.io/v3/af83c96cc0ff485bb901f9ed92726df3"
w3 = Web3(HTTPProvider(url))
w3.middleware_onion.add(ExtraDataToPOAMiddleware)
contract = w3.eth.contract(address=contract_address, abi=abi)
jwt='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiI3ZGVkZjdmZi1mZWFiLTQzOTItYmZlMi05ODYxZjg3ZWQxMWIiLCJlbWFpbCI6Im9hd29mb2x1QHNlYXMudXBlbm4uZWR1IiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInBpbl9wb2xpY3kiOnsicmVnaW9ucyI6W3siZGVzaXJlZFJlcGxpY2F0aW9uQ291bnQiOjEsImlkIjoiRlJBMSJ9LHsiZGVzaXJlZFJlcGxpY2F0aW9uQ291bnQiOjEsImlkIjoiTllDMSJ9XSwidmVyc2lvbiI6MX0sIm1mYV9lbmFibGVkIjpmYWxzZSwic3RhdHVzIjoiQUNUSVZFIn0sImF1dGhlbnRpY2F0aW9uVHlwZSI6InNjb3BlZEtleSIsInNjb3BlZEtleUtleSI6ImVhZWM0OGFiY2FlNjdiNzFlNTRkIiwic2NvcGVkS2V5U2VjcmV0IjoiN2Y2OTE0MjBkNzU2ZmJjODg3Zjc3ZGZiOWEyNWEyM2FhYTc4YWUxY2IyYTM5ODYwZmE4NDM3NWZkYjZiMTU1MSIsImV4cCI6MTc4MzA0NjYyOX0.Y-M-9tlsLugpcKGJZhcIwFnct0_u3IzdQDTwFTZMZg0'
gateway = "gateway.pinata.cloud"

############################
# Connect to an Ethereum node
api_url = "https://mainnet.infura.io/v3/af83c96cc0ff485bb901f9ed92726df3"  # YOU WILL NEED TO PROVIDE THE URL OF AN ETHEREUM NODE
provider = HTTPProvider(api_url)
web3 = Web3(provider)


def get_ape_info(ape_id):
    assert isinstance(ape_id, int), f"{ape_id} is not an int"
    assert 0 <= ape_id, f"{ape_id} must be at least 0"
    assert 9999 >= ape_id, f"{ape_id} must be less than 10,000"

    data = {'owner': "", 'image': "", 'eyes': ""}

    # YOUR CODE HERE
    try:
        owner = contract.functions.ownerOfs(ape_id).call() 
        tokenURI = contract.functions.tokenURI(ape_id).call() 
        _, _, tokenCID = tokenURI.partition("ipfs://")
        imageMetadata = get_from_ipfs(tokenCID)
        print(imageMetadata)
        data = {'owner': owner, 'image': tokenURI, 'eyes': imageMetadata['eyes']}

        assert isinstance(data, dict), f'get_ape_info{ape_id} should return a dict'
        assert all([a in data.keys() for a in
                    ['owner', 'image', 'eyes']]), f"return value should include the keys 'owner','image' and 'eyes'"
        return data
    except:
        traceback.print_exc()

def get_from_ipfs(cid,content_type="json"):
    assert isinstance(cid,str), f"get_from_ipfs accepts a cid in the form of a string"
    url = f"https://{gateway}/ipfs/{cid}"
    response = requests.get(url, headers={"cid":cid, "Authorization": f"Bearer {jwt}"})
    data = response.json()
    assert isinstance(data,dict), f"get_from_ipfs should return a dict"
    return data