$(document).ready(function(){
	//render the data within the modal for edit question & answer
	$('#create-new-question-modal').on('show.bs.modal', function (event) {
		var modal = $(this);
		modal.find(".form-view").removeClass("hide");
		modal.find(".form-view input").val("");
		modal.find(".form-view textarea").val("");
		modal.find(".result-view").addClass("hide");
	});
	$('#edit-question-modal').on('show.bs.modal', function (event) {
		var modal = $(this);
		var qid = $(event.relatedTarget).data('content');
		var questionEl = $("#question-" + qid);
	  	var title = questionEl.find(".question-title").text().trim();
	  	var content = questionEl.find(".question-text").text().trim();
	  
	  	modal.data('content', qid);
	  	modal.find('input').val(title);
	  	modal.find('textarea').val(content)
	});
	$('#edit-answer-modal').on('show.bs.modal', function (event) {
		var modal = $(this);
		var data = $(event.relatedTarget).data('content');
		var qid = data.split(",")[0]
		var aid = data.split(",")[1];
		var answerEl = $("#answer-" + aid);
	  	var content = answerEl.find(".answer-text").text().trim();
	  	
	  	modal.data('content', qid + "," + aid);
	  	modal.find('textarea').val(content)
	});

	// submit the create/edit result via modal
	$("#create-new-question-modal").find("button").click(function(){
		var modal = $("#create-new-question-modal");
		var title = modal.find("input").val();
		var content = modal.find("textarea").val();

		if(title && content){
			var data = {
				content: content,
				title: title
			}
			$.post("/questions", data, function(data){
				data = JSON.parse(data);
				if(data.status == 200){  //which means it success
					var qid = data.data.qid;
					var link = "http://hao-question.appspot.com/questions/" + qid;
					var atag = modal.find(".result-view a");
					atag.attr("href", link);
					atag.text(link);

					modal.find(".form-view").addClass("hide");
					modal.find(".result-view").removeClass("hide");
				}	
			});
		}
	});
	$("#edit-question-modal").find("button").click(function(){
		var modal = $("#edit-question-modal");
		var qid = modal.data("content");
		var title = modal.find("input").val();
		var content = modal.find("textarea").val();
		
		if(title && content){
			var data = {
				type: "content",
				content: content,
				title: title
			}
			$.ajax({
				type: "PUT",
				url: "/questions/" + qid,
				data: data,
				success: function(data){
					data = JSON.parse(data);
					if(data.status == 200){  //which means it success
						var questionEl = $("#question-" + qid);
					  	questionEl.find(".question-title h5").text(title);
					  	questionEl.find(".question-text").html(data.data.content);
					  	modal.modal('hide');
					}	
				}
			});
		}
	});
	$("#edit-answer-modal").find("button").click(function(){
		var modal = $("#edit-answer-modal");
		var data = modal.data("content");
		var qid = data.split(",")[0];
		var aid = data.split(",")[1];
		var content = modal.find("textarea").val();
		
		if(content){
			var data = {
				content: content
			}
			$.ajax({
				type: "PUT",
				url: "/questions/" + qid + "/answers/" + aid,
				data: data,
				success: function(data){
					data = JSON.parse(data);
					if(data.status == 200){  //which means it success
						var answerEl = $("#answer-" + aid);
					  	answerEl.find(".answer-text").html(data.data.content);
					  	modal.modal('hide');
					}	
				}
			});
		}
	});
	// submit the create new answer via input area below
	$("#create-new-answer").find("button").click(function(){
		var qid = $(this).data("content");
		var content = $("#create-new-answer").find("textarea").val();
		
		if(content){
			var data = {
				content: content
			}
			$.post("/questions/" + qid + "/answers", data, function(data){
				data = JSON.parse(data);
				if(data.status == 200){
					var content = data.data.content;
					$('.answers').append(content);
					$("#create-new-answer").find("textarea").val("");
				}
			});
		}
	});

	//vote up/down and delete event for question & answer
	$(".question-vote-up-btn").click(function(){
		var qid = $(this).data("content");
		$.post("/questions/" + qid, {type: "up"}, function(data){
			data = JSON.parse(data);
			if(data.status == 200){
				$("#question-" + qid).find(".question-vote-count").text(data.data.vote);
			}
		});
	});
	$(".question-vote-down-btn").click(function(){
		var qid = $(this).data("content");
		$.post("/questions/" + qid, {type: "down"}, function(data){
			data = JSON.parse(data);
			if(data.status == 200){
				$("#question-" + qid).find(".question-vote-count").text(data.data.vote);
			}
		});
	});
	$(".question-delete").click(function(){
		var qid = $(this).data("content");
		$.ajax({
			type: "DELETE",
			url: "/questions/" + qid,
			success: function(data){
				data = JSON.parse(data);
				if(data.status == 200){  //which means it success
					window.location.href = "/";
				}	
			}
		});
	});
	$(".main-content").delegate(".answer-vote-up-btn", "click", function(){
		var data = $(this).data("content");
		var qid = data.split(",")[0];
		var aid = data.split(",")[1];
		$.post("/questions/" + qid + "/answers/" + aid, {type: "up"}, function(data){
			data = JSON.parse(data);
			if(data.status == 200){
				$("#answer-" + aid).find(".question-vote-count").text(data.data.vote);
			}
		});
	});
	$(".main-content").delegate(".answer-vote-down-btn", "click", function(){
		var data = $(this).data("content");
		var qid = data.split(",")[0];
		var aid = data.split(",")[1];
		$.post("/questions/" + qid + "/answers/" + aid, {type: "down"}, function(data){
			data = JSON.parse(data);
			if(data.status == 200){
				$("#answer-" + aid).find(".question-vote-count").text(data.data.vote);
			}
		});
	});
	$(".main-content").delegate(".answer-delete", "click", function(){
		var data = $(this).data("content");
		var qid = data.split(",")[0];
		var aid = data.split(",")[1];
		$.ajax({
			type: "DELETE",
			url: "/questions/" + qid + "/answers/" + aid,
			success: function(data){
				data = JSON.parse(data);
				if(data.status == 200){  //which means it success
					$("#answer-" + aid).remove();
				}	
			}
		});
	});

	// tags management
	var taginput = $('.question-tagsinput');
	taginput.tagsinput();
	taginput.on('itemAdded itemRemoved', function(event) {
		var qid = $(this).data('content');
		var data = {
			type: "tag",
			tag: $('.question-tagsinput').val()
		}
		$.ajax({
			type: "PUT",
			url: "/questions/" + qid,
			data: data
		});
	});
}) 