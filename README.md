# web-admin-basics

Linux is an amazing OS where it runs from the smallest computers such as Raspberry Pi (http://www.raspbian.org/) 
to Smartphones (https://haydenjames.io/85-of-all-smartphones-are-powered-by-linux/) to 
Supercomputer clusters (https://itsfoss.com/linux-runs-top-supercomputers/). 

But the most popular use of Linux has to be running web servers on the Internet.  The goal of this assignment is to 
teach you to run your own web server so anyone on the Internet can access your content and run your scripts.

You should have received an email from AWS academy, which gives you $100 credit to access the Amazon Web Services (AWS) 
console. 

Launch your own Linux instance with Apache HTTP server on AWS

1. Follow this video to setup your aws account: https://youtu.be/puu_G8ANeTM 

   Note: if you are using PuTTY to connect to your ec2 instance, please follow these instructions: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/putty.html 

2. Follow this video to get a quick introduction on installing and using apache2 web server: https://youtu.be/KyN0DTeSE8A.  Notes:
   - We will be using Ubuntu Server 22.04, which is a very popular linux distribution. 
   - Make sure your instance type is t2.nano, this is minimize your cost
   - By default, the apache http server stores files in these locations
      - Static files: /var/www/html/
      - CGI scripts: /usr/lib/cgi-bin/
      - Configuration files: /etc/apache2/

3. Getting a static ip to your instance using AWS’s “Elastic IP” feature
   - You instance’s IP may change between start and stop.  For a web server, we want the IP to not change
   - https://youtu.be/mgfpduy5ZAo 
   - After following the instructions, try stopping and restarting your instance to make sure that the IP is preserved

4. Create DNS entry
   - DNS is used to associate meaningful names with ip address
   - I reserved the wmdd4950.com domain for this class
   - I also setup a simple REST API so you can manage creating and deleting wmdd4950.com subdomains
   - Pick a subdomain of your choice and associate your static ip with it

   - DNS API
      - List all subdomains: `curl api.wmdd4950.com/arecord/list`
      - Add a subdomain: `curl api.wmdd4950.com/arecord/${sub_domain}?ip=${ip_address}`
      - For example, the following command will associate the ip address 54.70.53.85 with jmadar.wmdd4950.com
      - `curl api.wmdd4950.com/arecord/jmadar?ip=54.70.53.85`
      - To delete a subdomain: `curl -XDELETE api.wmdd4950.com/arecord/${sub_domain}`
      - For example, to delete the jmadar.wmdd4950.com subdomain: `curl -XDELETE api.wmdd4950.com/arecord/jmadar`
   
# Hand-in

1. Follow all the instructions/videos from above to setup your server, including putting **`test.sh`** inside the 
`/usr/lib/cgi-bin/` directory.

2. Clone this assignment repository under your home directory (i.e. `/home/ubuntu/`)
   
4. Install the following python packages so pytest can run:
   - `sudo apt install -y python3-pip python-is-python3; pip install pytest`
   - Exit and relogin

6. Run `pytest` at the top level of your assignment repo, this will copy all the relevant files to assignment repo
   and check them for errors.

   - NOTE: running pytest will create a file called my_ip.txt in your assignment repo.  This file contained your
   sever's ip address using auto detection.  If your server ip has changed, you will need to delete this file so
   pytest will re-create it.

7. When you are satisified, run the following commands to submit:
   - `git add -A`
   - `git commit -a -m 'submit'`
   - `git push` 






