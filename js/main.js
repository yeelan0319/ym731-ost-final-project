$(document).ready(function(){
	$("#create-new-question-modal").find("button").click(function(){
		var title = $("#create-new-question-modal").find("input").val();
		var content = $("#create-new-question-modal").find("textarea").val();
		console.log(title);
		console.log(content);
		alert("I am clicked");
	});
}) 