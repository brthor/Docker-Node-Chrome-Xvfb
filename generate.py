import os, json, subprocess
from multiprocessing import Pool

dockerfileTemplate = """FROM node:{node_version}-slim

# Install latest chrome package.
# Note: this installs the necessary libs to make the bundled version of Chromium that Pupppeteer
# installs, work.
RUN apt-get update && apt-get install -y wget --no-install-recommends \\
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \\
    && sh -c 'echo ""deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main"" >> /etc/apt/sources.list.d/google.list' \\
    && apt-get update \\
    && apt-get install -y google-chrome-stable \\
    --no-install-recommends \\
    && rm -rf /var/lib/apt/lists/* \\
    && apt-get purge --auto-remove -y curl \\
    && rm -rf /src/*.deb

RUN apt-get update && apt-get install -y xvfb xauth \\
    && rm -rf /var/lib/apt/lists/* \\
    && rm -rf /src/*.deb

RUN mkdir -p /app

RUN cd /app && echo "{{}}" > package.json && npm install --save puppeteer@{puppeteer_version}

"""

class CmdResult(object):
    def __init__(self, returncode, stdout, stderr):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        self.failed = self.returncode != 0

    def dump(self):
        print("-- STDOUT --")
        print(self.stdout)
        print("-- END STDOUT --")
        print("-- STDERR --")
        print(self.stderr)
        print("-- END STDERR --")

    @classmethod
    def get(cls, cmdArr, timeout=900):
        proc = subprocess.Popen(cmdArr, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        outs, errs = proc.communicate()
        
        return cls(proc.returncode, outs, errs)


def readFileArray(filename):
    with open(filename, 'r') as f:
        return [line.replace("\n", "") for line in f.read().split("\n")]


def versionStrings(nodeVersion, puppeteerVersion):
    version = '{0}-{1}'.format(nodeVersion, puppeteerVersion)
    versionPath = "version/{0}".format(version)

    if not os.path.exists(versionPath):
        os.makedirs(versionPath)

    return (version, versionPath)


def buildDockerImage(nodeVersion, puppeteerVersion):
    version, versionPath = versionStrings(nodeVersion, puppeteerVersion)
    print "Building docker image.", version
    with open(versionPath + "/Dockerfile", "w") as f:
        f.write(dockerfileTemplate.format(node_version=nodeVersion, puppeteer_version=puppeteerVersion))

    CmdResult
    cmdResult = CmdResult.get(["docker", "build", "-t", "brthornbury/docker-node-chrome-puppeteer-xvfb:" + version, versionPath])
    if (cmdResult.failed):
        cmdResult.dump()
        raise Exception("failed to build docker image " + version)
    
    print "Finished building docker image.", version


def pushDockerImage(version):
    print "Pushing docker image.", version
    cmdResult = CmdResult.get(["docker", "push", "brthornbury/docker-node-chrome-puppeteer-xvfb:" + version])
    if (cmdResult.failed):
        cmdResult.dump()
        raise Exception("failed to push docker image " + version)

    print "Finished pushing docker image.", version


def buildAndPushDockerImage(versionTuple):
    nodeVersion, puppeteerVersion = versionTuple
    version, versionPath = versionStrings(nodeVersion, puppeteerVersion)

    try:
        buildDockerImage(nodeVersion, puppeteerVersion)
        pushDockerImage(version)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    nodeVersions = readFileArray("NODE_VERSIONS")
    puppeteerVersions = readFileArray("PUPPETEER_VERSIONS")

    versionSuperset = [(x,y) for x in nodeVersions for y in puppeteerVersions]
    print("Building {0} docker images...".format(len(versionSuperset)))

    concurrency = 10
    pool = Pool(processes=concurrency)

    pool.map(buildAndPushDockerImage, versionSuperset)
