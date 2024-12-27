class systemInfo:
    def __init__(self, version, codename, branch, build):
        self.version = version
        self.codename = codename
        self.branch = branch
        self.build = build


class platforms:
    def __init__(self, operating_system, version, kernel):
        self.operating_system = operating_system
        self.version = version
        self.kernel = kernel


branches = [
    "Alpha",
    "Dev",
    "Beta",
    "Release Candidate",
    "Release Preview",
    "Release"
]

lunaChatInfo = {
    "Version": systemInfo("1.0", "Andromeda", f"{branches[0]}", "2614"),
    "releaseDate": None,
    "hostPlatforms": [
        platforms("Windows", "11", "NT"),
        platforms("macOS", "14.5", "darwin")
    ]
}


def getLunaChatInfo(selection):
    getInfo = lunaChatInfo.get(selection)
    if isinstance(getInfo, list):
        return [list(vars(item).values()) for item in getInfo]
    elif getInfo is not None:
        return list(vars(getInfo).values())
    else:
        return getInfo
