import os
import json
import requests
from datetime import datetime
from dataclasses import dataclass

GITHUB_TOKEN=os.environ.get("GITHUB_TOKEN")

@dataclass
class ReleaseInfo:
    version: int
    releaseDate: datetime
    branch: str

@dataclass
class BuildMetadata:
    filename: str
    checksum: str
    commit: str
    branch: str

def getReleaseInfo(releaseVersion):
    # Get next version
    milestones = requests.get(f"https://chromiumdash.appspot.com/fetch_milestone_schedule?mstone={releaseVersion}").json()
    releaseDate = datetime.fromisoformat(milestones["mstones"][0]["stable_date"])
    print(f"Release: version {releaseVersion}, date: {releaseVersion}")

    # Get next version branch
    releases = requests.get(f"https://chromiumdash.appspot.com/fetch_milestones?mstone={releaseVersion}").json()
    releaseBranch = "branch-heads/" + releases[0]["webrtc_branch"]

    return ReleaseInfo(version = releaseVersion, releaseDate = releaseDate, branch = releaseBranch)

def buildWebRTC(branch):
    os.environ["BUILD_VP9"] = "true"
    os.environ["BRANCH"] = branch
    os.environ["IOS"] = "true"
    os.environ["MACOS"] = "true"
    os.environ["MAC_CATALYST"] = "true"

    return os.system('sh scripts/build.sh') == 0

def getBuildMetadata(outputDir):
    with open(f"{outputDir}/metadata.json", 'r') as f:
        jsonData = json.loads(f.read())
        return BuildMetadata(filename = jsonData['file'], checksum = jsonData['checksum'], commit = jsonData['commit'], branch = jsonData['branch'])

def createReleaseDraft(release, buildMetadata):
    body = f"Release notes: https://webrtc.googlesource.com/src.git/+log/refs/{buildMetadata.branch}/\n"
    body += f"WebRTC Branch: [{buildMetadata.branch}](https://chromium.googlesource.com/external/webrtc/+log/{buildMetadata.branch})\n"
    body += f"WebRTC Commit: `{buildMetadata.commit}`\n"
    body += f"SHA 256 checksum: `{buildMetadata.checksum}`"

    fields = { 
        'name': f'M{release.version}',
        'tag_name': f'{release.version}.0.0',
        'draft': True,
        'body': body
    }
    headers = {'accept': 'application/vnd.github.v3+json', 'Authorization': f'token {GITHUB_TOKEN}'}
    return requests.post("https://api.github.com/repos/EffectsSDK/WebRTC/releases", json = fields, headers = headers).json()

def uploadReleaseAsset(url, assetLocalPath, assetName):
    url = url.replace(u'{?name,label}','')
    fileToUpload = open(assetLocalPath, 'rb')  
    size = os.stat(assetLocalPath).st_size
    params = {'name': assetName}
    headers = {'Authorization': f'token {GITHUB_TOKEN}', 'Content-Length': str(size), 'Content-Type': 'Application/zip'}
    response = requests.post(url, params = params, data = fileToUpload, headers = headers)
    success = response.status_code == requests.codes.created
    if not success:
        print(response)
    return success

def createPullRequest(release, head):
    headers = {'accept': 'application/vnd.github.v3+json', 'Authorization': f'token {GITHUB_TOKEN}'}
    body = { 
        'title': f'Release M{release.version}',
        'head': head,
        'base': 'latest',
        'body': 'Created by an automated sotfware 🤖'
    }
    response = requests.post("https://api.github.com/repos/EffectsSDK/WebRTC/pulls", json = body, headers = headers)
    success = response.status_code == requests.codes.created
    if not success:
        print(response)
    return success

if __name__ == "__main__":
    if not GITHUB_TOKEN:
        print("❌ GITHUB_TOKEN environment variable is not provided")
        os._exit(os.EX_SOFTWARE)

    releaseVersion = os.environ.get("WEBRTC_MILESTONE")

    print("➡️ Fetching release info...")
    releaseInfo = getReleaseInfo(releaseVersion)

    # Build WebRTC Frameworks
    print("➡️ Building WebRTC Library...")
    buildSuccess = buildWebRTC(releaseInfo.branch)
    if not buildSuccess:
        print("❌ WebRTC Build Failed")
        os._exit(os.EX_SOFTWARE)
        
    print("✅ WebRTC build successful\n")

    # Get metadata build file - it has all the information needed about the build
    outputDir="src/out"
    buildMetadata = getBuildMetadata(outputDir)
    print(buildMetadata)

    # Create new release draft
    print("➡️ Creating new release draft...")
    githubReleaseDraft = createReleaseDraft(releaseInfo, buildMetadata)

    # Upload asset to github
    print("➡️ Uploading asset to github...")
    assetName = f"WebRTC-M{releaseInfo.version}.xcframework.zip"
    assetPath = os.path.join(outputDir, buildMetadata.filename)
    uploadURL = githubReleaseDraft['upload_url']
    uploadResult = uploadReleaseAsset(uploadURL, assetPath, assetName)

    if not uploadResult:
        print("❌ Failed uploading asset to github")
        os._exit(os.EX_SOFTWARE)

    print(f"✅ Successfully created new draft release in github: {githubReleaseDraft['url']}")

    # Create new branch with code changes
    print("➡️ Creating local branch...")
    releaseBranch = f'release-M{releaseInfo.version}'
    os.system(f'git checkout -b {releaseBranch}')

    # Change code
    print("➡️ Applying code changes...")
    os.system(f"sed -i '' -E 's/[0-9]+.0.0\/WebRTC-M[0-9]+/{releaseInfo.version}.0.0\/WebRTC-M{releaseInfo.version}/g' Package.swift ")
    os.system(f"sed -i '' -E 's/checksum: \"[0-9a-f]+\"/checksum: \"{buildMetadata.checksum}\"/g' Package.swift ")
    os.system(f"sed -i '' -E 's/.upToNextMajor\\(\"[0-9]+.0.0/.upToNextMajor\\(\"{releaseInfo.version}.0.0/g' README.md")


    # Commit and push
    print("➡️ Commiting and pushing code to remote...")
    os.system(f'git add Package.swift README.md')
    os.system(f'git commit -m "Updated files for release M{releaseInfo.version}"')
    os.system(f'git push origin {releaseBranch}')

    # Create PR
    print("➡️ Creating pull request...")
    prResult = createPullRequest(releaseInfo, releaseBranch)
    if not prResult:
        print("❌ Failed creating pull request in github")
        os._exit(os.EX_SOFTWARE)

    print(f"✅ Done")
