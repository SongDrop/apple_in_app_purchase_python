# apple_in_app_purchase_python

AWS Lambda Python Code + JWT_AWS_LAMBDA_LAYER_ZIP_LINUX

Invalid ELF header ERROR caused by JWT layer.zip was built on MacOS while AWS Lambda runs on Linux.
This JWT layer.zip is built on Linux

Root cause for invalid elf header error

When executed, AWS Lambdas run on a Linux platform. If you are experiencing an invalid ELF header error, it is because the binaries included in your deployment package were built for a platform other than Linux. Typically you will see this issue when you develop your lambda in a non Linux environment.

How to resolve an invalid ELF header error

Now that we know why we are experiencing this issue, it is time to find a solution. This is where Docker comes into the picture. After you have developed your AWS Lambda, you should spin up a linux container with a bind mount, install all of your dependencies, and create your deployment package. This will ensure that all of your binaries are Linux compatible, resolving your invalid ELF header issue.

Creating a python AWS Lambda deployment using Docker

First we need to start an Ubuntu Docker container with a bind mount.

docker run -v directory_to_lambda_code:/lambda -it --rm ubuntu
Next, we install python3, pip, and zip.
```
apt-get update && apt-get install -y -qq python3-pip git \
&& cd /usr/local/bin && ln -s /usr/bin/python3 python \
&& python3 -m pip install --upgrade pip \
&& python3 -m pip install ipython \
&& rm -rf /var/lib/apt/lists/\*
apt-get update && apt-get install zip
```
At this point, we can change to the directory that contains our code and begin installing all required python modules.
```
cd /lambda
pip install -t . pip_module_name
```
Finally, we can create our deployment package.

zip -r9 name_of_deployment_package .
Conclusion

With our newly created python AWS Lambda deployment package, we can now upload and execute our lambda without fear of encountering an invalid ELF header error.
