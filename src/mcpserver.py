from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from os import getenv
import httpx, sys
import pycountry
import asyncio

load_dotenv()
mcp = FastMCP(getenv('AGENT_NAME'))
api = getenv('EXTERNAL_API')
client = httpx.AsyncClient()

@mcp.tool()
async def run_docker_command(command: str) -> dict:
    """Runs a Docker command in the shell.

    Args:
        command: The Docker command to execute.
    """
    try:
        process = await asyncio.create_subprocess_shell(
            f"docker {command}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            return {"stdout": stdout.decode().strip()}
        else:
            return {"error": f"Command failed with exit code {process.returncode}", "stderr": stderr.decode().strip()}
    except FileNotFoundError:
        return {"error": "Docker command not found. Is Docker installed and in your PATH?"}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def getTypesOfSources(country: str) -> dict:
    """Get distribution of the types of publication sources (journal, repository, book series, conference, etc..) for a country.

    Args:
        country: full name of the country (string)
    """

    _countryCode = pycountry.countries.lookup(country)
    _params = {
        'filter': f'country_code:{_countryCode.alpha_2}',
        'group_by': 'type',
    }
    _url = f'{api}/sources'
    response = await client.get(_url, params=_params)

    if response.status_code != 200:
        return {
            'error': f"API returned {response.status_code}",
            'detail': response.text
        }

    data = response.json()
    if 'group_by' not in data:
        return {
            'error': "Missing 'meta' in API response",
            'response': data
        }
    
    result = {
        item["key_display_name"]: item["count"]
        for item in data["group_by"]
    }

    return {
        "country": country,
        "PublicationSourceTypeCounts": result
    }

@mcp.tool()
async def getNumberOfSources(country: str) -> dict:
    """Get number of publication sources (journal, repository, book series, conference, etc..) for a country.

    Args:
        country: full name of the country (string)
    """

    _countryCode = pycountry.countries.lookup(country)
    _params = {
        'filter': f'country_code:{_countryCode.alpha_2}',
    }
    _url = f'{api}/sources'
    response = await client.get(_url, params=_params)

    if response.status_code != 200:
        return {
            'error': f"API returned {response.status_code}",
            'detail': response.text
        }

    data = response.json()

    if 'meta' not in data:
        return {
            'error': "Missing 'meta' in API response",
            'response': data
        }

    return {
        'country': country,
        'numberOfPublicationSources': data['meta']['count']
    }

@mcp.tool()
async def getNamesOfSources(country: str) -> dict:
    """Get the Names of publication sources for a country.

    Args:
        country: full name of the country (string)
    """

    _countryCode = pycountry.countries.lookup(country)
    _params = {
        'filter': f'country_code:{_countryCode.alpha_2}',
        'page': 1,
    }
    _url = f'{api}/sources'

    has_more_pages = True
    fewer_than_10k_results = True
    functionResponse = []
    loop_index = 0

    while has_more_pages and fewer_than_10k_results:
        _httpResponse = await client.get(_url, params=_params)
        
        if _httpResponse.status_code != 200:
            return {
                'error': f"API returned {_httpResponse.status_code}",
                'detail': _httpResponse.text
            }
        
        data = _httpResponse.json()

        if 'meta' not in data:
            return {
                'error': "Missing 'meta' in API response",
                'response': data
            }

        if 'results' not in data:
            return {
                'error': "Missing 'results' in API response",
                'response': data
            }
        
        pagedResponse = [transform_result(r) for r in data.get("results", [])]
        functionResponse.extend(pagedResponse)
        _params['page'] += 1

        per_page = data.get("meta", {}).get("per_page")
        has_more_pages = len(pagedResponse) == per_page
        fewer_than_10k_results = per_page * _params['page'] <= 10000
        loop_index += 1

    return {
        'country': country,
        'getNamesOfPublicationSources': functionResponse
    }

@mcp.tool()
def transform_result(result):
    """Cleans up the result from https://api.openalex.org
       It needs to be exposed to the MCP client to be used.

    Args:
        The result (JSON)
    """
    item = {
        "name": result.get("display_name"),
        "issn_l": result.get("issn_l"),
        "host_organization_name": result.get("host_organization_name"),
        "works_count": result.get("works_count"),
        "cited_by_count": result.get("cited_by_count"),
        "type": result.get("type"),
    }

    for key in ["subfield", "field", "domain"]:
        value = result.get(key, {}).get("display_name")
        if value:
            item[key] = value

    return item

def serverMain(_transport):
    print('MCP Server started...', _transport)
    mcp.run(transport=_transport)

if __name__=="__main__":
    validTransport = ['sse', 'stdio']
    if (len(sys.argv) > 1 and sys.argv[1] in validTransport):
        transport = sys.argv[1]
    else:
        transport = 'stdio'
    serverMain(transport)