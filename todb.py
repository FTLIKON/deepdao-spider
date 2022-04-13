import pymysql
from pymysql.converters import escape_string

# 数据库连接信息
db = pymysql.connect(
    host="119.91.192.183",
    port=3306,
    database="deepdao",
    user="debian-sys-maint",
    password="123456",
    charset='utf8mb4'
)
cursor = db.cursor()

#将sql推送至数据库执行
def sqltodb(sql_str):
    sql_str = sql_str[:-1]+";"
    try:
        cursor.execute(sql_str)
        db.commit()
    except Exception as e:
        print("sql install error", e)
        print(sql_str)
    else:
        print("********sql上传成功*********")
    
# 提取txt，将txt字段拼接成sql-insert语句
def txt_db(file,sql_str):
    for line in open(file, encoding="utf-8"):
        sql_str+="(null" 
        res = line[:-1].split("\t")
        for obj in res:
            sql_str += ", '%s'" % (escape_string(obj))
        sql_str += "),"
    sqltodb(sql_str)


if __name__ == "__main__":

    # 将6个txt文件使用不同的sql语句执行入库
    txt_db("./dao_list.txt","INSERT INTO dao_list (id, platform_name, platform_url, organization_name, organization_url, treasury_count, members_num, proposals_num, snapshot_time, snapshot_date) VALUES ")
    txt_db("./dao_member.txt","INSERT INTO dao_member (id, platform_name, platform_url, organization_name, organization_url, member_username, member_address, member_tokens_share, member_share_percent, member_proposals_created_num, member_proposals_win_percent, member_proposals_lost_percent, member_voted_num, member_voted_win_percent, member_voted_lost_percent, snapshot_time, snapshot_date) VALUES ")
    txt_db("./dao_proposal_list.txt","INSERT INTO dao_proposal_list (id, platform_name, platform_url, organization_name, organization_url, proposal_title, proposal_content, proposal_start_time, proposal_end_time, proposal_proposed_name, proposal_outcome, proposal_votes_num, proposal_for_num, proposal_against_num, snapshot_time, snapshot_date) VALUES ")
    txt_db("./proposal_voter_list.txt","INSERT INTO dao_proposal_voter_list (id, platform_name, platform_url, organization_name, organization_url, proposal_title, proposal_start_time, proposal_end_time, proposal_proposed_name, voter_name, voter_opinion, voter_count, snapshot_time, snapshot_date) VALUES ")
    txt_db("./people_holds.txt","INSERT INTO people_holds (id, platform_name, platform_url, people_username, people_address, people_token_name, people_token_symbol, people_token_address, people_token_value, people_token_usd, people_token_usd_percent, snapshot_time, snapshot_date) VALUES ")
    txt_db("./people_info.txt","INSERT INTO people_info (id, platform_name, platform_url, people_username, people_address, people_participation_score, people_dao_num, people_proposals_created, people_voted_num, people_organization_name, people_organization_votes, people_organization_voted_win, people_organization_proposals, people_organization_proposals_win, snapshot_time, snapshot_date) VALUES ")
    
