"""Fetch live GitHub stats and rebuild the SVG cards.
Needs env vars: ACCESS_TOKEN (personal access token) and USER_NAME.
"""
import os, requests
from datetime import datetime
import build_svg

TOKEN = os.environ["ACCESS_TOKEN"]
USER = os.environ.get("USER_NAME", build_svg.USER)
H = {"Authorization": f"bearer {TOKEN}"}


def gql(query, **variables):
    r = requests.post("https://api.github.com/graphql", json={"query": query, "variables": variables}, headers=H, timeout=30)
    r.raise_for_status()
    data = r.json()
    if "errors" in data:
        raise RuntimeError(data["errors"])
    return data["data"]


def main():
    d = gql("""query($u:String!){ user(login:$u){ createdAt followers{totalCount}
        repositories(ownerAffiliations:OWNER, first:100){ totalCount nodes{stargazerCount} }
        repositoriesContributedTo(first:1, contributionTypes:[COMMIT,PULL_REQUEST,REPOSITORY]){ totalCount } } }""", u=USER)["user"]
    stars = sum(n["stargazerCount"] for n in d["repositories"]["nodes"])
    commits = 0
    for year in range(int(d["createdAt"][:4]), datetime.now().year + 1):
        c = gql("""query($u:String!,$f:DateTime!,$t:DateTime!){ user(login:$u){
            contributionsCollection(from:$f,to:$t){ totalCommitContributions restrictedContributionsCount } } }""",
                u=USER, f=f"{year}-01-01T00:00:00Z", t=f"{year}-12-31T23:59:59Z")["user"]["contributionsCollection"]
        commits += c["totalCommitContributions"] + c["restrictedContributionsCount"]
    build_svg.build({
        "repos": d["repositories"]["totalCount"],
        "contrib": d["repositoriesContributedTo"]["totalCount"],
        "stars": stars,
        "commits": f"{commits:,}",
        "followers": d["followers"]["totalCount"],
    })


if __name__ == "__main__":
    main()
