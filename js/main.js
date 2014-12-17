var MORE_FLAG = true;
var INFINITE_SCROLL_PX_OFFSET = 150;
var LOADING_LOCK = false;
var cursor = "";

$(document).ready(function(){
	fetchNextPage();

	$(document).scroll(function(){
		var windowTop = $(this).scrollTop();
		var windowBottom = windowTop + $(window).height();
		//Infinite scroll
		if(!LOADING_LOCK & windowBottom + INFINITE_SCROLL_PX_OFFSET > $('body').height() && MORE_FLAG){
			console.log("trigger");
			LOADING_LOCK = true;  //prevent the inf scroll from triggering multiple times
			fetchNextPage();
		}
	});

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
					window.location.reload();
				}	
			});
		}
	});
})

function fetchNextPage(){
	$.get("/questions?cursor=" + cursor, function(data){
		data = JSON.parse(data);
		if(data.status == 200){
			var content = data.data.content;
			MORE_FLAG = data.data.more;
			cursor = data.data.next_curs;

			$('.main-content').append(content);
			LOADING_LOCK = false;
		}
	})
} 