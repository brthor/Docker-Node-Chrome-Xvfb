import os

dockerfileTemplate = """FROM node:{0}-slim

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

"""

nodeVersions = [
    "10.6.0",
    "10.5.0",
    "10.4.1",
    "10.4.0",
    "10.3.0",
    "10.2.1",
    "10.2.0",
    "10.1.0",
    "10.0.0",
    "9.11.2",
    "9.11.1",
    "9.11.0",
    "9.10.1",
    "9.10.0",
    "9.9.0",
    "9.8.0",
    "9.7.1",
    "9.7.0",
    "9.6.1",
    "9.6.0",
    "9.5.0",
    "9.4.0",
    "9.3.0",
    "9.2.1",
    "9.2.0",
    "9.1.0",
    "9.0.0",
    "8.11.3",
    "8.11.2",
    "8.11.1",
    "8.11.0",
    "8.10.0",
    "8.9.4",
    "8.9.3",
    "8.9.2",
    "8.9.1",
    "8.9.0",
    "8.8.1",
    "8.8.0",
    "8.7.0",
    "8.6.0",
    "8.5.0",
    "8.4.0",
    "8.3.0",
    "8.2.1",
    "8.2.0",
    "8.1.4",
    "8.1.3",
    "8.1.2",
    "8.1.1",
    "8.1.0",
    "8.0.0"]

if __name__ == '__main__':
    for nodeVersion in nodeVersions:
        versionPath = 'version/' + nodeVersion
        if not os.path.exists(versionPath):
            os.makedirs(versionPath)

        with open(versionPath + "/Dockerfile", "w") as f:
            f.write(dockerfileTemplate.format(nodeVersion))

