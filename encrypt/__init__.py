import os
if not os.path.exists(os.path.join(os.environ.get("HOME"),'.elite')):
    from deps import install_dependencies
    install_dependencies()