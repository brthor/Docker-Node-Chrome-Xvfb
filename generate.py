import os, json

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

def readFileArray(filename):
    with open(filename, 'r') as f:
        return [line.replace("\n", "") for line in f.read().split("\n")]

def versionStrings(nodeVersion, puppeteerVersion):
    version = '{0}-{1}'.format(nodeVersion, puppeteerVersion)
    versionPath = "version/{0}".format(version)

    if not os.path.exists(versionPath):
        os.makedirs(versionPath)

    return (version, versionPath)


nodeVersions = readFileArray("NODE_VERSIONS")
puppeteerVersions = readFileArray("PUPPETEER_VERSIONS")

if __name__ == '__main__':
    dockerfileInformationArr = []

    for nodeVersion in nodeVersions:
        for puppeteerVersion in puppeteerVersions:
            version, versionPath = versionStrings(nodeVersion, puppeteerVersion)
            dockerfileInformationArr.append(dict(branch='master', tag=version, path='/' + versionPath))

    # Generate Browser Scripts
    with open('./browser-scripts/dockerhub.com-addAllVersionsToBuildSettings.js.template', 'r') as f:
        fContents = f.read()
        newContents = fContents.replace('{dockerfile_information_arr}', json.dumps(dockerfileInformationArr))

        with open('./browser-scripts/dockerhub.com-addAllVersionsToBuildSettings.js', 'w') as nf:
            print("Writing: browser-scripts/dockerhub.com-addAllVersionsToBuildSettings.js")
            nf.write(newContents)

    for nodeVersion in nodeVersions:
        for puppeteerVersion in puppeteerVersions:
            version, versionPath = versionStrings(nodeVersion, puppeteerVersion)

            # Generate Dockerfiles
            with open(versionPath + "/Dockerfile", "w") as f:
                print("Writing: " + versionPath)
                f.write(dockerfileTemplate.format(node_version=nodeVersion, puppeteer_version=puppeteerVersion))



