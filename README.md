<h2>How to run the project</h2>
<li>Download the zip file and extract the file on local machine</li>
<li>Go inside webapp directory</li>
<li>Open terminal and run command "./manage.py runserver"</li>
<li>On successfull running of server, open browser and hit http://localhost:8000</li>
<br>
<h2>Api Specification</h2>

<li><strong>Register-</strong> It will ask three parameters, Name, email, user's access key. A random key can also be generated using management command</li>
<li><strong>Post-</strong> It will require access key and an image, This image will be stored in the file system (BaseDirectory/tmp/UserName_UserKey)</li>
<li><strong>Delete-</strong> It will require access key and image which you want to delete from the file system (If the image is not there it will return 400:Bad Request)</li>
<li><strong>Update-</strong> It will require access key and image which will be replaced by already existing image with the same name as that of the provided image</li>
<li><strong>All-</strong> It will require access key and will display all the image associated with the access key in the folder(BaseDirectory/tmp/UserName_UserKey)</li>
<li><strong>One-</strong> It will require access key and an image which will be displayed from the file system</li>
<li><strong>Forgot-</strong> This will require your email address with which you have registered yourself. Access key will mailed to your email address</li>
