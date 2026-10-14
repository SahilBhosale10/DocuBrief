import argostranslate.package


# Get all available translation packages
available_packages = argostranslate.package.get_available_packages()


# Languages we need
required_languages = [
    ("en", "hi"),
    ("en", "mr")
]


for from_code, to_code in required_languages:

    print(f"\nLooking for {from_code} -> {to_code}...")

    package_to_install = None

    for package in available_packages:

        if (
            package.from_code == from_code
            and package.to_code == to_code
        ):

            package_to_install = package
            break


    if package_to_install:

        print("Package found.")

        print("Downloading package...")

        download_path = package_to_install.download()

        print("Installing package...")

        argostranslate.package.install_from_path(
            download_path
        )

        print(
            f"{from_code} -> {to_code} installed successfully."
        )

    else:

        print(
            f"{from_code} -> {to_code} package not found."
        )