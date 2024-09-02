import pbr.version

# Create a VersionInfo object for your project
version_info = pbr.version.VersionInfo('python-openstackclient')

try:
    # Try to retrieve the version string
    version = version_info.version_string()
    print(f"Version: {version}")
except Exception as e:
    print(f"Error: {e}")
