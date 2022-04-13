import json
import requests
import time
import random
import anal

payload = {}
headers = {
    'authority': 'golden-gate-server.deepdao.io',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6'
}


def try_get(url, payload, headers):

    while True:
        try:
            response = requests.request("GET", url, headers=headers, data=payload, timeout=10)
        except Exception as e:
            print(e)
        else:
            time.sleep(random.randint(1, 3))
            return json.loads(response.text)


def get_proposal_voter(proposal_id):
    payload = json.dumps({
        "operationName": "Votes",
        "variables": {
            "id": proposal_id,
            "orderBy": "vp",
            "orderDirection": "desc",
            "first": 100000,
            "skip": 0
        },
        "query": "query Votes($id: String!, $first: Int, $skip: Int, $orderBy: String, $orderDirection: OrderDirection, $voter: String) {\n  votes(\n    first: $first\n    skip: $skip\n    where: {proposal: $id, vp_gt: 0, voter: $voter}\n    orderBy: $orderBy\n    orderDirection: $orderDirection\n  ) {\n    ipfs\n    voter\n    choice\n    vp\n    vp_by_strategy\n  }\n}"
    })
    headers = {
        'authority': 'hub.snapshot.org',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6',
        'content-type': 'application/json',
        'origin': 'https://snapshot.org',
        'referer': 'https://snapshot.org/',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
    }
    url = "https://hub.snapshot.org/graphql"
    while True:
        try:
            response = requests.request("POST", url, headers=headers, data=payload, timeout=10)
        except Exception as e:
            print(e)
        else:
            time.sleep(random.randint(1, 3))
            return json.loads(response.text)


if __name__ == "__main__":
    # 采集dao的id，并按照资金量排序
    dao_list = try_get("https://golden-gate-server.deepdao.io/dashboard/ksdf3ksa-937slj3", payload, headers)
    sorted_daos = []
    for dao in dao_list["daosSummary"]:
        sorted_daos.append((float(dao["totalValueUSD"]) if dao["totalValueUSD"] else 0.0, dao["organizationId"], dao["daoName"]))
    sorted_daos.sort(reverse=True)
    
    # 采集TOP100 dao的基础信息，并解析至dao_list表
    for dao in sorted_daos[:100]:
        dao_info = try_get("https://golden-gate-server.deepdao.io/organization/ksdf3ksa-937slj3/{}".format(dao[1]), payload, headers)
        anal.anal_dao_list(dao[1], dao[2], dao_info)

    # 采集TOP10 dao的全部提案，并解析至dao_proposal_list表
    for dao in sorted_daos[:10]:
        dao_id = try_get("https://golden-gate-server.deepdao.io/organization/ksdf3ksa-937slj3/{}/dao".format(dao[1]), payload, headers)["data"][0]["daoId"]
        dao_proposals = try_get("https://golden-gate-server.deepdao.io/organization/ksdf3ksa-937slj3/{}/governance/decisions".format(dao_id), payload, headers)
        anal.anal_dao_proposal_list(dao[1], dao[2], dao_proposals)
    # 采集TOP1 dao的全部提案的投票，并解析至dao_proposal_voter_list表
    dao_id = try_get("https://golden-gate-server.deepdao.io/organization/ksdf3ksa-937slj3/{}/dao".format(sorted_daos[0][1]), payload, headers)["data"][0]["daoId"]
    dao_proposals = try_get("https://golden-gate-server.deepdao.io/organization/ksdf3ksa-937slj3/{}/governance/decisions".format(dao_id), payload, headers)
    for proposal in dao_proposals["decisions"]:
        proposal_voters = get_proposal_voter(proposal["id"])
        anal.anal_proposal_voter_list(sorted_daos[0][1], sorted_daos[0][2], proposal, proposal_voters)

    # 采集TOP10 dao的成员信息，并解析至dao_member表
    for dao in sorted_daos[:10]:
        dao_id = try_get("https://golden-gate-server.deepdao.io/organization/ksdf3ksa-937slj3/{}/dao".format(dao[1]), payload, headers)["data"][0]["daoId"]
        dao_members = try_get("https://golden-gate-server.deepdao.io/organization/ksdf3ksa-937slj3/{}/members".format(dao_id), payload, headers)
        anal.anal_dao_member(dao[1], dao[2], dao_members)
    
    # 采集TOP100 用户信息，并解析至people_info表
    for offset in (0,50):
        people_list = try_get("https://golden-gate-server.deepdao.io/people/top?limit=50&offset={}&sortBy=participationScore".format(offset), payload, headers)
        for people in people_list[:10]:
            people_proposals = try_get("https://golden-gate-server.deepdao.io/user/2/{}/proposals".format(people["address"]), payload, headers)
            people_votes = try_get("https://golden-gate-server.deepdao.io/user/2/{}/votes".format(people["address"]), payload, headers)
            anal.anal_people_info(people, people_proposals, people_votes)
    
    # 采集TOP100 用户的代币持有信息，并解析至people_holds表
    for offset in (0,50):
        people_list = try_get("https://golden-gate-server.deepdao.io/people/top?limit=50&offset={}&sortBy=participationScore".format(offset), payload, headers)
        anal.anal_people_holds(people_list)
    
