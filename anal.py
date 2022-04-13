import datetime
import imp
import json
import time
from pymysql.converters import escape_string

platform_name = "deepdao"
platform_url = "https://deepdao.io/"

def anal_dao_list(daoId, daoName, dao_info):

    organization_name = daoName
    organization_url = daoId
    treasury_count = str(dao_info["data"]["aum"])
    members_num = str(dao_info["data"]["membersCount"])
    proposals_num = str(dao_info["data"]["proposalsCount"])
    snapshot_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    snapshot_date = str(time.strftime("%Y-%m-%d", time.localtime()))
    with open("./dao_list.txt", "a+", encoding="utf-8") as f:
        f.write('\t'.join([platform_name, platform_url, organization_name, organization_url, treasury_count, members_num, proposals_num, snapshot_time, snapshot_date])+'\n')


def anal_dao_proposal_list(daoId, daoName, dao_proposals):

    for proposal in dao_proposals["decisions"]:
        organization_name = daoName
        organization_url = daoId
        proposal_title = escape_string(proposal["title"]).replace("\t","")
        proposal_content = escape_string(proposal["description"]).replace("\t","")
        proposal_start_time = datetime.datetime.strptime(proposal["createdAt"][:-5], "%Y-%m-%dT%H:%M:%S")
        proposal_end_time = proposal_start_time+datetime.timedelta(days=3)
        proposal_proposed_name = str(proposal["proposer"])
        proposal_outcome = str(proposal["status"])
        proposal_votes_num = str(proposal["votes"])
        proposal_for_num = str(proposal["sharesFor"])
        proposal_against_num = str(proposal["sharesAgainst"])
        snapshot_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        snapshot_date = str(time.strftime("%Y-%m-%d", time.localtime()))
        with open("./dao_proposal_list.txt", "a+", encoding="utf-8") as f:
            f.write('\t'.join([platform_name, platform_url, organization_name, organization_url, proposal_title, proposal_content, str(proposal_start_time), str(proposal_end_time), proposal_proposed_name, proposal_outcome, proposal_votes_num, proposal_for_num, proposal_against_num, snapshot_time, snapshot_date])+'\n')


def anal_proposal_voter_list(daoId, daoName, proposal, proposal_voters):

    for voter in proposal_voters["data"]["votes"]:
        organization_name = daoName
        organization_url = daoId
        proposal_title = escape_string(proposal["title"])
        proposal_start_time = datetime.datetime.strptime(proposal["createdAt"][:-5], "%Y-%m-%dT%H:%M:%S")
        proposal_end_time = proposal_start_time+datetime.timedelta(days=3)
        proposal_proposed_name = str(proposal["proposer"])
        voter_name = str(voter["voter"])
        voter_opinion = str(voter["choice"])
        voter_count = str(voter["vp"])
        snapshot_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        snapshot_date = str(time.strftime("%Y-%m-%d", time.localtime()))
        with open("./proposal_voter_list.txt", "a+", encoding="utf-8") as f:
            f.write('\t'.join([platform_name, platform_url, organization_name, organization_url, proposal_title, str(proposal_start_time), str(proposal_end_time), proposal_proposed_name, voter_name, voter_opinion, voter_count, snapshot_time, snapshot_date])+'\n')


def anal_dao_member(daoId, daoName, dao_members):
    for member in dao_members["members"]:
        organization_name = daoName
        organization_url = daoId
        member_username = str(member["name"])
        member_address = str(member["address"])
        member_tokens_share = str(member["tokenShares"])
        member_share_percent = str(member["tokenSharesPercentage"])
        member_proposals_created_num = str(member["proposalsCount"])
        member_proposals_win_percent = str(member["proposalsWonCount"])
        member_proposals_lost_percent = str(member["proposalsLostCount"])
        member_voted_num = str(member["votesCount"])
        member_voted_win_percent = str(member["votesWonCount"])
        member_voted_lost_percent = str(member["votesLostCount"])
        snapshot_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        snapshot_date = str(time.strftime("%Y-%m-%d", time.localtime()))
        with open("./dao_member.txt", "a+", encoding="utf-8") as f:
            f.write('\t'.join([platform_name, platform_url, organization_name, organization_url, member_username, member_address, member_tokens_share, member_share_percent, member_proposals_created_num, member_proposals_win_percent, member_proposals_lost_percent, member_voted_num, member_voted_win_percent, member_voted_lost_percent, snapshot_time, snapshot_date])+'\n')

def anal_people_info(people_info,people_proposals, people_votes):

    people_organization = {}
    for dao_id in people_proposals:
        for proposal in people_proposals[dao_id]:
            people_organization[proposal["daoName"]] = {"votes":0,"votes_win":0,"proposals":0,"proposals_win":0}
            break
    for dao_id in people_votes:
        for vote in people_votes[dao_id]:
            people_organization[vote["daoName"]] = {"votes":0,"votes_win":0,"proposals":0,"proposals_win":0}
            break

    for dao_id in people_proposals:
        for proposal in people_proposals[dao_id]:
            people_organization[proposal["daoName"]]["proposals"] += 1
            try:
                if proposal["successfulVote"]:
                    people_organization[proposal["daoName"]]["proposals_win"] += 1
            except Exception as e:
                pass
    for dao_id in people_votes:
        for vote in people_votes[dao_id]:
            people_organization[vote["daoName"]]["votes"] += 1
            try:
                if vote["successful"]:
                    people_organization[vote["daoName"]]["votes_win"] += 1
            except Exception as e:
                pass
    people_username = people_info["name"]
    people_address = people_info["address"]
    people_participation_score = str(people_info["participationScore"])
    people_dao_num = str(people_info["daoAmount"])
    people_proposals_created = str(people_info["proposalsAmount"])
    people_voted_num = str(people_info["votesAmount"])
    for dao_name in people_organization:
        people_organization_name = dao_name
        people_organization_votes = str(people_organization[dao_name]["votes"])
        people_organization_voted_win = str(people_organization[dao_name]["votes_win"])
        people_organization_proposals = str(people_organization[dao_name]["proposals"])
        people_organization_proposals_win = str(people_organization[dao_name]["proposals_win"])
        snapshot_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        snapshot_date = str(time.strftime("%Y-%m-%d", time.localtime()))
        with open("./people_info.txt", "a+", encoding="utf-8") as f:
            f.write('\t'.join([platform_name,platform_url,people_username,people_address,people_participation_score,people_dao_num,people_proposals_created,people_voted_num,people_organization_name,people_organization_votes,people_organization_voted_win,people_organization_proposals,people_organization_proposals_win, snapshot_time, snapshot_date])+'\n')
    
def anal_people_holds(people_list):
    for people in people_list:

        people_username = people["name"]
        people_address = people["address"]
        for token in people["daos"]["tokens"]:
            people_token_name = str(token["name"])
            people_token_symbol = str(token["symbol"])
            people_token_address = str(token["tokenAddress"])
            people_token_value = str(token["value"])
            people_token_usd = str(token["usd"])
            people_token_usd_percent = str(token["usdVolumePercent"])
            snapshot_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            snapshot_date = str(time.strftime("%Y-%m-%d", time.localtime()))
            with open("./people_holds.txt", "a+", encoding="utf-8") as f:
                f.write('\t'.join([platform_name,platform_url,people_username,people_address,people_token_name,people_token_symbol,people_token_address,people_token_value,people_token_usd,people_token_usd_percent, snapshot_time, snapshot_date])+'\n')
    