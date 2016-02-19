//test whether page is loading script
console.log('Script loaded');

//assigning lists from HTML to variables
var toDoList = $('#todolist');
var completeList = $('#donelist');

//add new item to TO DO list from text field
function newListItem() {
	var addedItem = $('#newlistitem').val();
	$('#todolist').prepend("<li>" + addedItem +'</li><button onclick="moveToDone()">Done</button>');
	//console.log(toDoList);
	$('#newlistitem').val('');

}

//move item from ToDo list to done list...not working due to difficulty capturing current element
//fail...
function moveToDone() {
	alert($(this).text);
	//var thisitem = $("button").closest("li").text();
	//thisitem=$("button").closest("li").val();
	//var current = $(this).closest().innerHTML;
	//alert(current)
	//alert(current);
	//$('#donelist').prepend(thisitem);
	//alert(thisitem.text());
	//console.log($("button").closest("li").html())
	//$("#donelist").prepend("<li>" +thisitem.text() + '<button type="button" onclick="moveBackToDo()">Done</button></li>');
	//thisitem.remove();

}
//placeholder for moving things back to todo list
function moveBackToDo (){
	alert('Back!');
}

//former test function when I was trying to do this by arrays; no longer used
function reciteAll() {
	console.log('Reciting');
	for (i=toDoList.length-1; i>=0; i--) {
		alert(toDoList[i]);
	}
}
