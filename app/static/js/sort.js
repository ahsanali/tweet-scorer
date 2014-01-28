//This Functions sorts tweets according to parameters provided.
function tweet_sort(sort_class){
	
	//Fetching All the divs whch 'media' class 
	var myrow = new Array();
	$(".media").each(function(data){
		myrow[data] = this;
	});

	//Sorting Them according to provided call
	myrow.sort(function(a,b){
		return 	parseFloat(String($(b).find(sort_class).text()).trim()) - 
				parseFloat(String($(a).find(sort_class).text()).trim())
	});
	
	var newhtml=""
	for(i=0 ; i < myrow.length ; i++){
		newhtml = newhtml + "<div class='media'>"+$(myrow[i]).html()+"</div>";
	}
	$("#tweet-container").html(newhtml);
}