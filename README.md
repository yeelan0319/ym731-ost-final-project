#Hao Question Documentation


#Application Features

## user authentication
This is handled by take advantage of Google's API associtated with GAE, so that people can use their google ID to sign in

##Question List
The question list page list all questions created so far.

- user no matter signed in or not can view the question list
- list fetches 10 questions each time and when user scroll approaching the bottom of the page, it will automatically trigger the fetch function and get the next 10 items (inifinite scroll)
- the question is fetched by descending order of update time(utime)
- the question content is trunked to 500 words and hyperlink, images is not resolved in this page.
- a hyperlink is provided so when user click on the preview, it will jump to the detail page of  the question

##Question Detail
In the question detail page, you can view the detail information of this question and associated answers to this question.

- user no matter signed in or not can view the question detail
- full content of the question with the hyperlinked resolved as \<a\> tag, images hyperlink resolved as \<img\> tag
- user will be able to vote up and down for a question
- user will be able to add tags to questions
- anser is fetch and ordered by the descending of vote numbers
- The owner of the question/answer will be able to edit/delete this item, however, others may not. 
- You can create new answer to this question on detailed page
- You can generate RSS file of this question by clicking on the upper-right rss button

##Image upload
- upload all type of image with the correct MIME type
- all uploaded image will be provided with a permlink, so you can paste in text
- all uploaded image will be able to be viewed in the image upload page


##Question creation

- question can be created either at question page or detail page through modal



#Implementation

##Overview
The application is basically served with a single python script called "ym731.py" because of its scope is not that large.

The skelton of the application is served using backend template and all within page interaction is through ajax request and update the page with the json object returned.


##API

The application provides a RESTful like API.

**/questions**

- [GET] Returns the rended question items with question.html template
	
- [POST] Create a new question and returns its key


**/questions/qid**

- [GET] Returns the rendered question detail page with detail.html template

- [POST] Vote up/down for the question, I know this go against the idea of REST design but just want to save a API
	
- [PUT] Edit the content/title/tag of the question

- [DELETE] Delete the question
	
**/questions/qid/answers/**

- [POST] Create a new answer to the question with that qid

**/questions/qid/answers/aid**
- [POST] Vote up/down for the answer, the same reason for question
	
- [PUT] Edit the content of the answer

- [DELETE] Delete the answer

**/questions/id/rss**

- [GET] Returns the rendered rss page with rss.html

**/images**

- [GET] Returns the rended image list with image.html

- [POST] Upload a new image
**/images/iid**

- [GET] Returns the image file blob with the that iid

###Returns of the API

The API will return either an html file for browser request or json string for ajax request.

The returned json object will have the following structure:
	
	{
		status: 200
		data: {
			....		}	}

In which case, status can be the following values:

- **200**: Success. so you can use the data returned to update the page
- **401**: Not Authorized. Basically its because user tries to do something that they are not suppose to do, like delete the question they didn't create. It is prevented from the UI interface, however, since malicious user may communicate directly with API. It is still checked at the backend.
-  **403**: Not Authenticated. Merely because user haven't logged in or session expires.



##Dependencies

The application depends on the following platform & libraries:

Front-end

- Bootstrap
- Flat UI
- Jquery


Back-end (Python)

- Google App Engine
- Webapp2
- Jinja Template

##Extra requirement

###Commits
All git commit is labeled with status of the commit, date, detail description of this commit. It can have the following two state:

- UNSTABLE: the application is not ready for deployment

- RELEASE CANDIDATE: the application is right under self-debugging process, need a final check until is can be tagged as production


###Branches
The application git repo has two branches.

- master:
The main development branch

- rss-off: 
The branch with rss functionality commented out.




 