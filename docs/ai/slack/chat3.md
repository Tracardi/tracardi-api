# Does the latest version of Tracardi support Python 3.10 and above?

Yes, the latest version of Tracardi supports Python 3.10 and above.

# I am setting up the Python Dev Environment following the instructions in the Tracardi Documentation, but I encountered an error while trying to install the requirements. What should I do?

The error message states that the 'tracardi' package requires a different Python version, specifically 3.9.16 instead
of '>=3.10'. Before this, you mentioned trying to install it with Python 3.10 but faced an issue with the celery
library. Did you clone Tracardi from version branch or master? The master branch is unstable. It is recommended to use
tagged branches and clone from the version branch.

# I have a question: Am I installing Tracardi from source to contribute, or am I simply interested in trying the new version? Is there a more convenient way to try the new version?

If you're interested in trying the new version and not contributing, it would be more convenient to use Docker with the
version tag. Otherwise, use source code form the newest version branch.

# Actually, I want to create new plugins and contribute to the platform. Can you help me with that?

Sure please head to our github or slack channel where you can get assistance