import datetime

import pytz
from github import Github

"""README

1. inptut your github personal token in GITHUB_PERSONAL_TOKEN below
2. run this file and re-direct the output to a file, e.g., ./stats.log. via: `python stats.py > ./stats.log`
3. wait for a while, and then check the stats.log file.
"""

GITHUB_PERSONAL_TOKEN = ""
SINCE_DATETIME = datetime.datetime(2022, 11, 6).replace(tzinfo=pytz.timezone("UTC"))
UNTIL_DATETIME = datetime.datetime(2023, 11, 6).replace(tzinfo=pytz.timezone("UTC"))


def get_review_count(repo_name):
    g = Github(GITHUB_PERSONAL_TOKEN)
    repo = g.get_repo(repo_name)

    pull_requests = repo.get_pulls(state="closed")
    review_count = 0
    review_code_line_count = 0

    print(SINCE_DATETIME)
    for pr in pull_requests:
        review_comments = pr.get_review_comments()

        # 统计2022-11-6~2023-11-6期间，非HydrogenSulfate的已合并pr的review数据情况
        if not (SINCE_DATETIME < pr.created_at and pr.created_at < UNTIL_DATETIME):
            if pr.created_at < SINCE_DATETIME:
                # 早于2022-11-6，直接退出循环
                print(
                    f"pr.created_at is {pr.created_at}, earlier than {SINCE_DATETIME}, break..."
                )
                break
            else:
                # 否则只跳过，不退出循环
                print(
                    f"pr.created_at is {pr.created_at}, not in {SINCE_DATETIME} ~ {UNTIL_DATETIME}, skip..."
                )
                continue

        if pr.is_merged() and pr.user.login != "HydrogenSulfate":
            print(
                f'[{pr.created_at}], creator="{pr.user.login}", title="{pr.title}", '
                f"#review_comments={review_comments.totalCount}"
            )

            pages = review_comments.get_page(0)
            for page in pages:
                if page.user.login == "HydrogenSulfate":
                    # 1. 统计review评论数量
                    review_count += 1
                    # 2. 统计review代码行数
                    review_code_line_count += len(page.diff_hunk.split("\n"))
                    print(
                        f"review_count is: {review_count}, "
                        f"review_code_line_count is: {review_code_line_count}"
                    )

    return review_count, review_code_line_count


def get_merge_count(repo_name):
    g = Github(GITHUB_PERSONAL_TOKEN)
    repo = g.get_repo(repo_name)

    pull_requests = repo.get_pulls(state="closed")
    merge_count = 0
    merge_code_line_count = 0

    print(SINCE_DATETIME)
    for pr in pull_requests:
        # 统计2022-11-6~2023-11-6期间，非HydrogenSulfate的已合并pr的review数据情况
        if not (SINCE_DATETIME < pr.created_at and pr.created_at < UNTIL_DATETIME):
            if pr.created_at < SINCE_DATETIME:
                # 早于2022-11-6，直接退出循环
                print(
                    f"pr.created_at is {pr.created_at}, earlier than {SINCE_DATETIME}, break..."
                )
                break
            else:
                # 否则只跳过，不退出循环
                print(
                    f"pr.created_at is {pr.created_at}, not in {SINCE_DATETIME} ~ {UNTIL_DATETIME}, skip..."
                )
                continue

        if pr.is_merged() and pr.user.login == "HydrogenSulfate":
            print(
                f"[{pr.created_at}], creator={pr.user.login}, title={pr.title}"
            )
            # 1. 统计合并次数
            merge_count += 1
            # 2. 统计合并的有效代码行数(新增+删除)
            merge_code_line_count += pr.additions + pr.deletions
            print(
                f"merge_count is: {merge_count}, "
                f"merge_code_line_count is: {merge_code_line_count}"
            )

    return merge_count, merge_code_line_count


if __name__ == "__main__":
    repo_name_list = [
        "PaddlePaddle/PaddleScience",
        "lululxvi/deepxde",
        "PaddlePaddle/PaddleClas",
        "PaddlePaddle/Paddle",
    ]

    # 统计review情况
    for repo_name in repo_name_list:
        review_count, review_code_line_count = get_review_count(repo_name)
        print(
            f"{repo_name}: review_count={review_count}, "
            f"review_code_line_count={review_code_line_count}"
        )

    # 统计merge情况
    for repo_name in repo_name_list:
        merge_count, merge_code_line_count = get_merge_count(repo_name)
        print(
            f"{repo_name}: merge_count={merge_count}, "
            f"merge_code_line_count={merge_code_line_count}"
        )
