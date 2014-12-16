$(document).ready(function(){
	//render the data within the modal for edit question & answer
	$('#edit-question-modal').on('show.bs.modal', function (event) {
		var modal = $(this);
	  	var qid = $(event.relatedTarget).data('content');
	  	var title = $("#question-" + qid).find(".question-title").text().trim();
	  	var content = $("#question-" + qid).find(".question-text").text().trim();
	  
	  	modal.data('content', qid);
	  	modal.find('input').val(title);
	  	modal.find('textarea').val(content)
	});
	$('#edit-answer-modal').on('show.bs.modal', function (event) {
		var modal = $(this);
	  	var aid = $(event.relatedTarget).data('content');
	  	var content = $("#answer-" + aid).find(".answer-text").text().trim();
	  	
	  	modal.data('content', aid);
	  	modal.find('textarea').val(content)
	});

	// submit the create/edit result via modal
	$("#create-new-question-modal").find("button").click(function(){
		var title = $("#create-new-question-modal").find("input").val();
		var content = $("#create-new-question-modal").find("textarea").val();
		console.log(title);
		console.log(content);
		alert("I am clicked");
	});
	$("#edit-question-modal").find("button").click(function(){
		var qid = $("#edit-question-modal").data("content");
		var title = $("#edit-question-modal").find("input").val();
		var content = $("#edit-question-modal").find("textarea").val();
		console.log(qid, title, content);
		alert("I am clicked");
	});
	$("#edit-answer-modal").find("button").click(function(){
		var aid = $("#edit-answer-modal").data("content");
		var content = $("#edit-answer-modal").find("textarea").val();
		console.log(aid, content);
		alert("I am clicked");
	});
	// submit the create new answer via input area below
	$("#create-new-answer").find("button").click(function(){
		var content = $("#create-new-answer").find("textarea").val();
		console.log(content);
		alert("I am clicked");
	});

	//vote up/down and delete event for question & answer
	$(".question-vote-up-btn").click(function(){
		alert("vote up for question: " + $(this).data("content"));
	});
	$(".question-vote-down-btn").click(function(){
		alert("vote down for question: " + $(this).data("content"));
	});
	$(".question-delete").click(function(){
		alert("delete question: " + $(this).data("content"));
	});
	$(".main-content").delegate(".answer-vote-up-btn", "click", function(){
		alert("vote up for answer: " + $(this).data("content"));
	});
	$(".main-content").delegate(".answer-vote-down-btn", "click", function(){
		alert("vote down for answer: " + $(this).data("content"));
	});
	$(".main-content").delegate(".answer-delete", "click", function(){
		alert("delete answer: " + $(this).data("content"));
	});
}) 